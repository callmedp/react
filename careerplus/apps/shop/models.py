from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from seo.models import AbstractSEO, AbstractAutoDate
from meta.models import ModelMeta
from faq.models import FAQuestion

from .functions import (
    get_upload_path_category,
    get_upload_path_product_banner,
    get_upload_path_product_icon,
    get_upload_path_product_image,
    get_upload_path_product_file,)
from .choices import (
    ENTITY_CHOICES,
    CATEGORY_CHOICES,
    PRODUCT_CHOICES,
    FLOW_CHOICES,
    EXP_CHOICES,
    ATTRIBUTES_CHOICES,
    RELATION_CHOICES)


class Category(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    type_entity = models.PositiveSmallIntegerField(
        _('Entity'), choices=ENTITY_CHOICES, default=0)
    type_level = models.PositiveSmallIntegerField(
        _('Level'), choices=CATEGORY_CHOICES, default=0)
    description = models.TextField(
        _('Description'), blank=True, default='')
    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path_category,
        blank=True, null=True)
    image = models.ImageField(
        _('Image'), upload_to=get_upload_path_category,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_category,
        blank=True, null=True)
    parent = models.ForeignKey(
        _('Main Parent'), 'self',
        on_delete=models.SET_NULL,
        related_name='parent',
        null=True)
    other_parent = models.ManyToManyField(
        _('Other Parent'),
        'self', symmetrical=False,
        on_delete=models.SET_NULL,
        related_name='other_parent',
        null=True)
    active = models.BooleanField(default=False)
    display_order = models.IntegerField(default=1)

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'created',
        'modified_time': 'modified',
        'url': 'get_full_url',
    }

    class Meta:
        verbose_name = _('Catalog Category')
        verbose_name_plural = _('Catalog Categories')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_desc
        if not description:
            description = self.description
        return description.strip()

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('category-listing', kwargs={'slug': self.slug})


