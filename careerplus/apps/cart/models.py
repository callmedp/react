from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from seo.models import AbstractAutoDate
from geolocation.models import Country

from .managers import OpenBasketManager, SavedBasketManager
from .choices import STATUS_CHOICES
from order.models import Order


class Cart(AbstractAutoDate):
    try:
        country_choices, CHOICE_COUNTRY = [], []
        for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact='')):
            country_choices.append((m.phone, m.phone))
            CHOICE_COUNTRY.append((m.phone, m.name))

        indian_obj = Country.objects.filter(name='India', phone='91')[0].phone
        default_country = indian_obj

    except:
        country_choices, CHOICE_COUNTRY = [], []
        indian_obj = None
        default_country = None

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
    last_status = models.PositiveIntegerField(("Status"),
        default=None, null=True, blank=True, choices=STATUS_CHOICES)
    # vouchers = models.ManyToManyField(
    #     'coupon.Voucher', verbose_name=_("Vouchers"), blank=True)
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
    first_name = models.CharField(max_length=255, null=True, blank=True,
        verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, null=True, blank=True,
        verbose_name=_("Last Name"))

    email = models.EmailField(max_length=255, null=True, blank=False)

    country_code = models.CharField(max_length=15, choices=country_choices,
        default=indian_obj, null=True, blank=False,
        verbose_name=_("Country Code"))

    mobile = models.CharField(max_length=15, null=True, blank=False)

    address = models.CharField(max_length=255, null=True, blank=True)

    pincode = models.CharField(max_length=15, null=True, blank=True)

    state = models.CharField(max_length=255, null=True, blank=True)

    country = models.CharField(max_length=15, choices=CHOICE_COUNTRY,
        default=default_country, null=True, blank=False)
    
    shipping_done = models.BooleanField(default=False)  #shipping process
    # summary_done = models.BooleanField(default=False)  #summary process

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

    def get_country(self):
        country_dict = dict(self.CHOICE_COUNTRY)
        return country_dict.get(self.country)

    def get_status(self):
        dataD = dict(STATUS_CHOICES)
        return dataD.get(self.status)

    def get_last_status(self):
        dataD = dict(STATUS_CHOICES)
        return dataD.get(self.last_status)


class LineItem(AbstractAutoDate):
    cart = models.ForeignKey(
        Cart, related_name='lineitems',
        verbose_name=_("Cart"))
    parent = models.ForeignKey('self', null=True, blank=True)
    type_item = models.PositiveSmallIntegerField(default=0)
    # unique slug for line item delete
    reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    product = models.ForeignKey(
        'shop.Product', related_name='cart_lineitems',
        verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    # price_currency = models.ForeignKey(
    #     _("Currency"), max_length=12,)
    price_excl_tax = models.DecimalField(
        _('Price excl. Tax'), decimal_places=2, max_digits=12,
        null=True)
    price_incl_tax = models.DecimalField(
        _('Price incl. Tax'), decimal_places=2, max_digits=12, null=True)

    no_process = models.BooleanField(default=False)
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


class Subscription(models.Model):
    candidateid = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    expire_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.order.id, self.candidateid)
