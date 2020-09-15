# python imports
import math
import logging
import json
from datetime import datetime, timedelta
import time

from decimal import Decimal
from dateutil import relativedelta

# django imports
from django.db import models
from django.db.models import Q, Count, Case, When, IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django_mysql.models import ListTextField
from django.core.cache import cache
from django.db.models.signals import post_save
from django.core.cache import cache

# local imports
from .choices import STATUS_CHOICES, SITE_CHOICES,\
    PAYMENT_MODE, OI_OPS_STATUS, OI_LINKEDIN_FLOW_STATUS,\
    OI_USER_STATUS, OI_EMAIL_STATUS, REFUND_MODE, REFUND_OPS_STATUS,\
    TYPE_REFUND, OI_SMS_STATUS, WC_CATEGORY, WC_SUB_CATEGORY,\
    WC_FLOW_STATUS, OI_OPS_TRANSFORMATION_DICT, LTV_BRACKET_LABELS, \
    SHINE_ACTIVATION

from .functions import get_upload_path_order_invoice, process_application_highlighter
from .tasks import generate_resume_for_order, bypass_resume_midout, upload_Resume_shine, board_user_on_neo, av_user_enrollment, update_purchase_on_shine

# inter app imports
from linkedin.models import Draft
from seo.models import AbstractAutoDate
from geolocation.models import Country, CURRENCY_SYMBOL
from users.models import User
from console.feedbackCall.choices import FEEDBACK_RESOLUTION_CHOICES, FEEDBACK_CATEGORY_CHOICES, FEEDBACK_STATUS, TOTAL_FEEDBACK_OPERATION_TYPE
from order.utils import get_ltv
from coupon.models import Coupon
from order.utils import FeatureProfileUtil


# third party imports
from payment.utils import manually_generate_autologin_url
from shop.choices import S_ATTR_DICT, DAYS_CHOICES_DICT, AV_STATUS_CHOICES
from coupon.models import Coupon


# Global Constants
CURRENCY_SYMBOL_CODE_MAPPING = {0: "INR", 1: "USD", 2: "AED", 3: "GBP"}


class GazettedHoliday(models.Model):
    holiday_date = models.DateField(unique=True)
    holiday_type = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        if not self.holiday_type:
            return ""
        return self.holiday_type

    @property
    def get_holiday_list(self):
        dates = list(GazettedHoliday.objects.all(
        ).values_list('holiday_date', flat=True))
        holidays = []
        for day in dates:
            holidays.append(day.strftime('%d-%m-%Y'))
        return holidays


