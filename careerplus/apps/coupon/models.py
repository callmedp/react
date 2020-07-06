import random

from django.conf import settings
from django.db import IntegrityError
from django.db import models
from django.dispatch import Signal
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from seo.models import AbstractAutoDate
from shop.functions import get_upload_path_coupon

from .choices import (
    COUPON_TYPES, CODE_LENGTH, CODE_CHARS,
    SEGMENTED_CODES, SEGMENT_LENGTH, SEGMENT_SEPARATOR,
    SITE_CHOICES, COUPON_SCOPE_CHOICES
)



class CouponManager(models.Manager):
    def create_coupon(self, coupon_type, value, users=[], valid_until=None, prefix="", campaign=None, user_limit=None):
        coupon = self.create(
            value=value,
            code=Coupon.generate_code(prefix),
            coupon_type=coupon_type,
            valid_until=valid_until,
            campaign=campaign,
        )
        if user_limit is not None:  # otherwise use default value of model
            coupon.user_limit = user_limit
        try:
            coupon.save()
        except IntegrityError:
            # Try again with other code
            coupon = Coupon.objects.create_coupon(coupon_type, value, users, valid_until, prefix, campaign)
        if not isinstance(users, list):
            users = [users]
        for user in users:
            if user:
                CouponUser(user=user, coupon=coupon).save()
        return coupon

    def create_coupons(self, quantity, coupon_type, value, valid_until=None, prefix="", campaign=None):
        coupons = []
        for i in range(quantity):
            coupons.append(self.create_coupon(coupon_type, value, None, valid_until, prefix, campaign))
        return coupons

    def used(self):
        return self.exclude(users__redeemed_at__isnull=True)

    def unused(self):
        return self.filter(users__redeemed_at__isnull=True)

    def expired(self):
        return self.filter(valid_until__lt=timezone.now())


class Coupon(AbstractAutoDate):
    value = models.DecimalField(
        _("Value"), max_digits=8, decimal_places=2, default=0.0)
    min_purchase = models.DecimalField(
        _("Minimum purchase Value"), max_digits=8, decimal_places=2, default=0.0)
    max_deduction = models.DecimalField(
        _("Maximum Deduction"), max_digits=8, decimal_places=2, default=0.0)
    code = models.CharField(
        _("Code"), max_length=30, unique=True, blank=True,
        help_text=_("Leaving this field empty will generate a random code."))
    coupon_type = models.CharField(_("Type"), max_length=20, choices=COUPON_TYPES)
    user_limit = models.PositiveIntegerField(_("User limit"), default=1)
    valid_from = models.DateTimeField(
        _("Valid from"), blank=True, null=True,
        help_text=_("Leave empty for coupons that never expire"))
    valid_until = models.DateTimeField(
        _("Valid until"), blank=True, null=True,
        help_text=_("Leave empty for coupons that never expire"))

    image = models.ImageField(
        _('image'), upload_to=get_upload_path_coupon,
        blank=True, null=True)

    coupon_msg = models.CharField(
        _("Message to be displayed"), max_length=60, null=True, blank=True,
        help_text=_("This message will display when coupon limit exceeds"))

    description = models.CharField(
        _("Description to be displayed on mailers"), max_length=255, null=True, blank=True,
        help_text=_("This will be display on description"))

    campaign = models.ForeignKey(
        'Campaign',
        verbose_name=_("Campaign"),
        blank=True, null=True, related_name='coupons',on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    site = models.PositiveIntegerField(
        _("Site"), choices=SITE_CHOICES, default=0)

    coupon_scope = models.PositiveIntegerField(
        _("Coupon Scope"), choices=COUPON_SCOPE_CHOICES, default=0)

    products = models.ManyToManyField(
        "shop.Product",
        verbose_name=_('Coupon Products'),
        related_name='couponproducts',
        blank=True)

    source = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        blank=True)
    
    objects = CouponManager()

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Coupon.generate_code()
        super(Coupon, self).save(*args, **kwargs)

    def suspended(self):
        return self.valid_from is not None and self.valid_from > timezone.now() and self.active

    def expired(self):
        return self.valid_until is not None and self.valid_until < timezone.now()

    @property
    def is_redeemed(self):
        """ Returns true is a coupon is redeemed (completely for all users) otherwise returns false. """
        return self.users.filter(
            redeemed_at__isnull=False
        ).count() >= self.user_limit and self.user_limit is not 0

    @property
    def redeemed_at(self):
        try:
            return self.users.filter(redeemed_at__isnull=False).order_by('redeemed_at').last().redeemed_at
        except self.users.through.DoesNotExist:
            return None

    @classmethod
    def generate_code(cls, prefix="", segmented=SEGMENTED_CODES):
        code = "".join(random.choice(CODE_CHARS) for i in range(CODE_LENGTH))
        if segmented:
            code = SEGMENT_SEPARATOR.join([code[i:i + SEGMENT_LENGTH] for i in range(0, len(code), SEGMENT_LENGTH)])
            return prefix + code
        else:
            return prefix + code

    def is_valid_coupon(self, site=1, source=None, cart_obj=None, product_list=[]):
        # site=1 for learning
        flag = False
        if site == 2:
            if self.coupon_scope == 2 and source:
                source_list = self.source.split(',')
                if source and str(source) in source_list:
                    flag = True
            elif self.coupon_scope == 1 and product_list:
                coupon_products = list(self.products.all().values_list('id', flat=True))
                if set(coupon_products) & set(product_list):
                    flag = True
            elif self.coupon_scope == 0:
                flag = True

        elif site == 1:
            if cart_obj and self.coupon_scope == 1:
                product_list = list(cart_obj.lineitems.all().values_list('product', flat=True))
                coupon_products = list(self.products.all().values_list('id', flat=True))
                if set(product_list) & set(coupon_products):
                    flag = True
            elif self.coupon_scope == 0:
                flag = True
        else:
            # site = 0
            if self.coupon_scope == 2 and source:
                source_list = self.source.split(',')
                if source and str(source) in source_list:
                    flag = True

            elif cart_obj and self.coupon_scope == 1:
                product_list = list(cart_obj.lineitems.all().values_list('product', flat=True))
                coupon_products = list(self.products.all().values_list('id', flat=True))
                if set(product_list) & set(coupon_products):
                    flag = True
            elif self.coupon_scope == 0:
                flag = True

        return flag


class Campaign(AbstractAutoDate):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.name


class CouponUser(AbstractAutoDate):
    coupon = models.ForeignKey(Coupon, related_name='users',on_delete=models.CASCADE)
    user = models.CharField(
        _("User Email"),
        max_length=255, blank=True,
        null=True)

    redeemed_at = models.DateTimeField(_("Redeemed at"), blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['pk']
        verbose_name = _("Coupon User")
        verbose_name_plural = _("Coupon Users")
