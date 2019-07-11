#python imports
import math
import datetime,logging

from decimal import Decimal
from dateutil import relativedelta

#django imports
from django.db import models
from django.db.models import Q, Count, Case, When, IntegerField

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone

#local imports
from .choices import STATUS_CHOICES, SITE_CHOICES,\
    PAYMENT_MODE, OI_OPS_STATUS, OI_LINKEDIN_FLOW_STATUS,\
    OI_USER_STATUS, OI_EMAIL_STATUS, REFUND_MODE, REFUND_OPS_STATUS,\
    TYPE_REFUND, OI_SMS_STATUS, WC_CATEGORY, WC_SUB_CATEGORY,\
    WC_FLOW_STATUS

from .functions import get_upload_path_order_invoice, process_application_highlighter
from .tasks import generate_resume_for_order

#inter app imports
from linkedin.models import Draft
from seo.models import AbstractAutoDate
from geolocation.models import Country, CURRENCY_SYMBOL

#third party imports
from payment.utils import manually_generate_autologin_url
from shop.choices import S_ATTR_DICT

#Global Constants
CURRENCY_SYMBOL_CODE_MAPPING = {0:"INR",1:"USD",2:"AED",3:"GBP"}

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

    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES)

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

    payment_date = models.DateTimeField(null=True, blank=True)  # order payment complete
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
    alt_mobile = models.CharField(max_length=15, null=True, blank=True,verbose_name=_("Alternate Mobile"))
    alt_email = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Alternate Email"))

    address = models.CharField(max_length=255, null=True, blank=True)

    pincode = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    country = models.ForeignKey(Country, null=True)

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
    welcome_call_records = models.TextField(_('Call Recording'),blank=True,null=True)
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
        oi = OrderItem.objects.filter(Q(replacement_order_id=self.id) | Q(replacement_order_id=self.number)).first()
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

    def get_currency_code(self):
        return CURRENCY_SYMBOL_CODE_MAPPING.get(self.currency)

    def get_past_orders_for_email_and_mobile(self):
        return Order.objects.filter(email=self.email,mobile=self.mobile,\
            status__in=[1,2,3]).exclude(id=self.id)

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
            before_time = follow_up - datetime.timedelta(
                minutes=30
            )
            later_time = follow_up + datetime.timedelta(
                minutes=60
            )
            if c_time >= before_time and c_time <= later_time:
                return 'pink'
        return ''

    def save(self,**kwargs):
        created = not bool(getattr(self,"id"))
        if created:
            return super(Order,self).save(**kwargs)

        existing_obj = Order.objects.get(id=self.id)
        
        if self.status == 1:
            assesment_items = self.orderitems.filter(
                order__status__in=[0, 1],
                product__type_flow=16,
                product__sub_type_flow=1602,
                autologin_url=None
            )
            manually_generate_autologin_url(assesment_items=assesment_items)
        
        if self.status == 1 and existing_obj.status != 1 and self.order_contains_resume_builder():
            generate_resume_for_order.delay(self.id)
            logging.getLogger('info_log').info("Generating resume for order {}".format(self.id))

        return super(Order,self).save(**kwargs)


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
        'order.Order', related_name='orderitems', verbose_name=_("Order"))

    parent = models.ForeignKey('self', null=True, blank=True)

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

    oio_linkedin = models.OneToOneField(Draft, null=True, blank=True)

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
    approved_on = models.DateTimeField(null=True, blank=True)  # draft approved on
    expiry_date = models.DateTimeField(null=True, blank=True)
    user_feedback = models.BooleanField(default=False)
    buy_count_updated = models.BooleanField(default=False)

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
            ("writer_assignment_linkedin_action", "Can Assign to Other linkedin writer"),
            ("can_assigned_to_linkedin_writer", "Can Assigned To This linkedin Writer"),
            ("can_show_linkedinrejectedbyadmin_queue", "Can View Linkedin Rejected By Admin Queue"),
            ("can_show_linkedinrejectedbycandidate_queue", "Can View LinkedinRejected By Candidate Queue"),
            ("can_show_linkedin_approval_queue", "Can View Linkedin Approval Queue"),
            ("can_show_linkedin_approved_queue", "Can View Linkedin Approved Queue"),
            ("can_show_linkedin_inbox_queue", "Can View Linkedin Inbox Queue"),
            ("can_show_linkedin_writer_draft", "Can View Linkedin Writer Draft"),
            ("can_show_linkedin_counselling_form", "Can View Linkedin Counselling Form"),
            ("can_view_counselling_form_in_approval_queue", "Can View Counselling Form In Approval Queue"),

            # Approval Queue
            ("can_show_approval_queue", "Can View Approval Queue"),
            ("can_view_all_approval_list", "Can View All Approval List"),
            ("can_view_only_assigned_approval_list", "Can View Only Assigned Approval List"),
            ("can_approve_or_reject_draft", "Can Approve Or Reject Draft"),

            # Appoved Queue
            ("can_show_approved_queue", "Can View Approved Queue"),
            ("can_view_all_approved_list", "Can View All Approved List"),
            ("can_view_only_assigned_approved_list", "Can View Only Assigned Approved List"),

            # Rejected By Admin Queue
            ("can_show_rejectedbyadmin_queue", "Can View Rejected By Admin Queue"),
            ("can_view_all_rejectedbyadmin_list", "Can View All Rejected by Admin List"),
            ("can_view_only_assigned_rejectedbyadmin_list", "Can View Only Assigned Rejected By Admin List"),

            # Rejected By Candidate Queue
            ("can_show_rejectedbycandidate_queue", "Can View Rejected By Candidate Queue"),
            ("can_view_all_rejectedbycandidate_list", "Can View All Rejected By Candidate List"),
            ("can_view_only_assigned_rejectedbycandidate_list", "Can View Only Assigned Rejected By Candidate List"),

            # Allocated Queue
            ("can_show_allocated_queue", "Can Show Allocated Queue"),
            ("can_view_all_allocated_list", "Can View All Allocated List"),
            ("can_view_only_assigned_allocated_list", "Can View Only Assigned Allocated List"),

            # Booster Queue
            ("can_show_booster_queue", "Can Show Booster Queue"),

            # Domestic Profile Update Queue Permissions
            ("can_show_domestic_profile_update_queue", "Can Show Domestic Profile Update Queue"),
            ("domestic_profile_update_assigner", "Domestic Profile Update Assigner"),
            ("domestic_profile_update_assignee", "Domestic Profile Update Assignee"),
            ("can_show_domestic_profile_initiated_queue", "Can Show Domestic Profile Initiated Queue"),

            # Domestic Profile Approval Queue Permissions
            ("can_show_domestic_profile_approval_queue", "Can Show Domestic Profile Approval Queue"),

            # International Profile Update Queue Permissions
            ("can_show_international_profile_update_queue", "Can Show International Profile Update Queue"),
            ("international_profile_update_assigner", "International Profile Update Assigner"),
            ("international_profile_update_assignee", "International Profile Update Assignee"),

            # International Profile Approval Queue Permissions
            ("can_show_international_profile_approval_queue", "Can Show International Profile Approval Queue"),

            # Closed Permission
            ("can_show_closed_oi_queue", "Can Show Closed Orderitem Queue"),
            ("can_view_all_closed_oi_list", "Can View All Closed Orderitem List"),
            ("can_view_only_assigned_closed_oi_list", "Can View Only Assigned Closed Orderitem List"),

            # partner inbox permission
            ("can_show_partner_inbox_queue", "Can Show Partner Inbox Queue"),
            ("show_test_status_fields", "Show Test Status Field For Studymate"),

            # Hold queue permissions
            ("can_show_hold_orderitem_queue", "Can Show Hold Orderitem Queue"),

            # Varification report queue
            ("can_show_varification_report_queue", "Can Show Varification Report Queue"),

            # Action Permission
            ("oi_action_permission", "OrderItem Action Permission"),
            ("oi_export_as_csv_permission", "Order Item Export As CSV Permission"),

            # complaince generation permission
            ("can_generate_compliance_report", "can create compliance report permmission"),

            # jobs on the move permission
            ("can_view_assigned_jobs_on_the_move", "Can view assigned jobs on the move"),
            ("can_assign_jobs_on_the_move", "Can assign jobs on the move"),
            ("can_send_jobs_on_the_move", "Can send assigned jobs on the move")
        )

    def __str__(self):
        return "#{}".format(self.pk)

    @property
    def get_oi_status(self):
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
    def sent_link_count(self):
        return self.jobs_link.filter(status=2).count()


    def get_weeks(self):
        weeks, weeks_till_now = None, None
        sevice_started_op = self.orderitemoperation_set.all().filter(oi_status__in=[5, 31]).order_by('id').first()
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
        sevice_started_op = self.orderitemoperation_set.all().filter(oi_status__in=[5,31]).order_by('id').first()
        links_per_week = getattr(self.product.attr, S_ATTR_DICT.get('LC'), 2)
        if sevice_started_op:
            links_count = 0
            started = sevice_started_op.created
            day = self.product.get_duration_in_day()
            weeks = math.floor(day / 7)
            today = timezone.now()
            for i in range(0, weeks):
                start = started + relativedelta.relativedelta(days=i * 7)
                if start > today:
                    break
                links_count += links_per_week
        return links_count

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
        sevice_started_op = self.orderitemoperation_set.all().filter(oi_status__in=[5,31]).order_by('id').first()
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
        links_sent_till_now = self.jobs_link.filter(status=2).count()
        links_pending = links_needed_till_now - links_sent_till_now

        if links_pending < 0:
            links_pending = 0
        self.pending_links_count = links_pending
        self.save()

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

    def save(self, *args, **kwargs):
        created = not bool(getattr(self, "id"))
        orderitem = OrderItem.objects.filter(id=self.pk).first()
        self.oi_status = 4 if orderitem and orderitem.oi_status == 4 else self.oi_status

        # handling combo case getting parent and updating child
        if self.is_combo and not self.parent:
            jobs_on_the_move_item = self.order.orderitems.filter(product__sub_type_flow=502)
            for i in jobs_on_the_move_item:
                from order.tasks import process_jobs_on_the_move
                process_jobs_on_the_move.delay(i.id)
        elif self.product.sub_type_flow == 502:
            from order.tasks import process_jobs_on_the_move
            process_jobs_on_the_move.delay(self.id)
        super().save(*args, **kwargs)  # Call the "real" save() method.
        # automate application highlighter/priority applicant
        if self.product.sub_type_flow == 503:
            process_application_highlighter(obj=self)

         # # for resume booster create orderitem
        # if self.product.type_flow in [7, 15] and obj.oi_status != last_oi_status:
        #     if obj.oi_status == 5:
        #         self.orderitemoperation_set.create(
        #             oi_draft=self.oi_draft,
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



