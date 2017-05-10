from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import OpenBasketManager, SavedBasketManager
from .choices import STATUS_CHOICES
from seo.models import AbstractAutoDate
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied


class Cart(AbstractAutoDate):
    owner_id = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Owner ID"))
    owner_email = models.CharField(
        null=True,
        max_length=255,
        verbose_name=_("Owner Email"))
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=0, choices=STATUS_CHOICES)
    # vouchers = models.ManyToManyField(
    #     'coupon.Voucher', verbose_name=_("Vouchers"), blank=True)
    date_merged = models.DateTimeField(
        _("Date merged"), null=True, blank=True)
    date_submitted = models.DateTimeField(
        _("Date submitted"), null=True, blank=True)
    date_frozen = models.DateTimeField(
        _("Date frozen"), null=True, blank=True)
    date_closed = models.DateTimeField(
        _("Date closed"), null=True, blank=True)

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
            u"%(status)s cart (owner: %(owner)s, lines: %(num_lines)d)") \
            % {'status': self.status,
               'owner': self.owner,
               'num_lineitems': self.num_lineitems}


class LineItem(AbstractAutoDate):
    cart = models.ForeignKey(
        Cart, related_name='lineitems',
        verbose_name=_("Cart"))
    parent = models.ForeignKey('self', null=True, blank=True)
    type_item = models.PositiveSmallIntegerField(default=0)
    # reference = unique slug
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
            u"Cart #%(cart_id)d, Product #%(product_id)d, quantity"
            u" %(quantity)d") % {'cart_id': self.cart.pk,
                                 'product_id': self.product.pk,
                                 'quantity': self.quantity}