class Order(AbstractAutoDate):
    co_id = models.IntegerField(
        _('CP Order'),
        blank=True,
        null=True,
        editable=False)
    archive_json = models.TextField(
        _('Archive JSON'),
        blank=True,
        editable=False)

    number = models.CharField(
        _("Order number"), max_length=128, db_index=True)

    site = models.PositiveSmallIntegerField(default=0, choices=SITE_CHOICES)

    # customer information
    candidate_id = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Customer ID"))

    status = models.PositiveSmallIntegerField(
        default=0, choices=STATUS_CHOICES)

    currency = models.PositiveIntegerField(
        _("Currency"), choices=CURRENCY_SYMBOL, default=0)

    total_incl_tax = models.DecimalField(
        _("Payable Amount (inc. tax)"),
        decimal_places=2, max_digits=12, default=0)
    total_excl_tax = models.DecimalField(
        _("Total Amount (excl. tax excl. Point)"),
        decimal_places=2, max_digits=12, default=0)
    conv_charge = models.DecimalField(
        _("Convienance Charges"), decimal_places=2, max_digits=12, default=0)

    tax_config = models.CharField(max_length=255, null=True, blank=True)

    payment_date = models.DateTimeField(
        null=True, blank=True)  # order payment complete
    date_placed = models.DateTimeField(db_index=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    # shipping Address
    email = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Customer Email"))

    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("First Name"))

    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Last Name"))

    country_code = models.CharField(
        max_length=15, null=True, blank=True, verbose_name=_("Country Code"))

    mobile = models.CharField(max_length=15, null=True, blank=True,)
    alt_mobile = models.CharField(
        max_length=15, null=True, blank=True, verbose_name=_("Alternate Mobile"))
    alt_email = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Alternate Email"))

    address = models.CharField(max_length=255, null=True, blank=True)

    pincode = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    # welcome call done or not
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='order_assigned',
        null=True, blank=True)
    wc_cat = models.PositiveIntegerField(
        _("Welcome Call Category"), default=0,
        choices=WC_CATEGORY)
    wc_sub_cat = models.PositiveIntegerField(
        _("Welcome Call Sub-Category"), default=0,
        choices=WC_SUB_CATEGORY)
    wc_status = models.PositiveIntegerField(
        _("Welcome Call Status"), default=0,
        choices=WC_FLOW_STATUS)
    wc_follow_up = models.DateTimeField(null=True, blank=True)
    welcome_call_done = models.BooleanField(default=False)
    welcome_call_records = models.TextField(
        _('Call Recording'), blank=True, null=True)
    midout_sent_on = models.DateTimeField(null=True, blank=True)

    # cash or Faild trasnsaction manual paid by..
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='order_paid_by',
        null=True, blank=True)

    # invoce order
    invoice = models.FileField(
        upload_to=get_upload_path_order_invoice, max_length=255,
        blank=True, null=True)

    # crm information
    crm_sales_id = models.CharField(
        max_length=255, null=True, blank=True)
    crm_lead_id = models.CharField(
        max_length=255, null=True, blank=True)
    sales_user_info = models.TextField(default='', null=True, blank=True)

    # resume writing
    auto_upload = models.BooleanField(default=False)
    service_resume_upload_shine = models.BooleanField(default=True)

    # utm parameters
    utm_params = models.TextField(null=True, blank=True)

    ref_order = models.ForeignKey('self', null=True, default=None,
                                  on_delete=models.SET_NULL)

    class Meta:
        app_label = 'order'
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = (
            # order queue permission
            ("can_show_order_queue", "Can Show Order Queue"),
            ("can_show_all_order", "Can View All Orders"),
            ("can_show_paid_order", "Can View Only Paid Orders"),

            # welcome call permission
            ("can_show_welcome_queue", "Can Show Welcome Queue"),

            # order deatil permissions
            ("can_view_order_detail", "Can View Order Deatil"),

            # order Action permissions
            ("can_mark_order_as_paid", "Can Mark Order As Paid"),

            # order Search permissions
            ("can_search_order_from_console", "Can Search Order From Console"),
        )

    def __str__(self):
        return u"#%s" % (self.number,)

    def order_contains_resume_builder(self):
        items = self.orderitems.all()
        return any([item.product.type_flow == 17 for item in items])

    def order_contains_expert_assistance(self):
        items = self.orderitems.all()
        return any([item.product.sub_type_flow == 101 for item in items])

    def order_contains_neo_item(self):
        items = self.orderitems.all()
        return any([item.product.vendor.slug == 'neo' for item in items])

    def order_contains_analytics_vidhya_item(self):
        items = self.orderitems.all()
        return any([item.product.vendor.slug == 'analytics_vidhya' for item in items])

    def order_contains_amcat_item(self):
        items = self.orderitems.all()
        return any([item.product.vendor.slug == 'amcat' for item in items])

    def order_contains_resumebuilder_subscription(self):
        items = self.orderitems.all()
        return any([item.product.sub_type_flow == 1701 for item in items])

    def order_contains_jobs_on_the_move(self):
        items = self.orderitems.all()
        return any([item.product.sub_type_flow == 502 for item in items])

    def order_contains_shine_premium(self):
        items = self.orderitems.filter(parent=None)
        return any([item.product.type_flow == 18 for item in items])

    def order_contains_profile_booster(self):
        items = self.orderitems.filter(parent=None)
        return any([item.product.type_flow == 19 for item in items])

    def order_contains_resume_writing(self):
        items = self.orderitems.all()
        return any([item.product.type_flow == 1 for item in items])

    def order_contains_course(self):
        items = self.orderitems.all()
        return any([item.product.type_flow == 2 for item in items])

    def update_subscription_in_order_item(self):
        items = self.orderitems.all().select_related('product')
        items = [item for item in items if item.product.sub_type_flow == 1701]
        for oi in items:
            oi.start_date = timezone.now()
            oi.end_date = timezone.now() + timedelta(days=oi.product.day_duration)
            oi.active_on_shine = 1
            update_purchase_on_shine.delay(oi.pk)
            oi.save()

    @property
    def get_status(self):
        statusD = dict(STATUS_CHOICES)
        return statusD.get(self.status)

    @property
    def get_payment_mode(self):
        payD = dict(PAYMENT_MODE)
        return payD.get(self.payment_mode)

    def get_first_touch_for_email(self):
        order_obj = Order.objects.filter(email=self.email).\
            order_by('id').first()
        return order_obj.created

    @property
    def replaced_order(self):
        oi = OrderItem.objects.filter(Q(replacement_order_id=self.id) | Q(
            replacement_order_id=self.number)).first()
        if oi:
            return oi.order.id
        return None

    @property
    def masked_email(self):
        if not self.email:
            return ""
        email = self.email
        return email[:2] + "".join(["*" for i in list(email[2:len(email) - 5])]) + email[-5:]

    @property
    def masked_mobile(self):
        if not self.mobile:
            return ""
        mobile = str(self.mobile)
        return mobile[:2] + "".join(["*" for i in list(mobile[2:len(mobile)-2])]) + mobile[-2:]

    @property
    def masked_altmobile(self):
        if not self.alt_mobile:
            return ""
        mobile = str(self.alt_mobile)
        return mobile[:2] + "".join(["*" for i in list(mobile[2:len(mobile)-2])]) + mobile[-2:]

    @property
    def full_name(self):
        name = ""
        if self.first_name:
            name += self.first_name + " "
        if self.last_name:
            name += self.last_name
        return name

    def get_currency_code(self):
        return CURRENCY_SYMBOL_CODE_MAPPING.get(self.currency)

    def get_past_orders_for_email_and_mobile(self):
        return Order.objects.filter(email=self.email, mobile=self.mobile,
                                    status__in=[1, 2, 3]).exclude(id=self.id)

    def get_txns(self):
        return self.ordertxns.all()

    def get_currency(self):
        currency_dict = dict(CURRENCY_SYMBOL)
        return currency_dict.get(self.currency)

    def get_wc_cat(self):
        sub_dict = dict(WC_CATEGORY)
        return sub_dict.get(self.wc_cat, '')

    def get_email(self):
        if self.alt_email:
            return self.alt_email
        else:
            return self.email

    def get_mobile(self):
        if self.alt_mobile:
            return self.alt_mobile
        else:
            return self.mobile

    def get_wc_sub_cat(self):
        cat_dict = dict(WC_SUB_CATEGORY)
        return cat_dict.get(self.wc_sub_cat, '')

    def get_wc_status(self):
        status_dict = dict(WC_FLOW_STATUS)
        return status_dict.get(self.wc_status, '')

    def follow_up_color(self):
        c_time = timezone.now()
        follow_up = self.wc_follow_up
        if follow_up:
            before_time = follow_up - timedelta(
                minutes=30
            )
            later_time = follow_up + timedelta(
                minutes=60
            )
            if c_time >= before_time and c_time <= later_time:
                return 'pink'
        return ''

    def get_product_name(self):
        product_list = self.orderitems.values_list('product__name',flat=True)

        return " ,".join(product_list)



    def upload_service_resume_shine(self, existing_obj):
        if self.service_resume_upload_shine and self.service_resume_upload_shine != existing_obj.service_resume_upload_shine:
            order_items = self.orderitems.filter(
                oi_status=4, product__type_flow__in=[1, 12, 13, 8, 3, 4])
            for order_item in order_items:
                upload_Resume_shine(order_item.id)

    def get_oi_actual_price_mapping(self):
        amt_dict = {}
        order_items = OrderItem.objects.filter(order=self)
        if not order_items:
            return amt_dict
        coupon_order = CouponOrder.objects.filter(order=self).first()
        coupon_code = coupon_order.coupon_code if coupon_order else ""
        order_discount = sum(
            order_items.values_list('discount_amount', flat=True))
        coupon_objs = Coupon.objects.filter(
            id__in=self.couponorder_set.values_list('coupon', flat=True))
        forced_coupon_amount = 0

        for obj in coupon_objs:
            amount = float(obj.value) if obj.coupon_type == "flat" else \
                float((obj.value * self.total_excl_tax) / 100)
            forced_coupon_amount += amount

        for item in order_items:
            if not item.product:
                continue
            combo_parent = False
            item_selling_price = item.selling_price
            item_cost_price = float(item.cost_price)
            if not item_cost_price:
                item_cost_price = float(item.product.inr_price)
            if item.product.type_product == 0 and item_selling_price == 0 \
                    and not item.is_combo and not item.no_process:
                item_selling_price = float((float(item.product.inr_price) -
                                            forced_coupon_amount)) * 1.18

            item_refund_request_list = RefundItem.objects.filter(oi_id=item.id,
                                                                 refund_request__status__in=[1, 3, 5, 7, 8, 11])
            refund_amount = item_refund_request_list.first().amount \
                if item_refund_request_list else 0

            if item.is_combo and item.parent:
                parent_sum = float(item.parent.cost_price)
                if not parent_sum:
                    # Assuming price remains unchanged
                    parent_sum = float(item.parent.product.inr_price)
                    order_discount = float(forced_coupon_amount)

                actual_sum_of_child_combos = 0
                child_combos = item.order.orderitems.filter(parent=item.parent)

                for child_combo in child_combos:
                    child_cost_price = float(child_combo.cost_price)
                    if not child_cost_price:
                        child_cost_price = float(child_combo.product.inr_price)
                    actual_sum_of_child_combos += child_cost_price

                virtual_decrease_in_price = actual_sum_of_child_combos - parent_sum
                virtual_decrease_part_of_this_item = virtual_decrease_in_price * \
                    (float(
                        item_cost_price) / actual_sum_of_child_combos)
                actual_price_of_item_after_virtual_decrease = float(
                    item_cost_price) - virtual_decrease_part_of_this_item

                if order_discount > 0:
                    combo_discount_amount = (float(order_discount) /
                                             float(self.total_excl_tax)) * \
                        actual_price_of_item_after_virtual_decrease
                    actual_price_of_item_after_virtual_decrease -= combo_discount_amount

                item_selling_price = round(
                    (actual_price_of_item_after_virtual_decrease * 1.18), 2)
                item_refund_request_list = RefundItem.objects.filter(
                    oi_id=item.parent.id,
                    refund_request__status__in=[1, 3, 5, 7, 8, 11])
                total_refund = float(item_refund_request_list.first().amount) \
                    if item_refund_request_list else 0

                if item.parent.selling_price:
                    refund_amount = round(total_refund * (item_selling_price /
                                                          float(item.parent.selling_price)), 2)
                else:
                    refund_amount = 0

            if item.is_combo and not item.parent:
                combo_parent = True
                item_selling_price = 0
                refund_amount = 0

            if item.wc_sub_cat == 65:
                replaced = True
                replacement_id = item.get_replacement_order_id

            total_items = item.order.orderitems.count()
            if total_items == 1 and item_selling_price == 0:
                item_selling_price = float(float(self.total_excl_tax) -
                                           float(forced_coupon_amount)) * 1.18
            if item_selling_price:
                amt_dict.update({item.id: float(item_selling_price) + float(
                    item.delivery_price_incl_tax)})
        return amt_dict

    def save(self, **kwargs):
        created = not bool(getattr(self, "id"))
        if created:
            return super(Order, self).save(**kwargs)
        existing_obj =None
        try:
            existing_obj = Order.objects.get(id=self.id)
        except:
            logging.getLogger('error_log').error('order not in save found checking using master -{}'.format(self.id))
            existing_obj = Order.objects.using('master').get(id=self.id)

        if self.status == 1:
            assesment_items = self.orderitems.filter(
                order__status__in=[0, 1],
                product__type_flow=16,
                product__sub_type_flow=1602,
                autologin_url=None
            )
            manually_generate_autologin_url(assesment_items=assesment_items)
        if self.status == 1 and existing_obj.status != 1 and self.order_contains_neo_item():
            neo_items_id = list(self.orderitems.filter(
                product__vendor__slug='neo',
                no_process=False
            ).values_list('id', flat=True))
            board_user_on_neo.delay(neo_ids=neo_items_id)

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_analytics_vidhya_item():
            av_items_id = list(self.orderitems.filter(
                product__vendor__slug='analytics_vidhya',
                no_process=False
            ).values_list('id', flat=True))
            av_user_enrollment.delay(av_ids=av_items_id)

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_jobs_on_the_move():
            jobs_on_the_move_items = self.orderitems.filter(
                product__sub_type_flow=502)

            for jobs_oi in jobs_on_the_move_items:
                jobs_oi.start_date = timezone.now()
                jobs_oi.end_date = timezone.now() + timedelta(days=jobs_oi.product.day_duration)
                jobs_oi.active_on_shine = 1
                update_purchase_on_shine.delay(jobs_oi.pk)
                jobs_oi.save()

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_amcat_item():
            amcat_items = self.orderitems.filter(
                product__vendor__slug='amcat',
                no_process=False
            )

            for amcat_oi in amcat_items:
                amcat_oi.start_date = timezone.now()
                amcat_oi.end_date = timezone.now() + timedelta(days=15)
                amcat_oi.active_on_shine = 1
                update_purchase_on_shine.delay(amcat_oi.pk)
                amcat_oi.save()

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_resume_builder():
            # imported here to not cause cyclic import for resumebuilder models
            from resumebuilder.models import Candidate

            if self.order_contains_resumebuilder_subscription():

                self.update_subscription_in_order_item()
                cand_id = existing_obj and existing_obj.candidate_id
                if cand_id:
                    candidate_obj = Candidate.objects.filter(
                        candidate_id=cand_id).first()
                    if candidate_obj:
                        candidate_obj.active_subscription = True
                        candidate_obj.save()

            if self.order_contains_expert_assistance():
                cand_id = existing_obj and existing_obj.candidate_id
                if cand_id:
                    candidate_obj = Candidate.objects.filter(
                        candidate_id=cand_id).first()
                    if candidate_obj:
                        candidate_obj.resume_generated = False
                        candidate_obj.save()

            generate_resume_for_order.delay(self.id)

            logging.getLogger('info_log').info(
                "Generating resume for order {}".format(self.id))

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_shine_premium():
            from wallet.models import ProductPoint
            """
            Handle the ProductPoint Flow for shine resume.
            Step 1 - Create a product point with the order id and candidate id.
            Step 2 - check the sub type flow.
            step 3 - Based on sub type decide the validity and count of test & assessments.
            """
            order_item = self.orderitems.filter(
                parent=None, product__type_flow=18).first()
            product_redeem_count = 0
            product_validity_in_days = 0

            if order_item:
                sub_type_flow = order_item.product.sub_type_flow if order_item.product else None

            if sub_type_flow == 1800:
                product_redeem_count = 1
                product_validity_in_days = order_item.product.day_duration
                order_item.start_date = timezone.now()
                order_item.end_date = timezone.now() + timedelta(days=product_validity_in_days)

            elif sub_type_flow == 1801:
                product_redeem_count = 2
                product_validity_in_days = order_item.product.day_duration
                order_item.start_date = timezone.now()
                order_item.end_date = timezone.now() + timedelta(days=product_validity_in_days)
            elif sub_type_flow == 1802:
                product_redeem_count = 3
                product_validity_in_days = order_item.product.day_duration
                order_item.start_date = timezone.now()
                order_item.end_date = timezone.now() + timedelta(days=product_validity_in_days)

            order_item.active_on_shine = 1

            now = datetime.now()
            time_tuple = now.timetuple()
            purchased_at = time.mktime(time_tuple)
            update_purchase_on_shine.delay(order_item.pk)

            # saving this for assessments and practice test
            redeem_options = [{
                'type': 'assessment',
                'product_redeem_count': product_redeem_count,
                'product_validity_in_days': product_validity_in_days,
                'purchased_at': purchased_at
            },
                {
                'type': 'practice_test',
                'product_redeem_count': product_redeem_count,
                'product_validity_in_days': product_validity_in_days,
                'purchased_at': purchased_at
            }]

            product_point, created = ProductPoint.objects.update_or_create(
                candidate_id=self.candidate_id,
                defaults={'order': self,
                          'redeem_options': str(redeem_options),
                          'candidate_id': self.candidate_id,
                          'active': True}
            )
            try:
                product_point.save()
                order_item.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "Could not able to create product points or order item for order {}".format(self.id))

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_profile_booster():
            order_item = self.orderitems.filter(
               parent=None, product__type_flow=19).first()
            order_item.start_date = timezone.now()
            order_item.end_date = timezone.now() + timedelta(days=order_item.product.day_duration)
            order_item.active_on_shine = 1
            update_purchase_on_shine.delay(order_item.pk)
            try:
                order_item.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "Could not able to save order item {}  for order {}".format(order_item.id, self.id))

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_resume_writing():
            order_items = self.orderitems.filter(
                 product__type_flow=1)
            for order_item in order_items:
                order_item.start_date = timezone.now()
                order_item.end_date = timezone.now() + timedelta(days=30)
                order_item.active_on_shine = 1
                update_purchase_on_shine.delay(order_item.pk)
                try:
                    order_item.save()
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "Could not able to save order item {}  for order {}".format(order_item.id, self.id))

        if self.status == 1 and existing_obj.status != 1 and self.order_contains_course():
            order_items = self.orderitems.filter(
                product__type_flow=2)
            for order_item in order_items:
                order_item.start_date = timezone.now()
                order_item.end_date = timezone.now() + timedelta(days=30)
                order_item.active_on_shine = 1
                update_purchase_on_shine.delay(order_item.pk)
                try:
                    order_item.save()
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "Could not able to save order item {}  for order {}".format(order_item.id, self.id))

        self.upload_service_resume_shine(existing_obj)
        obj = super(Order, self).save(**kwargs)

        if self.status == 1:
            bypass_resume_midout(self.id)

        return obj


