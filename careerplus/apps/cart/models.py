import json
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _

from haystack.query import SearchQuerySet

from seo.models import AbstractAutoDate
from order.models import Order
from geolocation.models import Country, CURRENCY_SYMBOL

from .managers import OpenBasketManager, SavedBasketManager
from .choices import STATUS_CHOICES, SITE_STATUS


class Cart(AbstractAutoDate):

    owner_id = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Owner ID"))
    owner_email = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Owner Email"))
    session_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=0, choices=STATUS_CHOICES)
    last_status = models.PositiveIntegerField(
        _("Last Status"), default=None, null=True,
        blank=True, choices=STATUS_CHOICES)
    coupon = models.ForeignKey(
        'coupon.Coupon',
        on_delete=models.SET_NULL,
        verbose_name=_("Coupon"), null=True,)
    site = models.PositiveSmallIntegerField(
        _("Site Status"),
        default=0, choices=SITE_STATUS)
    is_submitted = models.BooleanField(default=False)
    date_merged = models.DateTimeField(
        _("Date merged"), null=True, blank=True)
    date_submitted = models.DateTimeField(
        _("Date submitted"), null=True, blank=True)
    date_frozen = models.DateTimeField(
        _("Date frozen"), null=True, blank=True)
    date_closed = models.DateTimeField(
        _("Date closed"), null=True, blank=True)

    # shipping detail
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Last Name"))

    email = models.EmailField(max_length=255, null=True, blank=False)

    country_code = models.CharField(
        max_length=15,
        null=True, blank=True, verbose_name=_("Country Code"))

    mobile = models.CharField(max_length=15, null=True, blank=False)

    address = models.CharField(max_length=255, null=True, blank=True)

    pincode = models.CharField(max_length=15, null=True, blank=True)

    state = models.CharField(max_length=255, null=True, blank=True)

    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE)

    shipping_done = models.BooleanField(default=False)  # shipping process
    payment_page = models.BooleanField(default=False)
    # summary_done = models.BooleanField(default=False)  #summary process
    lead_archive = models.BooleanField(default=False)
    lead_created = models.BooleanField(default=False)

    # utm parameters
    utm_params = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'cart'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    objects = models.Manager()
    open = OpenBasketManager()
    saved = SavedBasketManager()

    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(*args, **kwargs)

        self._lineitems = None

    def __str__(self):
        return _(
            u"%(status)s cart (owner: %(owner)s)") \
            % {'status': self.status,
               'owner': self.owner_id}

    def get_status(self):
        dataD = dict(STATUS_CHOICES)
        return dataD.get(self.status)

    def get_last_status(self):
        dataD = dict(STATUS_CHOICES)
        return dataD.get(self.last_status)


class LineItem(AbstractAutoDate):
    cart = models.ForeignKey(
        Cart, related_name='lineitems',
        verbose_name=_("Cart"), on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    type_item = models.PositiveSmallIntegerField(default=0)
    # unique slug for line item delete
    reference = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    product = models.ForeignKey(
        'shop.Product', related_name='cart_lineitems',
        verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    delivery_service = models.ForeignKey(
        'shop.DeliveryService',
        related_name='delivery_lineitems',
        on_delete=models.SET_NULL,
        null=True, blank=True)
    # price_currency = models.ForeignKey(
    #     _("Currency"), max_length=12,)
    price_excl_tax = models.DecimalField(
        _('Price excl. Tax'), decimal_places=2, max_digits=12,
        null=True)
    price_incl_tax = models.DecimalField(
        _('Price incl. Tax'), decimal_places=2, max_digits=12, null=True)

    no_process = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    # True for variation and False for Addon
    parent_deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(LineItem, self).__init__(*args, **kwargs)

    class Meta:
        app_label = 'cart'
        ordering = ['modified', 'pk']
        # unique_together = ("cart", "reference")
        verbose_name = _('Cart Line Item')
        verbose_name_plural = _('Cart Line Items')

    def __str__(self):
        return _(
            u"Cart #%(cart_id)d, Product #%(product_id)d, lineid"
            u" %(line_id)d") % {'cart_id': self.cart.pk,
                                'product_id': self.product.pk,
                                'line_id': self.pk}

    def available(self):
        flag = False
        if self.parent:
            base_product = self.parent.product
            product = self.product
            sqs = SearchQuerySet().filter(id=base_product.pk)
            try:
                sqs = sqs[0]
                if self.parent_deleted:
                    variations = json.loads(sqs.pVrs)
                    product_list = variations.get('var_list', [])
                else:
                    fbts = json.loads(sqs.pFBT)
                    product_list = fbts.get('fbt_list', [])

                for p_data in product_list:
                    if p_data.get('id') == product.pk:
                        flag = True
                        break
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                pass

        else:
            product = self.product
            sqs = SearchQuerySet().filter(id=product.pk)
            try:
                sqs = sqs[0]
                flag = True
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                pass

        return flag

    def get_solr_price(self):
        if self.parent:
            base_product = self.parent.product
            product = self.product
            sqs = SearchQuerySet().filter(id=base_product.pk)
            try:
                sqs = sqs[0]
                price = 0
                if self.parent_deleted:
                    variations = json.loads(sqs.pVrs)
                    product_list = variations.get('var_list', [])
                else:
                    fbts = json.loads(sqs.pFBT)
                    product_list = fbts.get('fbt_list', [])

                for p_data in product_list:
                    if p_data.get('id') == product.pk:
                        price = p_data.get('inr_price')
                        break

                if not price:
                    price = product.get_price()

            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                price = product.get_price()

        else:
            product = self.product
            sqs = SearchQuerySet().filter(id=product.pk)
            try:
                sqs = sqs[0]
                price = sqs.pPinb
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

                price = product.get_price()

        return round(price, 0)


SUBSCRIPTION_STATUS = (
    (-1, "Invalid"),
    (0, "Failed"),
    (1, "Processed"),
    (2, "Expired"),
)


class Subscription(AbstractAutoDate):
    candidateid = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.SmallIntegerField(
        choices=SUBSCRIPTION_STATUS, default=-1)
    remark = models.CharField(max_length=255, null=True, blank=True)
    expire_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.order.id, self.candidateid)