class Attribute(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    display_name = models.CharField(
        _('Display Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    type_attribute = models.PositiveSmallIntegerField(
        _('Type'), choices=ATTRIBUTES_CHOICES, default=0)
    is_visible = models.BooleanField(default=True)
    is_multiple = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_indexable = models.BooleanField(default=True)
    is_comparable = models.BooleanField(default=True)
    is_filterable = models.BooleanField(default=True)
    is_sortable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Keyword(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Currency(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Name of Currency'))
    value = models.PositiveIntegerField(
        _('Value'), max_length=100,
        help_text=_('Integer Value'))
    # country = models.ManytoManyField()
    exchange_rate = models.DecimalField(
        _('Exchange'), default=0.0)
    offset = models.DecimalField(
        _('Offset'), default=0.0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class AbstractProduct(AbstractAutoDate, AbstractSEO):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    type_product = models.PositiveSmallIntegerField(
        _('Type'), choices=PRODUCT_CHOICES, default=0)
    type_flow = models.PositiveSmallIntegerField(
        _('Flow'), choices=FLOW_CHOICES, default=0)
    upc = models.CharField(
        _('Universal Product Code'), max_length=100,
        help_text=_('To be filled by vendor'))
    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path_product_banner,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_product_icon,
        blank=True, null=True)
    image = models.ImageField(
        _('Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    video_url = models.CharField(
        _('Video Url'), blank=True, max_length=200)
    flow_image = models.ImageField(
        _('Delivery Flow Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    email_cc = models.TextField(
        _('Email_CC ID'), blank=True, default='')
    about = models.TextField(
        _('About Product'), blank=True, default='')
    description = models.TextField(
        _('Description Product'), blank=True, default='')
    buy_shine = models.TextField(
        _('Why Buy From Shine'), blank=True, default='')
    mail_desc = models.TextField(
        _('Welcome Mail Description'), blank=True, default='')
    duration_months = models.IntegerField(
        _('Duration In Months'), default=0)
    duration_days = models.IntegerField(
        _('Duration In Days'), default=0)
    experience = models.PositiveSmallIntegerField(
        _('Experience'), choices=EXP_CHOICES, default=0)

    class Meta:
        abstract = True


class Product(AbstractProduct, ModelMeta):
    avg_rating = models.DecimalField(
        _('Average Rating'), default=2.5)
    no_review = models.PositiveIntegerField(
        _('No. Of Review'), default=0)
    buy_count = models.PositiveIntegerField(
        _('Buy Count'), default=0)
    keywords = models.ManyToManyField(
        _('Keywords'), Keyword,
        on_delete=models.SET_NULL,
        null=True)
    search_keywords = models.TextField(
        _('Search Keywords'), blank=True, default='')

    siblings = models.ManyToManyField(
        _('Sibling Products'), 'self',
        on_delete=models.SET_NULL,
        symmetrical=True,
        related_name='siblings',
        null=True)
    related = models.ManyToManyField(
        _('Related Products'), 'self',
        on_delete=models.SET_NULL,
        through='RelatedProduct',
        null=True)
    childs = models.ManyToManyField(
        _('Child Products'), 'self',
        on_delete=models.SET_NULL,
        through='ChildProduct',
        null=True)
    categories = models.ManyToManyField(
        _('Product Category'),
        Category,
        through='ProductCategory',
        on_delete=models.SET_NULL,
        null=True)
    faqs = models.ManyToManyField(
        _('Product FAQ'), FAQuestion,
        through='FAQProduct',
        on_delete=models.SET_NULL,
        null=True)
    attributes = models.ManyToManyField(
        _('Product Attributes'), Attribute,
        through='ProductAttribute',
        on_delete=models.SET_NULL,
        null=True)
    prices = models.ManyToManyField(
        _('Product Price'), Currency,
        through='ProductPrice',
        on_delete=models.SET_NULL,
        null=True)

    active = models.BooleanField(default=False)
    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'created',
        'modified_time': 'modified',
        'url': 'get_full_url',
    }

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_desc
        if not description:
            description = self.description
        return description.strip()

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


class ProductArchive(AbstractProduct):
    originalproduct = models.ForeignKey(
        _('Original Product'), Product,
        on_delete=models.SET_NULL,
        related_name='originalproduct',
        null=True)
    parent = models.IntegerField(
        _('Parent'),
        blank=True,
        null=True)
    siblings = models.CharField(
        _('Siblings'),
        blank=True,
        max_length=255)
    back_nav = models.IntegerField(
        _('Back Navigation'),
        blank=True,
        null=True)
    main_nav = models.CharField(
        _('Main Category'),
        blank=True,
        max_length=255)
    sub_nav = models.CharField(
        _('Sub Category'),
        blank=True,
        max_length=255)
    faqs = models.CharField(
        _('FAQ'),
        blank=True,
        max_length=255)

    class Meta:
        verbose_name = _('Product Archive')
        verbose_name_plural = _('Product Archives ')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name


class ProductScreen(AbstractProduct):
    linkedproduct = models.ForeignKey(
        _('Linked Product'), Product,
        on_delete=models.SET_NULL,
        related_name='linkedproduct',
        null=True)
    parent = models.IntegerField(
        _('Parent'),
        blank=True,
        null=True)
    siblings = models.CharField(
        _('Siblings'),
        blank=True,
        max_length=255)
    back_nav = models.IntegerField(
        _('Back Navigation'),
        blank=True,
        null=True)
    main_nav = models.CharField(
        _('Main Category'),
        blank=True,
        max_length=255)
    sub_nav = models.CharField(
        _('Sub Category'),
        blank=True,
        max_length=255)
    faqs = models.CharField(
        _('FAQ'),
        blank=True,
        max_length=255)

    class Meta:
        verbose_name = _('Product Screen')
        verbose_name_plural = _('Product Screens ')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name


class RelatedProduct(AbstractAutoDate):
    primary = models.ForeignKey(
        _('Primary'),
        Product, on_delete=models.SET_CASCADE)
    secondary = models.ForeignKey(
        _('Secondary'),
        Product, on_delete=models.SET_CASCADE)
    type_relation = models.PositiveSmallIntegerField(
        _('Relation'), choices=RELATION_CHOICES, default=0)
    price_offset = models.DecimalField(
        _('Price Offset'), default=0.0)
    price_offset_percent = models.DecimalField(
        _('% Offset'), default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class ChildProduct(AbstractAutoDate):
    parent = models.ForeignKey(
        _('Primary'),
        Product, on_delete=models.SET_CASCADE)
    child = models.ForeignKey(
        _('Secondary'),
        Product, on_delete=models.SET_CASCADE)
    price_offset = models.DecimalField(
        _('Price Offset'), default=0.0)
    price_offset_percent = models.DecimalField(
        _('% Offset'), default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class ProductCategory(AbstractAutoDate):
    category = models.ForeignKey(
        _('Category'),
        Category, on_delete=models.SET_CASCADE)
    product = models.ForeignKey(
        _('Product'),
        Product, on_delete=models.SET_CASCADE)
    is_main = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class FAQProduct(AbstractAutoDate):
    question = models.ForeignKey(
        _('FAQuestion'),
        FAQuestion, on_delete=models.SET_CASCADE)
    product = models.ForeignKey(
        _('Product'),
        Product, on_delete=models.SET_CASCADE)
    ordering = models.PositiveIntegerField(
        _('Ordering'),
        default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class ProductAttribute(AbstractAutoDate):
    attribute = models.ForeignKey(
        _('Attribute'),
        Attribute, on_delete=models.SET_CASCADE)
    product = models.ForeignKey(
        _('Product'),
        Product, on_delete=models.SET_CASCADE)
    value_text = models.CharField(
        _('Value Text'), max_length=100,
        blank=True)
    value_integer = models.PositiveSmallIntegerField(
        _('Value Integer'), default=0)
    value_image = models.ImageField(
        _('Value Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    value_file = models.ImageField(
        _('Value File'), upload_to=get_upload_path_product_file,
        blank=True, null=True)
    value_date = models.DateTimeField(
        _('Value Date'), blank=True, null=True)
    value_decimal = models.DecimalField(
        _('Value Date'), default=0.0)
    value_ltext = models.TextField(
        _('Value Large Text'), blank=True, default='')
    
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk


class ProductPrice(AbstractAutoDate):
    currency = models.ForeignKey(
        _('Currency'),
        Currency, on_delete=models.SET_CASCADE)
    product = models.ForeignKey(
        _('Product'),
        Product, on_delete=models.SET_CASCADE)
    value = models.DecimalField(
        _('Value Price'), default=0.0)
    fake_value = models.DecimalField(
        _('Value Fake Price'), default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.pk