class OrderItem(AbstractAutoDate):
    coi_id = models.IntegerField(
        _('CP OrderItem'),
        blank=True,
        null=True,
        editable=False)
    archive_json = models.TextField(
        _('Archive JSON'),
        blank=True,
        editable=False
    )

    order = models.ForeignKey(
        'order.Order', related_name='orderitems', verbose_name=_("Order"), on_delete=models.CASCADE)

    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)

    partner = models.ForeignKey(
        'partner.Vendor', related_name='order_items', blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name=_("Partner"))
    partner_name = models.CharField(
        _("Partner name"), max_length=128, blank=True)
    product = models.ForeignKey(
        'shop.Product', on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name=_("Product"))
    title = models.CharField(
        _("Product title"), max_length=255)
    upc = models.CharField(_("UPC"), max_length=128, blank=True, null=True)
    quantity = models.PositiveIntegerField(
        _("Quantity"), default=1)

    delivery_service = models.ForeignKey(
        'shop.DeliveryService',
        related_name='delivery_orderitems',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    delivery_price_incl_tax = models.DecimalField(
        _("Delivery Price (incl. tax excl Discount)"),
        decimal_places=2, max_digits=12, default=0)

    delivery_price_excl_tax = models.DecimalField(
        _("Delivery Price (site price)"),
        decimal_places=2, max_digits=12, default=0)

    # Price information before discounts are applied
    oi_price_before_discounts_incl_tax = models.DecimalField(
        _("Price before discounts (inc. tax)"),
        decimal_places=2, max_digits=12, default=0)
    oi_price_before_discounts_excl_tax = models.DecimalField(
        _("Price before discounts (excl. tax)"),
        decimal_places=2, max_digits=12, default=0)

    # price fields
    cost_price = models.DecimalField(
        _("Price before discounts (Site Price)"),
        decimal_places=2, max_digits=12, default=0)
    selling_price = models.DecimalField(
        _("Selling Price (incl. tax)"),
        decimal_places=2, max_digits=12, default=0)

    tax_amount = models.DecimalField(
        _("tax amount"),
        decimal_places=2, max_digits=12, default=0)

    discount_amount = models.DecimalField(
        _("Total Discount (incl. Wallet)"),
        decimal_places=2, max_digits=12, default=0)

    no_process = models.BooleanField(default=False)
    is_combo = models.BooleanField(default=False)
    is_variation = models.BooleanField(default=False)
    is_addon = models.BooleanField(default=False)

    # counselling form status
    oi_flow_status = models.PositiveSmallIntegerField(
        default=0, choices=OI_LINKEDIN_FLOW_STATUS)
    # operation fields
    oi_status = models.PositiveIntegerField(
        _("Operation Status"), default=0, choices=OI_OPS_STATUS)
    last_oi_status = models.PositiveIntegerField(
        _("Last Operation Status"), default=0, choices=OI_OPS_STATUS)
    oi_resume = models.FileField(
        max_length=255, upload_to='shinelearning/resumes/',
        null=True, blank=True, default='')
    oi_draft = models.FileField(
        max_length=255, upload_to='shinelearning/resumes/', null=True, blank=True)
    draft_counter = models.PositiveIntegerField(default=0)
    tat_date = models.DateTimeField(null=True, blank=True)

    oio_linkedin = models.OneToOneField(
        Draft, null=True, blank=True, on_delete=models.CASCADE)

    waiting_for_input = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned',
        null=True, blank=True)

    assigned_date = models.DateTimeField(
        null=True, blank=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oi_assigned_by',
        null=True, blank=True)

    closed_on = models.DateTimeField(null=True, blank=True)
    draft_added_on = models.DateTimeField(null=True, blank=True)
    approved_on = models.DateTimeField(
        null=True, blank=True)  # draft approved on
    expiry_date = models.DateTimeField(null=True, blank=True)
    user_feedback = models.BooleanField(default=False)
    buy_count_updated = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    # welcome call flow
    wc_cat = models.PositiveIntegerField(
        _("Welcome Call Category"), default=0,
        choices=WC_CATEGORY)
    wc_sub_cat = models.PositiveIntegerField(
        _("Welcome Call Sub-Category"), default=0,
        choices=WC_SUB_CATEGORY)
    wc_status = models.PositiveIntegerField(
        _("Welcome Call Status"), default=0,
        choices=WC_FLOW_STATUS)
    wc_follow_up = models.DateTimeField(null=True, blank=True)

    # replacement_order_id
    replacement_order_id = models.CharField(
        _("Replacement Order number"), null=True, blank=True, max_length=20)

    # autologin url for assesment
    autologin_url = models.CharField(
        _("Auto Login Url"), null=True, blank=True, max_length=2000,
    )

    # field for whatsapp job
    pending_links_count = models.IntegerField(
        blank=True,
        null=True,
        default=0
    )
    active_on_shine = models.PositiveIntegerField(
        _("Active On Shine"), default=0, choices=SHINE_ACTIVATION)
    is_resume_candidate_upload = models.BooleanField(default=False)

    class Meta:
        app_label = 'order'
        # Enforce sorting in order of creation.
        ordering = ['-created']
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        permissions = (
            # midout queue permission
            ("can_show_midout_queue", "Can Show Midout Queue"),
            ("can_upload_candidate_resume", "Can Upload Candidate resume"),

            # inbox permission
            ("can_show_inbox_queue", "Can Show Writer Inbox Queue"),
            ("can_view_extra_field_inbox", "Can View Extra Fields Of Writer Inbox"),
            ("writer_inbox_assigner", "Writer Inbox Assigner"),
            ("writer_inbox_assignee", "Writer Inbox Assignee"),

            # oirder item detail permission
            ("can_view_order_item_detail", "Can View Order Item Detail"),

            # for linkedin flow
            ("writer_assignment_linkedin_action",
             "Can Assign to Other linkedin writer"),
            ("can_assigned_to_linkedin_writer",
             "Can Assigned To This linkedin Writer"),
            ("can_show_linkedinrejectedbyadmin_queue",
             "Can View Linkedin Rejected By Admin Queue"),
            ("can_show_linkedinrejectedbycandidate_queue",
             "Can View LinkedinRejected By Candidate Queue"),
            ("can_show_linkedin_approval_queue",
             "Can View Linkedin Approval Queue"),
            ("can_show_linkedin_approved_queue",
             "Can View Linkedin Approved Queue"),
            ("can_show_linkedin_inbox_queue", "Can View Linkedin Inbox Queue"),
            ("can_show_linkedin_writer_draft", "Can View Linkedin Writer Draft"),
            ("can_show_linkedin_counselling_form",
             "Can View Linkedin Counselling Form"),
            ("can_view_counselling_form_in_approval_queue",
             "Can View Counselling Form In Approval Queue"),

            # Approval Queue
            ("can_show_approval_queue", "Can View Approval Queue"),
            ("can_view_all_approval_list", "Can View All Approval List"),
            ("can_view_only_assigned_approval_list",
             "Can View Only Assigned Approval List"),
            ("can_approve_or_reject_draft", "Can Approve Or Reject Draft"),

            # Appoved Queue
            ("can_show_approved_queue", "Can View Approved Queue"),
            ("can_view_all_approved_list", "Can View All Approved List"),
            ("can_view_only_assigned_approved_list",
             "Can View Only Assigned Approved List"),

            # Rejected By Admin Queue
            ("can_show_rejectedbyadmin_queue", "Can View Rejected By Admin Queue"),
            ("can_view_all_rejectedbyadmin_list",
             "Can View All Rejected by Admin List"),
            ("can_view_only_assigned_rejectedbyadmin_list",
             "Can View Only Assigned Rejected By Admin List"),

            # Rejected By Candidate Queue
            ("can_show_rejectedbycandidate_queue",
             "Can View Rejected By Candidate Queue"),
            ("can_view_all_rejectedbycandidate_list",
             "Can View All Rejected By Candidate List"),
            ("can_view_only_assigned_rejectedbycandidate_list",
             "Can View Only Assigned Rejected By Candidate List"),

            # Allocated Queue
            ("can_show_allocated_queue", "Can Show Allocated Queue"),
            ("can_view_all_allocated_list", "Can View All Allocated List"),
            ("can_view_only_assigned_allocated_list",
             "Can View Only Assigned Allocated List"),

            # Booster Queue
            ("can_show_booster_queue", "Can Show Booster Queue"),

            # Domestic Profile Update Queue Permissions
            ("can_show_domestic_profile_update_queue",
             "Can Show Domestic Profile Update Queue"),
            ("domestic_profile_update_assigner",
             "Domestic Profile Update Assigner"),
            ("domestic_profile_update_assignee",
             "Domestic Profile Update Assignee"),
            ("can_show_domestic_profile_initiated_queue",
             "Can Show Domestic Profile Initiated Queue"),

            # Domestic Profile Approval Queue Permissions
            ("can_show_domestic_profile_approval_queue",
             "Can Show Domestic Profile Approval Queue"),

            # International Profile Update Queue Permissions
            ("can_show_international_profile_update_queue",
             "Can Show International Profile Update Queue"),
            ("international_profile_update_assigner",
             "International Profile Update Assigner"),
            ("international_profile_update_assignee",
             "International Profile Update Assignee"),

            # International Profile Approval Queue Permissions
            ("can_show_international_profile_approval_queue",
             "Can Show International Profile Approval Queue"),

            # Closed Permission
            ("can_show_closed_oi_queue", "Can Show Closed Orderitem Queue"),
            ("can_view_all_closed_oi_list", "Can View All Closed Orderitem List"),
            ("can_view_only_assigned_closed_oi_list",
             "Can View Only Assigned Closed Orderitem List"),

            # partner inbox permission
            ("can_show_partner_inbox_queue", "Can Show Partner Inbox Queue"),
            ("show_test_status_fields", "Show Test Status Field For Studymate"),

            # Hold queue permissions
            ("can_show_hold_orderitem_queue", "Can Show Hold Orderitem Queue"),

            # Varification report queue
            ("can_show_varification_report_queue",
             "Can Show Varification Report Queue"),

            # Action Permission
            ("oi_action_permission", "OrderItem Action Permission"),
            ("oi_export_as_csv_permission", "Order Item Export As CSV Permission"),

            # complaince generation permission
            ("can_generate_compliance_report",
             "can create compliance report permmission"),

            # jobs on the move permission
            ("can_view_assigned_jobs_on_the_move",
             "Can view assigned jobs on the move"),
            ("can_assign_jobs_on_the_move", "Can assign jobs on the move"),
            ("can_send_jobs_on_the_move", "Can send assigned jobs on the move"),
            ("can_approve_jobs_on_the_move", "Can Approve jobs on the move"),
            ("can_update_manual_links", "Can Update Manual Links")
        )

    def __str__(self):
        return "#{}".format(self.pk)

    def service_pause_status(self):
        pause_resume_ops_count = self.orderitemoperation_set.filter(oi_status__in=[
                                                                    34, 35]).count()
        if pause_resume_ops_count & 1 and self.oi_status == 34:
            return False
        return True

    @property
    def get_duration_days(self):
        if self.start_date and self.end_date:
            duration_days = self.end_date - self.start_date
            return duration_days.days
        return self.product.day_duration

    @property
    def days_left_oi_product(self):
        if not self.product:
            return
        can_be_paused = self.product.is_pause_service
        duration_days = self.get_duration_days

        if not self.product or not self.product.is_service:
            return 0

        featured_op = self.orderitemoperation_set.filter(oi_status=28).first()

        if not featured_op:
            return 0
        if not self.start_date:
            sdt = featured_op.created
        else:
            sdt = self.start_date

        if not can_be_paused:
            edt = sdt + timedelta(days=duration_days)
            days_left = edt - timezone.now()
            return days_left.days

        edt = sdt + timedelta(days=duration_days*2)
        pause_resume_operations = self.orderitemoperation_set.filter(
            oi_status__in=[34, 35]).values_list('created', flat=True)
        days_left = timedelta(days=duration_days)
        days_between_pause_resume = timedelta(0)

        for pos in range(0, pause_resume_operations.count(), 2):
            if pos == 0:
                days_between_pause_resume += pause_resume_operations[pos] - sdt
                continue

            days_between_pause_resume += pause_resume_operations[pos] - \
                pause_resume_operations[pos-1]

        # if even no of operations -> the service is resumed
        if (not pause_resume_operations.count() & 1) and pause_resume_operations.count() > 0:
            days_between_pause_resume += timezone.now() - pause_resume_operations.last()
        elif pause_resume_operations.count() == 0:
            days_left -= (timezone.now() - sdt)

        days_left -= (days_between_pause_resume)

        if (edt - timezone.now()) < days_left:
            days_left = (edt - timezone.now())

        return days_left.days

    @property
    def order_payment_date(self):
        payment_date = self.order.payment_date.date()
        return payment_date

    @property
    def assigned_to_name(self):
        if self.assigned_to:
            return getattr(self.assigned_to, 'name', 'N.A')
        return 'N.A'

    @property
    def product_name(self):
        return self.product.get_name if self.product else ''

    @property
    def order_status_text(self):
        return dict(STATUS_CHOICES).get(self.order.status)

    @property
    def get_oi_status(self):
        if self.oi_status in [28, 29, 30]:
            return self.oi_status_transform()
        dict_status = dict(OI_OPS_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def get_user_oi_status(self):
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def get_replacement_order_id(self):
        if self.replacement_order_id:
            replacement_order_id = self.replacement_order_id.upper()
            if 'CP' in replacement_order_id:
                return replacement_order_id.replace('CP', '')
            return self.replacement_order_id

    @property
    def is_approved(self):
        if self.product.sub_type_flow == 502:
            profile = getattr(self, 'whatsapp_profile_orderitem', None)
            if profile:
                return profile.approved

    @property
    def has_due_date(self):
        if self.product.sub_type_flow == 502:
            profile = getattr(self, 'whatsapp_profile_orderitem', None)
            if profile:
                return bool(profile.due_date)

    @property
    def oi_draft_path(self):
        return str(self.oi_draft.url) if self.oi_draft else ""

    @property
    def is_onboard(self):
        if self.product.sub_type_flow == 502:
            profile = getattr(self, 'whatsapp_profile_orderitem', None)
            if profile:
                return profile.onboard

    def get_item_operations(self):
        if self.product.sub_type_flow == 502:
            ops = []
            start_op = self.orderitemoperation_set.filter(
                oi_status__in=[31, 32, 5]).order_by('id').first()
            ops.append(start_op)
            closed_op = self.orderitemoperation_set.filter(
                oi_status=4).order_by('id').first()
            if closed_op:
                start_op = ops.append(closed_op)

            return ops

    @property
    def sent_link_count(self):
        manual_links_count = self.get_manual_sent_link()
        return self.jobs_link.filter(status=2).count() + manual_links_count

    @property
    def is_closed(self):
        if self.oi_status == 4:
            return True

    @property
    def neo_mail_sent(self):
        sent = cache.get('neo_mail_sent_{}'.format(self.id))
        return sent

    @property
    def updated_from_trial_to_regular(self):
        return cache.get('updated_from_trial_to_regular_{}'.format(self.id))

    def get_due_date(self):
        profile = getattr(self, 'whatsapp_profile_orderitem', None)
        if profile and profile.due_date:
            temp_due_date = profile.due_date
            temp_due_date_extended_by = 0
            holiday_list = GazettedHoliday().get_holiday_list
            while (temp_due_date.weekday() == 6 or temp_due_date.strftime('%d-%m-%Y') in holiday_list):
                temp_due_date_extended_by += 1
                temp_due_date += relativedelta.relativedelta(days=1)
            if temp_due_date_extended_by:
                profile.due_date_extended_by += temp_due_date_extended_by
                profile.due_date += relativedelta.relativedelta(
                    days=profile.due_date_extended_by)
                profile.save()
            return profile.due_date.strftime('%d-%m-%Y')
        return 'N.A'

    def get_due_date_weekday(self):
        profile = getattr(self, 'whatsapp_profile_orderitem', None)
        if profile and profile.due_date:
            return DAYS_CHOICES_DICT.get(profile.due_date.weekday())
        return 'N.A'

    def get_weeks(self):
        weeks, weeks_till_now = None, None
        sevice_started_op = self.orderitemoperation_set.all().filter(
            oi_status__in=[31]).order_by('id').first()
        if sevice_started_op:
            started = sevice_started_op.created
            day = self.product.get_duration_in_day()
            weeks = math.floor(day / 7)
            today = timezone.now()
            weeks_till_now = ((today - started).days) // 7
            weeks_till_now += 1

        return weeks, weeks_till_now

    def get_links_needed_till_now(self):
        start, end = None, None
        links_count = 0
        sevice_started_op = self.orderitemoperation_set.all().filter(
            oi_status__in=[31]).order_by('id').first()
        links_per_week = getattr(self.product.attr, S_ATTR_DICT.get('LC'), 2)
        if sevice_started_op:
            links_count = 0
            started = sevice_started_op.created
            day = self.product.get_duration_in_day()
            weeks = math.floor(day / 7)
            today = timezone.now()
            for i in range(0, weeks):
                start = started + relativedelta.relativedelta(days=i * 7)
                start = start + timedelta(hours=12)
                if start > today:
                    break
                links_count += links_per_week
        return links_count

    def get_manual_sent_link(self):
        manual_change = None
        profile = getattr(self, 'whatsapp_profile_orderitem', None)
        if profile:
            if profile.manual_change == 1:
                manual_changes_data = eval(profile.manual_changes_data) if \
                    profile.manual_changes_data else {}
                already_sent_link = manual_changes_data.get(
                    'already_sent_link', 0)
                return already_sent_link
        return 0

    def has_saved_links(self):
        saved_links = self.jobs_link.filter(status=0)
        return saved_links.count()

    def get_total_links_needs_to_sent(self):
        day = self.product.get_duration_in_day()
        links_per_week = getattr(self.product.attr, S_ATTR_DICT.get('LC'), 2)
        if day:
            weeks = math.floor(day / 7)
            return weeks * links_per_week
        return None

    def get_sent_link_count_for_current_week(self):
        sevice_started_op = self.orderitemoperation_set.all().filter(
            oi_status__in=[31]).order_by('id').first()
        started = sevice_started_op.created
        day = self.product.get_duration_in_day()
        weeks = math.floor(day / 7)
        today = timezone.now()
        # Here we compute start date and end date for this week
        # for this order item
        for i in range(0, weeks):
            start = started + relativedelta.relativedelta(days=i * 7)
            end = started + relativedelta.relativedelta(days=(i + 1) * 7)
            if end > today:
                break
        links = self.jobs_link.filter(status=2, sent_date__range=[start, end])

        return links.count()

    def update_pending_links_count(self):
        links_needed_till_now = self.get_links_needed_till_now()
        links_sent_till_now = self.sent_link_count
        links_pending = links_needed_till_now - links_sent_till_now
        self.pending_links_count = links_pending
        if self.pending_links_count < 0:
            self.pending_links_count = 0
        self.save()

    def set_due_date(self):
        today = timezone.now()
        profile = getattr(self, 'whatsapp_profile_orderitem', None)

        if profile:
            if profile.due_date and profile.due_date > today:
                profile.due_date = profile.due_date + \
                    relativedelta.relativedelta(
                        days=(7 - profile.due_date_extended_by))
                profile.due_date_extended_by = 0
                profile.save()
            else:
                day_of_week = profile.day_of_week
                if today.weekday() == day_of_week:
                    profile.due_date = today + \
                        relativedelta.relativedelta(
                            days=(7 - profile.due_date_extended_by))
                    profile.due_date_extended_by = 0
                elif today.weekday() > day_of_week:
                    profile.due_date = today +\
                        relativedelta.relativedelta(
                            days=(7 - (today.weekday() - day_of_week) - profile.due_date_extended_by))
                    profile.due_date_extended_by = 0
                elif today.weekday() < day_of_week:
                    profile.due_date = today +\
                        relativedelta.relativedelta(
                            days=(day_of_week - today.weekday()) - profile.due_date_extended_by)
                    profile.due_date_extended_by = 0
                profile.save()

    def get_oi_communications(self):
        communications = self.message_set.all().select_related('added_by')
        return list(communications)

    def get_oi_operations(self):
        operations = self.orderitemoperation_set.all().select_related(
            'added_by', 'assigned_to')
        return list(operations)

    def get_oi_drafts(self):
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        drafts = self.orderitemoperation_set.filter(
            draft_counter__range=[1, max_limit_draft])
        return list(drafts)

    def get_draft_level(self):
        if self.draft_counter == settings.DRAFT_MAX_LIMIT:
            return 'Final Draft'
        elif self.draft_counter:
            return 'Draft %s' % (self.draft_counter)
        return ''

    def get_roundone_status(self):
        if self.oi_status == 142:
            pass
        elif self.oi_status not in [141, 142, 143]:
            pass
        return self.oi_status

    def get_test_obj(self):
        return self

    def get_refund_amount(self):
        refund_amount = Decimal(0)
        refund_amount += self.selling_price
        refund_amount += self.delivery_price_incl_tax
        return refund_amount

    def get_wc_cat(self):
        sub_dict = dict(WC_CATEGORY)
        return sub_dict.get(self.wc_cat, '')

    def get_wc_sub_cat(self):
        cat_dict = dict(WC_SUB_CATEGORY)
        if self.is_combo and self.parent:
            return cat_dict.get(self.parent.wc_sub_cat, '')
        return cat_dict.get(self.wc_sub_cat, '')

    def get_wc_status(self):
        status_dict = dict(WC_FLOW_STATUS)
        return status_dict.get(self.wc_status, '')

    def get_assigned_operation_date(self):
        assigned_op = self.orderitemoperation_set.filter(oi_status=1).first()
        if assigned_op:
            return assigned_op.created

    def oi_status_transform(self):
        if self.product:
            val = OI_OPS_TRANSFORMATION_DICT.get(self.product.sub_type_flow, {})\
                .get(self.oi_status, None)
        else:
            val = None
        if val:
            return val
        else:
            dict_status = dict(OI_OPS_STATUS)
            return dict_status.get(self.oi_status)

    def upload_service_resume_shine(self, existing_obj):
        if self.oi_status == 4 and self.oi_status != existing_obj.oi_status and self.order.service_resume_upload_shine:
            upload_Resume_shine.delay(self.id)

    def update_pause_resume_service(self, existing_obj):
        if not self.oi_status in [34, 35]:
            return
        feature_util = FeatureProfileUtil()

        # if pause or resume fails then return oi_status to previous position
        if not feature_util.pause_resume_feature(existing_obj, self.service_pause_status):
            self.oi_status = existing_obj.oi_status
            return

        self.last_oi_status = existing_obj.oi_status
        self.orderitemoperation_set.create(
            oi_status=self.oi_status,
            last_oi_status=existing_obj.oi_status,
            assigned_to=self.assigned_to)

    def is_assigned(self):
        assigned_operations = self.orderitemoperation_set.filter(oi_status=1)
        return True if len(assigned_operations) else False

    def save(self, *args, **kwargs):
        created = not bool(getattr(self, "id"))
        orderitem = OrderItem.objects.filter(id=self.pk).first()
        self.oi_status = 4 if orderitem and orderitem.oi_status == 4 else self.oi_status
        # handling combo case getting parent and updating child
        self.update_pause_resume_service(orderitem)
        # Call the "real" save() method.
        obj = super(OrderItem, self).save(*args, **kwargs)
        self.upload_service_resume_shine(orderitem)

        return obj

        # # for resume booster create orderitem
        # if self.product.type_flow in [7, 15] and obj.oi_status != last_oi_status:
        #     if obj.oi_status == 5:
        #         self.orderitemoperation_set.create(
        #
        # oi_draft=self.oi_draft,
        #             draft_counter=self.draft_counter,
        #             oi_status=self.oi_status,
        #             last_oi_status=self.last_oi_status,
        #             assigned_to=self.assigned_to,
        #         )
        #     else:
        #         self.orderitemoperation_set.create(
        #             oi_status=self.oi_status,
        #             last_oi_status=last_oi_status,
        #             assigned_to=self.assigned_to,
        #         )
        #     email_sets = list(self.emailorderitemoperation_set.all().values_list(
        #         'email_oi_status', flat=True))
        #     to_emails = [self.order.get_email()]
        #     candidate_data = {
        #         "email": self.order.get_email(),
        #         "mobile": self.order.get_mobile(),
        #         'subject': 'Your resume has been shared with relevant consultants',
        #         "username": self.order.first_name,
        #     }
        #     if obj.oi_status == 4:
        #         from emailers.tasks import send_email_task
        #         from emailers.sms import SendSMS
        #         # send mail to candidate
        #         if email_sets.count(93) <= 2:
        #             mail_type = 'BOOSTER_CANDIDATE'
        #             send_email_task.delay(
        #                 to_emails, mail_type, candidate_data,
        #                 status=93, oi=self.pk)

        #             # send sms to candidate
        #             SendSMS().send(
        #                 sms_type="BOOSTER_CANDIDATE", data=candidate_data)
        #         self.emailorderitemoperation_set.create(email_oi_status=92)

    @classmethod
    def post_save_product(cls, sender, instance, **kwargs):
        # automate application highlighter/priority applicant

        if instance.is_combo and not instance.parent:
            jobs_on_the_move_item = instance.order.orderitems.filter(
                product__sub_type_flow=502)
            priority_applicant_items = instance.order.orderitems.filter(
                product__sub_type_flow=503)
            top_applicant_items = instance.order.orderitems.filter(
                product__sub_type_flow=504)

            for i in jobs_on_the_move_item:
                from order.tasks import process_jobs_on_the_move
                process_jobs_on_the_move.delay(i.id)

            for i in priority_applicant_items:
                process_application_highlighter(i)

            for i in top_applicant_items:
                process_application_highlighter(i)

        elif instance.product.sub_type_flow == 502:
            from order.tasks import process_jobs_on_the_move
            process_jobs_on_the_move.delay(instance.id)

        if instance.product.sub_type_flow in [503, 504]:
            process_application_highlighter(obj=instance)


post_save.connect(OrderItem.post_save_product, sender=OrderItem)


class OrderItemOperation(AbstractAutoDate):
    coio_id = models.IntegerField(
        _('CP Order IO'),
        blank=True,
        null=True,
        editable=False)

    oi = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    linkedin = models.ForeignKey(
        Draft, null=True, blank=True, on_delete=models.CASCADE)
    oi_resume = models.FileField(
        max_length=255, upload_to='shinelearning/resumes/', null=True, blank=True)

    oi_draft = models.FileField(
        max_length=255, upload_to='shinelearning/resumes/', null=True, blank=True)
    draft_counter = models.PositiveIntegerField(default=0)
    oi_status = models.PositiveIntegerField(
        _("Operation Status"), default=0, choices=OI_OPS_STATUS)
    last_oi_status = models.PositiveIntegerField(
        _("Last Operation Status"), default=0, choices=OI_OPS_STATUS)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oio_assigned',
        null=True, blank=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='oio_added_by',
        null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "#{}".format(self.pk)

    @property
    def oi_status_display(self):
        return self.get_oi_status

    @property
    def get_oi_status(self):
        if self.oi_status in [28, 29, 30]:
            return self.oi_status_transform()
        dict_status = dict(OI_OPS_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def order_oio_linkedin(self):
        oi = self.oi
        return oi.oio_linkedin.id if oi.oio_linkedin else ""

    @property
    def get_user_oi_status(self):
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)

    def oi_status_transform(self):
        val = OI_OPS_TRANSFORMATION_DICT.get(self.oi.product.sub_type_flow, {})\
            .get(self.oi_status, None)
        if val:
            return val
        else:
            dict_status = dict(OI_OPS_STATUS)
            return dict_status.get(self.oi_status)


class Message(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem, null=True, on_delete=models.CASCADE)
    oio = models.ForeignKey(
        OrderItemOperation, null=True, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='message_added_by',
        null=True, blank=True)

    candidate_id = models.CharField(max_length=255, null=True, blank=False)

    message = models.TextField()

    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "#{}".format(self.pk)

    @property
    def added_by_name(self):
        if self.added_by:
            return self.added_by.name
        order = self.oi.order
        return order.first_name


class InternationalProfileCredential(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    username = models.CharField(_('Username'), max_length=100)
    password = models.CharField(
        _('Password'), max_length=100, null=True, blank=True)
    candidateid = models.CharField(
        _('CandidateId'), max_length=100, null=True, blank=True)
    candidate_email = models.CharField(_('Candidate Email'), max_length=100)
    site_url = models.CharField(
        _('Site Url'), max_length=100, null=True, blank=True)
    profile_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailOrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    email_oi_status = models.PositiveIntegerField(
        _("Email Operation Status"), default=0, choices=OI_EMAIL_STATUS)
    draft_counter = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    to_email = models.CharField(
        _('To Email'), max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{}-{}'.format(str(self.oi), self.to_email)


class SmsOrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    sms_oi_status = models.PositiveIntegerField(
        _("SMS Operation Status"), default=0, choices=OI_SMS_STATUS)
    draft_counter = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    to_mobile = models.CharField(max_length=15, null=True, blank=True,)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{} - {}".format(self.oi, self.to_mobile)


class CouponOrder(AbstractAutoDate):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        'coupon.Coupon',
        on_delete=models.SET_NULL,
        verbose_name=_("Coupon"), null=True)

    coupon_code = models.CharField(
        _("Coupon Code"), max_length=30, blank=True, null=True)

    value = models.DecimalField(
        _("Value"), max_digits=8, decimal_places=2, default=0.0)


class RefundRequest(AbstractAutoDate):
    order = models.ForeignKey(
        'order.Order', verbose_name=_("Order"), on_delete=models.CASCADE)

    message = models.TextField()

    document = models.FileField(
        max_length=255, upload_to='refund/refund_request/',
        null=True, blank=True)

    status = models.PositiveIntegerField(
        _("Status"), default=0, choices=REFUND_OPS_STATUS)
    last_status = models.PositiveIntegerField(
        _("Last Status"), default=0, choices=REFUND_OPS_STATUS)

    refund_mode = models.CharField(
        max_length=255, default='select',
        choices=REFUND_MODE)
    currency = models.PositiveIntegerField(
        _("Currency"), choices=CURRENCY_SYMBOL, default=0)
    refund_amount = models.DecimalField(
        _("Refund Amount (incl. tax)"),
        decimal_places=2, max_digits=12, default=0)
    txn_no = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(
            'transaction no. in case of neft and serial no. in case cheque/dd'))
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='refund_request_added_by',
        null=True, blank=True)

    refund_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'order'
        ordering = ('-modified', )
        permissions = (
            ("can_view_refund_request_queue", "Can View Refund Request Queue"),
            ("can_view_refund_approval_queue", "Can View Refund Approval Queue"),
        )

    def __str__(self):
        return 'Order number %s and request id %s' % (
            self.order.number, self.id)

    def get_status(self):
        status_dict = dict(REFUND_OPS_STATUS)
        return status_dict.get(self.status)

    def get_currency(self):
        currency_dict = dict(CURRENCY_SYMBOL)
        return currency_dict.get(self.currency)


