# inbuilt imports
from datetime import datetime
from decimal import Decimal

# framework imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import ValidationError

# local imports
from .choices import USER_CERTITIFICATE_STATUS

# inter apps imports
from seo.models import AbstractSEO, AbstractAutoDate
from meta.models import ModelMeta
from shop.functions import (
    get_upload_path_vendor,
    get_upload_path_badge_file)
from geolocation.models import (
    Country,
    State,
    City,)
from order.choices import BOOSTER_RECRUITER_TYPE
from .choices import SCORE_TYPE_CHOICES

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


class Assesment(AbstractAutoDate):
    vendor_text = models.CharField(max_length=255, blank=True, null=True)
    vendor_provider = models.ForeignKey(Vendor, null=True, blank=True)
    assesment_name = models.CharField(max_length=255, blank=True, null=True)
    candidate_id = models.CharField(
        _('Candidate_id'), blank=True,
        max_length=60, help_text=_('Candidate_id'))
    candidate_email = models.EmailField(
        _('Email'),
        max_length=255, help_text=_('Candidate Email Address'))
    extra_info = models.TextField(
        _('Extra Info'), blank=True,
        default='', help_text=_('Extra Info'))
    report = models.TextField(blank=True)
    overallScore = models.DecimalField(
        default=Decimal('0.00'), decimal_places=2,
        max_digits=12, null=True, blank=True
    )




class Certificate(AbstractAutoDate):
    name = models.CharField(
        max_length=255, null=False, blank=False, db_index=True)
    skill = models.CharField(max_length=128, null=False, blank=False)
    vendor_provider = models.ForeignKey(Vendor, null=True, blank=True)
    vendor_text = models.CharField(max_length=255, null=True, blank=True)
    certificate_file_url = models.URLField(max_length=500, blank=True, null=True)
    vendor_image_url = models.URLField(max_length=500, blank=True, null=True)
    vendor_certificate_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.PositiveIntegerField(null=True, blank=True)


    @property
    def provider(self):
        if self.vendor_provider:
            return self.vendor_provider.name
        else:
            return self.vendor_text
    

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
    expiry_date = models.DateTimeField(null=True, blank=True)
    order_item = models.ForeignKey(
        'order.OrderItem', related_name='user_certificate_orderitem',
        verbose_name=_("Order Item"), blank=True, null=True)
    status = models.IntegerField(choices=USER_CERTITIFICATE_STATUS, default=0)
    extra_info = models.TextField(null=True, blank=True)
    assesment = models.ForeignKey('Assesment', null=True, blank=True)

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

class Report(models.Model):

    assessment_id = models.IntegerField()
    url = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Score(AbstractAutoDate):
    subject = models.CharField(max_length=255)
    assesment = models.ForeignKey('Assesment', null=True, blank=True)
    score_type = models.PositiveSmallIntegerField(choices=SCORE_TYPE_CHOICES, default=0)
    max_score = models.CharField(max_length=255)
    score_obtained = models.IntegerField(default=0)


class ParsedAssesmentData:

    def __init__(self):
        self.score = Score()
        self.scores = []
        self.assesment = Assesment()
        self.certificate = Certificate()
        self.user_certificate = UserCertificate()
        self.report = Report()
        self.reports = []
        self.certificates = []

class UserCertificateOperations(AbstractAutoDate):
    user_certificate = models.ForeignKey(UserCertificate)
    op_type = models.IntegerField(choices=USER_CERTITIFICATE_STATUS, default=0)
    last_op_type = models.IntegerField(choices=USER_CERTITIFICATE_STATUS, default=0)

        
    def __str__(self):
        return ' {} - ({}) for {} '.format(
            self.user_certificate.certificate.name, self.get_op_type_display(),
            self.user_certificate.candidate_email)


class ProductSkill(AbstractAutoDate):

    skill = models.ForeignKey(
        'shop.Skill',
        verbose_name=_('Skill'),
        related_name='new_productskills',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        'shop.Product',
        verbose_name=_('Product'),
        related_name='new_productskills',
        on_delete=models.CASCADE)
    third_party_skill_id = models.PositiveIntegerField(default=0)
    primary = models.BooleanField(default=False)

    def __str__(self):
        name = '{} - ({}) to {} - ({})'.format(
            self.skill.name, self.skill_id,
            self.product.get_name, self.product_id)
        return name

    class Meta:
        unique_together = ('product', 'skill')
        verbose_name = _('Product Skill')
        verbose_name_plural = _('Product Skills')

class PixelTracker(AbstractAutoDate):
    pixel_slug = models.CharField(
        max_length=255, help_text=('Pixel Slug')
    )
    conversion_urls = models.TextField(help_text='conversion_page_url')
    landing_urls = models.TextField(help_text='landing_page_urls')
    days = models.IntegerField(help_text='No. of days for tracking', blank=True, null=True)


