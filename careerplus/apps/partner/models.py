from django.db import models

from django.utils.translation import ugettext_lazy as _
from seo.models import AbstractSEO, AbstractAutoDate
from django.conf import settings
from meta.models import ModelMeta
from shop.functions import get_upload_path_vendor
from geolocation.models import (
    Country,
    State,
    City,)


class Vendor(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    email = models.EmailField(
        _('Email'), unique=True,
        max_length=100, help_text=_('Email Address'))
    mobile = models.CharField(
        _('Mobile Number'), blank=True,
        max_length=20, help_text=_('Mobile Number'))
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        on_delete=models.SET_NULL,
        related_name='partnercountry',
        null=True)
    state = models.ForeignKey(
        State,
        verbose_name=_('State'),
        on_delete=models.SET_NULL,
        related_name='partnerstate',
        null=True)
    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        on_delete=models.SET_NULL,
        related_name='partnercity',
        null=True)
    address = models.TextField(
        _('Address'), blank=True,
        default='', help_text=_('Address'))
    image = models.ImageField(
        _('Image'), upload_to=get_upload_path_vendor,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_vendor,
        blank=True, null=True)
    pan = models.CharField(
        _('PAN No.'), blank=True,
        max_length=20, help_text=_('PAN No.'))
    website = models.CharField(
        _('Website.'), blank=True,
        max_length=20, help_text=_('Website'))
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='VendorHierarchy',
        through_fields=('vendee', 'employee'),
        verbose_name=_('Vendor Hierarchy'),
        blank=True)

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'
        
    def __str__(self):
        return self.name


class VendorHierarchy(AbstractAutoDate):
    active = models.BooleanField(default=True)
    vendee = models.ForeignKey(
        Vendor,
        verbose_name=_('Vendor'),
        related_name='vendorset',
        on_delete=models.CASCADE)
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Employee'),
        related_name='employees',
        on_delete=models.CASCADE)
    designation = models.PositiveSmallIntegerField(
        default=1)

    def __str__(self):
        return _("%(vendor)s to '%(employee)s'") % {
            'vendor': self.vendee,
            'employee': self.employee}