class RefundItem(AbstractAutoDate):
    refund_request = models.ForeignKey(
        'order.RefundRequest', on_delete=models.CASCADE)
    oi = models.ForeignKey(
        'order.OrderItem', on_delete=models.SET_NULL,
        related_name='refund_items',
        null=True, blank=True)
    type_refund = models.CharField(
        max_length=255, default='select',
        choices=TYPE_REFUND)
    amount = models.DecimalField(
        _("Amount (incl. tax)"),
        decimal_places=2, max_digits=12, default=0)

    def get_type_refund(self):
        type_refund_dict = dict(TYPE_REFUND)
        return type_refund_dict.get(self.type_refund)


class RefundOperation(AbstractAutoDate):
    refund_request = models.ForeignKey(RefundRequest, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(
        _("Status"), default=0, choices=REFUND_OPS_STATUS)
    last_status = models.PositiveIntegerField(
        _("Last Status"), default=0, choices=REFUND_OPS_STATUS)

    message = models.TextField()

    document = models.FileField(
        max_length=255, upload_to='refund/refund_ops/', null=True, blank=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='refund_ops_added_by',
        null=True, blank=True)

    def get_status(self):
        statusD = dict(REFUND_OPS_STATUS)
        return statusD.get(self.status)

    def get_last_status(self):
        statusD = dict(REFUND_OPS_STATUS)
        return statusD.get(self.last_status)


class WelcomeCallOperation(AbstractAutoDate):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    wc_cat = models.PositiveIntegerField(
        _("Welcome Call Category"), default=0,
        choices=WC_CATEGORY)
    wc_sub_cat = models.PositiveIntegerField(
        _("Welcome Call Sub-Category"), default=0,
        choices=WC_SUB_CATEGORY)
    wc_status = models.PositiveIntegerField(
        _("Welcome Call Status"), default=0,
        choices=WC_FLOW_STATUS)
    wc_follow_up = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='wcall_assigned',
        null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='wop_created_by',
        verbose_name=_("Created By"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def get_wc_cat(self, default_text=""):
        sub_dict = dict(WC_CATEGORY)
        return sub_dict.get(self.wc_cat, default_text)

    def get_wc_sub_cat(self, default_text=""):
        cat_dict = dict(WC_SUB_CATEGORY)
        return cat_dict.get(self.wc_sub_cat, default_text)

    def get_wc_status(self, default_text=""):
        status_dict = dict(WC_FLOW_STATUS)
        return status_dict.get(self.wc_status, default_text)


class CustomerFeedback(models.Model):
    candidate_id = models.CharField('Candidate Id', max_length=100)
    full_name = models.CharField(
        'Full Name', max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=15, null=True, blank=True,)
    email = models.CharField(
        'Full Name', max_length=255, blank=True, null=True)
    added_on = models.DateTimeField(editable=False, auto_now_add=True)
    status = models.SmallIntegerField(choices=FEEDBACK_STATUS, default=1)
    assigned_to = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    follow_up_date = models.DateTimeField(
        'Follow Up Date', blank=True, null=True)
    comment = models.TextField('Feedback Comment', blank=True, null=True)
    last_payment_date = models.DateTimeField(
        'Last Payment Date', blank=True, null=True)
    ltv = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    category = models.SmallIntegerField(
        choices=FEEDBACK_CATEGORY_CHOICES, blank=True, null=True)
    resolution = models.SmallIntegerField(
        choices=FEEDBACK_RESOLUTION_CHOICES, blank=True, null=True)

    @property
    def status_text(self):
        return dict(FEEDBACK_STATUS).get(self.status)

    @property
    def assigned_to_text(self):
        return self.assigned_to.name if self.assigned_to else ''

    @property
    def category_text(self):
        return dict(FEEDBACK_CATEGORY_CHOICES).get(self.category)

    @property
    def resolution_text(self):
        return dict(FEEDBACK_RESOLUTION_CHOICES).get(self.resolution)

    def create_operation(self):
        prev_feedback = CustomerFeedback.objects.get(id=self.id)
        if prev_feedback.comment != self.comment:
            OrderItemFeedbackOperation.objects.create(comment=self.comment, customer_feedback=self,
                                                      assigned_to=self.assigned_to, oi_type=2)

        if not prev_feedback.assigned_to and self.assigned_to:
            OrderItemFeedbackOperation.objects.create(
                customer_feedback=self, assigned_to=self.assigned_to, oi_type=3)
        elif prev_feedback.assigned_to != self.assigned_to:
            OrderItemFeedbackOperation.objects.create(
                customer_feedback=self, assigned_to=self.assigned_to, oi_type=4)

        if prev_feedback.follow_up_date != self.follow_up_date:
            OrderItemFeedbackOperation.objects.create(
                customer_feedback=self, assigned_to=self.assigned_to, oi_type=5, follow_up_date=self.follow_up_date)

        if prev_feedback.category != self.category:
            OrderItemFeedbackOperation.objects.create(
                customer_feedback=self, assigned_to=self.assigned_to, oi_type=6, category=self.category)

        if prev_feedback.category != self.category:
            OrderItemFeedbackOperation.objects.create(
                customer_feedback=self, assigned_to=self.assigned_to, oi_type=7, resolution=self.resolution)

    def save(self, *args, **kwargs):
        created = not bool(self.id)
        if not created:
            self.create_operation()

        super(CustomerFeedback, self).save(*args, **kwargs)


class OrderItemFeedback(models.Model):
    category = models.SmallIntegerField(
        choices=FEEDBACK_CATEGORY_CHOICES, blank=True, null=True)
    resolution = models.SmallIntegerField(
        choices=FEEDBACK_RESOLUTION_CHOICES, blank=True, null=True)
    comment = models.TextField('Feedback Comment', blank=True, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    customer_feedback = models.ForeignKey(
        CustomerFeedback, on_delete=models.CASCADE)
    created = models.DateTimeField(
        editable=False, auto_now_add=True, null=True)

    @property
    def category_text(self):
        return dict(FEEDBACK_CATEGORY_CHOICES).get(self.category)

    @property
    def resolution_text(self):
        return dict(FEEDBACK_RESOLUTION_CHOICES).get(self.resolution)

    def save(self, *args, **kwargs):
        create = not bool(self.id)
        if not create:
            assigned_to = CustomerFeedback.objects.get(
                id=self.customer_feedback.id).assigned_to
            prev_data = OrderItemFeedback.objects.get(id=self.id)
            compare_list = [self.category == prev_data.category, self.resolution ==
                            prev_data.resolution, self.comment == prev_data.comment]
            if not all(compare_list):
                OrderItemFeedbackOperation.objects.create(category=self.category, resolution=self.resolution, comment=self.comment,
                                                          order_item=self.order_item, customer_feedback=self.customer_feedback, assigned_to=assigned_to, oi_type=1)
        super(OrderItemFeedback, self).save(
            *args, **kwargs)  # Call the real save() method


class OrderItemFeedbackOperation(models.Model):
    assigned_to = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    added_on = models.DateTimeField(editable=False, auto_now_add=True)
    category = models.SmallIntegerField(
        choices=FEEDBACK_CATEGORY_CHOICES, blank=True, null=True)
    resolution = models.SmallIntegerField(
        choices=FEEDBACK_RESOLUTION_CHOICES, blank=True, null=True)
    comment = models.TextField('Feedback Comment', blank=True, null=True)
    order_item = models.ForeignKey(
        OrderItem, blank=True, null=True, on_delete=models.CASCADE)
    customer_feedback = models.ForeignKey(
        CustomerFeedback, on_delete=models.CASCADE)
    oi_type = models.SmallIntegerField(
        choices=TOTAL_FEEDBACK_OPERATION_TYPE, default=-1)
    feedback_category = models.SmallIntegerField(
        choices=FEEDBACK_CATEGORY_CHOICES, default=-1)
    feedback_resolution = models.SmallIntegerField(
        choices=FEEDBACK_RESOLUTION_CHOICES, default=-1)
    follow_up_date = models.DateTimeField(
        'Follow Up Date', blank=True, null=True)

    @property
    def category_text(self):
        return dict(FEEDBACK_CATEGORY_CHOICES).get(self.category)

    @property
    def resolution_text(self):
        return dict(FEEDBACK_RESOLUTION_CHOICES).get(self.resolution)

    @property
    def assigned_to_text(self):
        return self.assigned_to.name if self.assigned_to else ''

    @property
    def oi_type_text(self):
        return dict(TOTAL_FEEDBACK_OPERATION_TYPE).get(self.oi_type)

    @property
    def feedback_category_text(self):
        return dict(FEEDBACK_CATEGORY_CHOICES).get(self.feedback_category)

    @property
    def feedback_resolution_text(self):
        return dict(FEEDBACK_RESOLUTION_CHOICES).get(self.feedback_resolution)

    def feedback_status_text(self):
        return dict(FEEDBACK_STATUS).get(self.feedback_status)


class LTVMonthlyRecord(models.Model):
    ltv_bracket = models.SmallIntegerField(choices=LTV_BRACKET_LABELS)
    total_users = models.IntegerField()
    crm_users = models.IntegerField(default=0)
    learning_users = models.IntegerField(default=0)
    total_order_count = models.IntegerField()
    total_item_count = models.IntegerField()
    crm_order_count = models.IntegerField()
    crm_item_count = models.IntegerField()
    learning_order_count = models.IntegerField()
    learning_item_count = models.IntegerField()
    year = models.IntegerField(validators=[MinValueValidator(2018)])
    month = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)])
    candidate_id_ltv_mapping = models.TextField()

    @property
    def ltv_bracket_text(self):
        return dict(LTV_BRACKET_LABELS).get(self.ltv_bracket)