class OrderItemOperation(AbstractAutoDate):
    coio_id = models.IntegerField(
        _('CP Order IO'),
        blank=True,
        null=True,
        editable=False)
    
    oi = models.ForeignKey(OrderItem)
    linkedin = models.ForeignKey(Draft, null=True, blank=True)
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
    def get_oi_status(self):
        dict_status = dict(OI_OPS_STATUS)
        return dict_status.get(self.oi_status)

    @property
    def get_user_oi_status(self):
        dict_status = dict(OI_USER_STATUS)
        return dict_status.get(self.oi_status)



class Message(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem, null=True)
    oio = models.ForeignKey(OrderItemOperation, null=True)
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


class InternationalProfileCredential(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
    country = models.ForeignKey(Country, null=True)
    username = models.CharField(_('Username'), max_length=100)
    password = models.CharField(_('Password'), max_length=100, null=True, blank=True)
    candidateid = models.CharField(_('CandidateId'), max_length=100, null=True, blank=True)
    candidate_email = models.CharField(_('Candidate Email'), max_length=100)
    site_url = models.CharField(_('Site Url'), max_length=100, null=True, blank=True)
    profile_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailOrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
    email_oi_status = models.PositiveIntegerField(
        _("Email Operation Status"), default=0, choices=OI_EMAIL_STATUS)
    draft_counter = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(default=0)
    to_email = models.CharField(_('To Email'), max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{}-{}'.format(str(self.oi), self.to_email)




class SmsOrderItemOperation(AbstractAutoDate):
    oi = models.ForeignKey(OrderItem)
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
    order = models.ForeignKey(Order)
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
        'order.Order', verbose_name=_("Order"))

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
    refund_request = models.ForeignKey('order.RefundRequest')
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
    refund_request = models.ForeignKey(RefundRequest)
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
    order = models.ForeignKey(Order)
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
        verbose_name=_("Created By"))

    def __str__(self):
        return str(self.pk)

    def get_wc_cat(self,default_text=""):
        sub_dict = dict(WC_CATEGORY)
        return sub_dict.get(self.wc_cat, default_text)

    def get_wc_sub_cat(self,default_text=""):
        cat_dict = dict(WC_SUB_CATEGORY)
        return cat_dict.get(self.wc_sub_cat, default_text)

    def get_wc_status(self,default_text=""):
        status_dict = dict(WC_FLOW_STATUS)
        return status_dict.get(self.wc_status, default_text)