from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from seo.models import AbstractSEO, AbstractAutoDate
from django.conf import settings
from django.forms import ValidationError
from meta.models import ModelMeta
from shop.functions import (
    get_upload_path_vendor,
    get_upload_path_badge_file)
from geolocation.models import (
    Country,
    State,
    City,)
from order.choices import BOOSTER_RECRUITER_TYPE


class Vendor(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        unique=True,
        help_text=_('Unique name going to decide the slug'))
    cp_id = models.IntegerField(
        _('CP Owner'),
        blank=True,
        null=True,
        editable=False)
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    email = models.EmailField(
        _('Email'),
        max_length=255, help_text=_('Email Address'))
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
    badge_image = models.ImageField(
        _('Badge Image'), upload_to=get_upload_path_badge_file,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_vendor,
        blank=True, null=True)
    pan = models.CharField(
        _('PAN No.'), blank=True,
        max_length=20, help_text=_('PAN No.'))
    website = models.CharField(
        _('Website.'), blank=True,
        max_length=255, help_text=_('Website'))
    prd_add_class = models.ManyToManyField(
        'shop.ProductClass',
        verbose_name=_('Product Add-Types'),
        blank=True)
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='VendorHierarchy',
        through_fields=('vendee', 'employee'),
        verbose_name=_('Vendor Hierarchy'),
        blank=True)

    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def clean(self):

        if not self.icon:
            raise ValidationError(_('Please upload the partner icon'),code='upload_error')



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

    # class Meta:
    #     # pass
    #     # Comment this while initial migration
    #     auto_created = True

    def __str__(self):
        return _("%(vendor)s to '%(employee)s'") % {
            'vendor': self.vendee,
            'employee': self.employee}


class Certificate(AbstractAutoDate):
    name = models.CharField(
        max_length=255, null=False, blank=False, db_index=True)
    skill = models.CharField(max_length=128, null=False, blank=False)
    vendor_provider = models.ForeignKey(Vendor, null=True, blank=True)
    vendor_text = models.CharField(max_length=255, null=True, blank=False)
    certificate_file_url = models.URLField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "vendor_provider")


class UserCertificate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, help_text=_('Created By'))
    certificate = models.ForeignKey(Certificate)
    year = models.PositiveIntegerField(
        null=True, blank=True, default=datetime.now().year)
    candidate_email = models.EmailField(
        _('Email'),
        max_length=255, help_text=_('Candidate Email Address'))
    candidate_mobile = models.CharField(
        _('Mobile Number'), blank=True,
        max_length=20, help_text=_('Candidate Mobile Number'))
    candidate_name = models.CharField(
        _('Name'), blank=True,
        max_length=20, help_text=_('Candidate Name'))
    candidate_id = models.CharField(
        _('Candidate ID'), blank=True,
        max_length=30, help_text=_('Candidate ID'))
    certificate_file_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.certificate.name)


class BoosterRecruiter(AbstractAutoDate):
    recruiter_list = models.TextField(help_text=_('Recruiter name'),)
    type_recruiter = models.PositiveIntegerField(
        _('Recruiter Type'),
        choices=BOOSTER_RECRUITER_TYPE, default=0,
        help_text=_('Recruiter type for booster service')
    )

    @property
    def get_recruiter_list(self):
        return self.recruiter_list.split(',')

    def __str__(self):
        return '<' + self.get_type_recruiter_display() + '>'