class MonthlyLTVRecord(models.Model):
    ltv_bracket = models.SmallIntegerField(choices=LTV_BRACKET_LABELS)
    crm_order_ids = models.TextField()
    learning_order_ids = models.TextField()
    # no process,free,combo parent,variation parent to be removed so query will take time
    crm_item_count = models.IntegerField()
    # no process,free,combo parent,variation parent to be removed so query will take time
    learning_item_count = models.IntegerField()
    year = models.IntegerField(validators=[MinValueValidator(2018)])
    month = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)])
    revenue = models.IntegerField(default=0)
    candidate_ids = models.TextField()

    @property
    def ltv_bracket_text(self):
        return dict(LTV_BRACKET_LABELS).get(self.ltv_bracket)

    @property
    def total_users(self):
        return len(json.loads(self.candidate_ids))

    @property
    def crm_users(self):
        candidates = Order.objects.filter(id__in=json.loads(
            self.crm_order_ids)).values_list('candidate_id', flat=True)
        return len({candidate for candidate in candidates})

    @property
    def crm_order_count(self):
        return len(json.loads(self.crm_order_ids))

    @property
    def learning_users(self):
        candidates = Order.objects.filter(id__in=json.loads(
            self.learning_order_ids)).values_list('candidate_id', flat=True)
        return len({candidate for candidate in candidates})

    @property
    def learning_order_count(self):
        return len(json.loads(self.learning_order_ids))

    @property
    def total_order_count(self):
        return len(json.loads(self.crm_order_ids)) + len(json.loads(self.learning_order_ids))

    @property
    def total_item_count(self):
        return self.crm_item_count + self.learning_item_count

    @property
    def revenue(self):
        order_ids = json.loads(self.crm_order_ids) + \
            json.loads(self.learning_order_ids)
        order_amounts = Order.objects.filter(
            id__in=order_ids).values_list('total_excl_tax', flat=True)
        return sum(order_amounts)


class AnalyticsVidhyaRecord(AbstractAutoDate):
    '''
    saving data for analytics vidhya
    '''
    AV_Id = models.CharField(max_length=255, blank=False,
                             null=False, unique=True)
    order_item = models.ForeignKey(
        'order.OrderItem', related_name='av_orders', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=AV_STATUS_CHOICES, default=0)
    status_msg = models.CharField(
        _("status message"), max_length=100)
    remarks = models.TextField(
        _("remarks"), null=True, blank=True)

    def __str__(self):
        return self.AV_Id
