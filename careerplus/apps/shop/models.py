from django.utils import timezone

from decimal import Decimal
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField

from seo.models import AbstractSEO, AbstractAutoDate
from meta.models import ModelMeta
from partner.models import Vendor
from faq.models import FAQuestion, Chapter
from geolocation.models import Country, Currency

from .functions import (
    get_upload_path_category,
    get_upload_path_product_banner,
    get_upload_path_product_icon,
    get_upload_path_product_image,
    get_upload_path_product_file,)
from .choices import (
    SERVICE_CHOICES,
    CATEGORY_CHOICES,
    PRODUCT_CHOICES,
    FLOW_CHOICES,
    EXP_CHOICES,
    ATTRIBUTE_CHOICES,
    RELATION_CHOICES,
    COURSE_TYPE_CHOICES,
    MODE_CHOICES,
    BG_CHOICES)


class Category(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    type_service = models.PositiveSmallIntegerField(
        _('Service'), choices=SERVICE_CHOICES, default=0)
    type_level = models.PositiveSmallIntegerField(
        _('Level'), choices=CATEGORY_CHOICES, default=0)
    video_link = models.CharField(
        _('Video Link'), blank=True, max_length=200)
    career_outcomes = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text='semi-colon(;) separated designations, e.g. Project Engineer; Software Engineer; ...')
    description = RichTextField(
        verbose_name=_('Description'), blank=True, default='')
    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path_category,
        blank=True, null=True)
    is_skill = models.BooleanField(
        _('Is Skill'),
        default=False)
    graph_image = models.ImageField(
        _('Graph Image'), upload_to=get_upload_path_category,
        blank=True, null=True)
    image = models.ImageField(
        _('Image'), upload_to=get_upload_path_category,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_category,
        blank=True, null=True)
    related_to = models.ManyToManyField(
        'self',
        through='CategoryRelationship',
        through_fields=('related_from', 'related_to'),
        verbose_name=_('Related Category'),
        symmetrical=False, blank=True)
    categoryproducts = models.ManyToManyField(
        'shop.Product',
        verbose_name=_('Category Product'),
        through='ProductCategory',
        through_fields=('category', 'product'),
        blank=True)
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

        return self.name + '(' + self.get_level + ')'

    @property
    def get_level(self):
        return dict(CATEGORY_CHOICES).get(self.type_level)

    def save(self, *args, **kwargs):
        if not self.url and self.pk:
            self.url = self.get_full_url()
        if self.name:
            if not self.title:
                self.title = self.name
            if not self.heading:
                self.heading = self.name
            if not self.image_alt:
                self.image_alt = self.name
        if self.description:
            if not self.meta_desc:
                self.meta_desc = self.get_meta_desc(self.description.strip())
                
        super(Category, self).save(*args, **kwargs)

    def get_meta_desc(self, description=''):
        if description:
            try:
                import re
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', description)
            except:
                cleantext = ''
        return cleantext

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_desc
        if not description:
            description = self.description
        return description.strip()

    def get_full_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        if self.pk:
            return reverse('skillpage:skill-page-listing', kwargs={'slug': self.slug, 'pk': self.pk})
        
    def add_relationship(self, category, relation=0):
        relationship, created = CategoryRelationship.objects.get_or_create(
            related_from=self,
            related_to=category,
            relation=relation)
        return relationship

    def remove_relationship(self, category, relation=0):
        CategoryRelationship.objects.filter(
            related_from=self,
            related_to=category,
            relation=relation).delete()
        return

    def get_relationships(self):
        return self.related_to.filter(
            to_category__related_from=self)

    def get_related_to(self, relation):
        return self.category_set.filter(
            from_category__related_to=self)

    def get_parent(self):
        if self.type_level in [0, 1]:
            return []
        elif self.type_level == 2:
            return self.related_to.filter(
                to_category__related_from=self,
                type_level=1)
        elif self.type_level == 3:
            return self.related_to.filter(
                to_category__related_from=self,
                type_level=2)
        elif self.type_level == 4:
            return self.related_to.filter(
                to_category__related_from=self,
                type_level=3)
        return []

    def get_childrens(self):
        if self.type_level == 1:
            return self.category_set.filter(
                from_category__related_to=self,
                type_level=2)
        elif self.type_level == 2:
            return self.category_set.filter(
                from_category__related_to=self,
                type_level=3)
        elif self.type_level == 3:
            return self.category_set.filter(
                from_category__related_to=self,
                type_level=4)
        return []

    def split_career_outcomes(self):
        return self.career_outcomes.split(',')

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_childrens().count()

    def create_icon(self):
        if not self.image:
            return
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (100, 100)
        DJANGO_TYPE = None

        if self.image.name.endswith(".jpg"):
            DJANGO_TYPE = 'image/jpeg'
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif self.image.name.endswith(".png"):
            DJANGO_TYPE = 'image/png'
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            return
        image = Image.open(BytesIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        self.icon.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
        )
        return


class CategoryRelationship(AbstractAutoDate):
    related_from = models.ForeignKey(
        Category,
        verbose_name=_('From'),
        related_name='from_category',
        on_delete=models.CASCADE)
    related_to = models.ForeignKey(
        Category,
        verbose_name=_('To'),
        related_name='to_category',
        on_delete=models.CASCADE)
    relation = models.PositiveSmallIntegerField(
        choices=((0, 'Active'), (1, 'Inactive'),), default=0)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    is_main_parent = models.BooleanField(default=False)

    def __str__(self):
        return _("%(pri)s to '%(sec)s'") % {
            'pri': self.related_from,
            'sec': self.related_to}

    class Meta:
        unique_together = ('related_from', 'related_to')
        verbose_name = _('Relationship')
        verbose_name_plural = _('Relationships')


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'), max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Attribute option group')
        verbose_name_plural = _('Attribute option groups')

    @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)


class AttributeOption(models.Model):
    group = models.ForeignKey(
        'shop.AttributeOptionGroup', related_name='options',
        verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)

    def __str__(self):
        return self.option

    class Meta:
        unique_together = ('group', 'option')
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')


class Attribute(AbstractAutoDate):
    type_service = models.PositiveSmallIntegerField(
        _('Service'), choices=SERVICE_CHOICES, default=0)
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    display_name = models.CharField(
        _('Display Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    type_attribute = models.PositiveSmallIntegerField(
        _('Type'), choices=ATTRIBUTE_CHOICES, default=0)
    required = models.BooleanField(_('Required'), default=False)
    is_visible = models.BooleanField(default=True)
    is_multiple = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_indexable = models.BooleanField(default=True)
    is_comparable = models.BooleanField(default=True)
    is_filterable = models.BooleanField(default=True)
    is_sortable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    option_group = models.ForeignKey(
        'shop.AttributeOptionGroup', blank=True, null=True,
        verbose_name=_("Option Group"),
        help_text=_('Select an option group if using type "Option"'))
    attributeproducts = models.ManyToManyField(
        'shop.Product',
        verbose_name=_('Attribute Product'),
        through='ProductAttribute',
        through_fields=('attribute', 'product'),
        blank=True)

    def __str__(self):
        return self.name

    @property
    def get_entity(self):
        return dict(SERVICE_CHOICES).get(self.type_service)

    @property
    def get_type(self):
        return dict(ATTRIBUTE_CHOICES).get(self.type_attribute)


class Keyword(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100, unique=True)
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
    type_service = models.PositiveSmallIntegerField(
        _('Service'), choices=SERVICE_CHOICES, default=0)
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
    image_bg = models.PositiveSmallIntegerField(
        _('Icon Background'), choices=BG_CHOICES, default=0)
    image = models.ImageField(
        _('Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    image_alt = models.CharField(
        _('Image Alt'), blank=True, max_length=100)
    video_url = models.CharField(
        _('Video Url'), blank=True, max_length=200)
    flow_image = models.ImageField(
        _('Delivery Flow Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    email_cc = RichTextField(
        verbose_name=_('Email CC'), blank=True, default='')
    about = RichTextField(
        verbose_name=_('About Product'), blank=True, default='')
    description = RichTextField(
        verbose_name=_('Description Product'), blank=True, default='')
    buy_shine = RichTextField(
        verbose_name=_('What you will get'), blank=True, default='')
    mail_desc = RichTextField(
        verbose_name=_('Welcome Mail Description'), blank=True, default='')
    call_desc = RichTextField(
        verbose_name=_('Welcome Call Description'), blank=True, default='')
    duration_months = models.IntegerField(
        _('Duration In Months'), default=0)
    duration_days = models.IntegerField(
        _('Duration In Days'), default=0)
    experience = models.PositiveSmallIntegerField(
        _('Experience'), choices=EXP_CHOICES, default=0)
    requires_delivery = models.BooleanField(
        _("Requires delivery?"),
        default=True)
    # is_discountable = models.BooleanField(
    #     _("Discountable?"),
    #     default=True)
    certification = models.BooleanField(
        _("Give Certification"),
        default=True)
    study_mode = models.PositiveSmallIntegerField(
        _('Study Mode'), choices=MODE_CHOICES, default=0)
    course_type = models.PositiveSmallIntegerField(
        _('Course Type'), choices=COURSE_TYPE_CHOICES, default=0)

    class Meta:
        abstract = True


class Product(AbstractProduct, ModelMeta):
    avg_rating = models.DecimalField(
        _('Average Rating'),
        max_digits=8, decimal_places=2,
        default=2.5)
    no_review = models.PositiveIntegerField(
        _('No. Of Review'), default=0)
    buy_count = models.PositiveIntegerField(
        _('Buy Count'), default=0)
    num_jobs = models.PositiveIntegerField(
        _('Num Jobs'), default=0)
    search_keywords = models.TextField(
        _('Search Keywords'),
        blank=True, default='')
    countries = models.ManyToManyField(
        Country,
        verbose_name=_('Country Available'),
        related_name='countryavailable',
        blank=True)
    variation = models.ManyToManyField(
        'self',
        through='VariationProduct',
        related_name='variationproduct+',
        through_fields=('main', 'sibling'),
        verbose_name=_('Variation Product'),
        symmetrical=False, blank=True)
    related = models.ManyToManyField(
        'self',
        through='RelatedProduct',
        related_name='relatedproduct+',
        through_fields=('primary', 'secondary'),
        verbose_name=_('Related Product'),
        symmetrical=False, blank=True)    
    childs = models.ManyToManyField(
        'self',
        through='ChildProduct',
        related_name='comboproduct+',
        through_fields=('father', 'children'),
        verbose_name=_('Child Product'),
        symmetrical=False, blank=True)
    categories = models.ManyToManyField(
        'shop.Category',
        verbose_name=_('Product Category'),
        through='ProductCategory',
        through_fields=('product', 'category'),
        blank=True)
    keywords = models.ManyToManyField(
        'shop.Keyword',
        verbose_name=_('Product Keyword'),
        related_name='productkeyword',
        blank=True)
    vendor = models.ForeignKey(
        'partner.Vendor', related_name='productvendor', blank=True,
        null=True, verbose_name=_("Product Vendor"))
    chapters = models.ManyToManyField(
        Chapter,
        verbose_name=_('Product Structure'),
        through='ProductChapter',
        through_fields=('product', 'chapter'),
        blank=True)
    faqs = models.ManyToManyField(
        FAQuestion,
        verbose_name=_('Product FAQ'),
        through='FAQProduct',
        through_fields=('product', 'question'),
        blank=True)
    attributes = models.ManyToManyField(
        Attribute,
        verbose_name=_('Product Attribute'),
        through='ProductAttribute',
        through_fields=('product', 'attribute'),
        blank=True)
    prices = models.ManyToManyField(
        Currency,
        verbose_name=_('Product Price'),
        through='ProductPrice',
        through_fields=('product', 'currency'),
        blank=True)
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

    def save(self, *args, **kwargs):

        if self.name:
            if not self.title:
                self.title = self.name
            if not self.heading:
                self.heading = self.name
            if not self.image_alt:
                self.image_alt = self.name
        if self.description:
            if not self.meta_desc:
                self.meta_desc = self.get_meta_desc(self.description)
                
        super(Product, self).save(*args, **kwargs)

    @property
    def var_child(self, *args, **kwargs):
        return self.type_product == 2

    @property
    def var_parent(self, *args, **kwargs):
        return self.type_product == 1

    @property
    def is_combo(self, *args, **kwargs):
        return self.type_product == 3

    @property
    def is_virtual(self, *args, **kwargs):
        return self.type_product == 4

    @property
    def is_course(self, *args, **kwargs):
        return self.type_service == 3

    @property
    def is_writing(self, *args, **kwargs):
        return self.type_service == 1

    @property
    def is_service(self, *args, **kwargs):
        return self.type_service == 2

    @property
    def is_others(self, *args, **kwargs):
        return self.type_service == 4

    @property
    def get_bg(self, *args, **kwargs):
        return dict(BG_CHOICES).get(self.image_bg)

    @property
    def get_exp(self, *args, **kwargs):
        return dict(EXP_CHOICES).get(self.experience)

    def pv_name(self, *args, **kwargs):
        if self.type_service == 1:
            return self.name + ' ( ' + self.get_exp + ' ) '
        elif self.type_service == 2:
            return self.name + ' ( ' + self.get_exp + ' ) '
        elif self.type_service == 3:
            return self.name + ' by ' + self.vendor.name
        
        return self.name

    def get_meta_desc(self, description=''):
        if description:
            try:
                import re
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', description)
            except:
                cleantext = ''
        return cleantext

    def get_price(self, *args, **kwargs):
        prices = self.productprices.filter(currency__value=0, active=True)
        if prices:
            return round(prices[0].value, 0)
        return 'Set Price'

    def get_fakeprice(self, *args, **kwargs):
        prices = self.productprices.filter(currency__value=0, active=True)
        if prices:
            inr_price = prices[0].value
            fake_inr_price = prices[0].fake_value
            if inr_price:
                if fake_inr_price > Decimal('0.00'):
                    diff = float(fake_inr_price) - float(inr_price)
                    percent_diff = round((diff / float(fake_inr_price)) * 100, 0)
                    return (round(prices[0].fake_value, 0), percent_diff)
        return None

    @property
    def category_slug(self):
        main_prod_cat = self.categories.filter(
            productcategories__is_main=True,
            productcategories__active=True)
        if main_prod_cat:
            return main_prod_cat[0]
        else:
            prod_cat = self.categories.filter(
                productcategories__is_main=False,
                productcategories__active=True)
            if prod_cat:
                return prod_cat[0]
        return None

    def verify_category(self, cat_slug=None):
        try:
            prod_cat = self.categories.filter(
                slug=cat_slug,
                active=True)
            if prod_cat:
                return prod_cat[0]
            else:
                return self.category_slug
        except:
            pass
        return None

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self, prd_slug=None, cat_slug=None):
        if cat_slug:
            pass
        else:
            cat_slug = self.category_slug
        cat_slug = cat_slug.slug if cat_slug else None
        if self.is_course:
            return reverse('course-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        elif self.is_writing:
            return reverse('resume-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        elif self.is_service:
            return reverse('job-assist-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        else:
            return reverse('other-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def create_icon(self):
        if not self.image:
            return
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (100, 100)
        DJANGO_TYPE = None

        if self.image.name.endswith(".jpg"):
            DJANGO_TYPE = 'image/jpeg'
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif self.image.name.endswith(".png"):
            DJANGO_TYPE = 'image/png'
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            return
        image = Image.open(BytesIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        self.icon.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
        )
        return

    def get_description(self):
        description = self.meta_desc
        if not description:
            description = self.description
        return description.strip()

    
    def get_ratings(self):
        pure_rating = int(self.avg_rating)
        decimal_part = self.avg_rating - pure_rating
        final_score = ['*' for i in range(pure_rating)]
        rest_part = int(Decimal(5.0) - self.avg_rating)
        res_decimal_part = Decimal(5.0) - self.avg_rating - Decimal(rest_part)
        if decimal_part >= 0.75:
            final_score.append("*")
        elif decimal_part >= 0.25:
            final_score.append("+")
        if res_decimal_part >= 0.75:
            final_score.append('-')
        for i in range(rest_part):
            final_score.append('-')
        return final_score

    def get_avg_ratings(self):
        return round(self.avg_rating, 1)

    @property
    def has_attributes(self):
        return self.attributes.exists()

    @property
    def get_type(self):
        return dict(PRODUCT_CHOICES).get(self.type_product)


class ProductArchive(AbstractProduct):
    originalproduct = models.ForeignKey(
        Product,
        verbose_name=_('Original Product'),
        on_delete=models.SET_NULL,
        related_name='originalproduct',
        null=True)
    siblings = models.CharField(
        _('Siblings Product'),
        blank=True,
        max_length=100)
    related = models.CharField(
        _('Related Product'),
        blank=True,
        max_length=100)
    childs = models.CharField(
        _('Child Product'),
        blank=True,
        max_length=100)
    categories = models.CharField(
        _('Product Category'),
        blank=True,
        max_length=100)
    keywords = models.CharField(
        _('Product Keyword'),
        blank=True,
        max_length=100)
    offers = models.CharField(
        _('Product Offer'),
        blank=True,
        max_length=100)
    faqs = models.CharField(
        _('Product Structure'),
        blank=True,
        max_length=100)
    attributes = models.CharField(
        _('Product Attributes'),
        blank=True,
        max_length=100)
    prices = models.CharField(
        _('Product Prices'),
        blank=True,
        max_length=100)
    

    class Meta:
        verbose_name = _('Product Archive')
        verbose_name_plural = _('Product Archives ')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name


class ProductScreen(AbstractProduct):
    originalproduct = models.ForeignKey(
        Product,
        verbose_name=_('Linked Product'),
        on_delete=models.SET_NULL,
        related_name='linkedproduct',
        null=True)
    siblings = models.CharField(
        _('Siblings Product'),
        blank=True,
        max_length=100)
    related = models.CharField(
        _('Related Product'),
        blank=True,
        max_length=100)
    childs = models.CharField(
        _('Child Product'),
        blank=True,
        max_length=100)
    categories = models.CharField(
        _('Product Category'),
        blank=True,
        max_length=100)
    keywords = models.CharField(
        _('Product Keyword'),
        blank=True,
        max_length=100)
    offers = models.CharField(
        _('Product Offer'),
        blank=True,
        max_length=100)
    faqs = models.CharField(
        _('Product Structure'),
        blank=True,
        max_length=100)
    attributes = models.CharField(
        _('Product Attributes'),
        blank=True,
        max_length=100)
    prices = models.CharField(
        _('Product Prices'),
        blank=True,
        max_length=100)
    
    class Meta:
        verbose_name = _('Product Screen')
        verbose_name_plural = _('Product Screens ')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name


class VariationProduct(AbstractAutoDate):
    main = models.ForeignKey(
        Product,
        related_name='mainproduct',
        on_delete=models.CASCADE)
    sibling = models.ForeignKey(
        Product,
        related_name='siblingproduct',
        on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return _("%(pri)s to '%(sec)s'") % {
            'pri': self.main,
            'sec': self.sibling}

    class Meta:
        unique_together = ('main', 'sibling')
        verbose_name = _('Product Variation')
        verbose_name_plural = _('Product Variations')


class RelatedProduct(AbstractAutoDate):
    primary = models.ForeignKey(
        Product,
        related_name='primaryproduct',
        on_delete=models.CASCADE)
    secondary = models.ForeignKey(
        Product,
        related_name='secondaryproduct',
        on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    price_offset = models.DecimalField(
        _('Price Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
    price_offset_percent = models.DecimalField(
        _('% Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
    active = models.BooleanField(default=True)
    type_relation = models.PositiveSmallIntegerField(
        _('Relation'), choices=RELATION_CHOICES, default=0)
    ranking = models.PositiveSmallIntegerField(
        _('Ranking'), default=0,
        help_text=_('Determines order of the products. A product with a higher'
                    ' value will appear before one with a lower ranking.'))

    def __str__(self):
        return _("%(pri)s to '%(sec)s'") % {
            'pri': self.primary,
            'sec': self.secondary}


class ChildProduct(AbstractAutoDate):
    father = models.ForeignKey(
        Product,
        related_name='parentproduct',
        on_delete=models.CASCADE)
    children = models.ForeignKey(
        Product,
        related_name='childrenproduct',
        on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    price_offset = models.DecimalField(
        _('Price Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
    price_offset_percent = models.DecimalField(
        _('% Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return _("%(pri)s to '%(sec)s'") % {
            'pri': self.father,
            'sec': self.children}

    class Meta:
        unique_together = ('father', 'children')
        verbose_name = _('Product Child')
        verbose_name_plural = _('Product Childs')


# class ProductOffer(AbstractAutoDate):
#     offer = models.ForeignKey(
#         Offer,
#         verbose_name=_('Offer'),
#         related_name='offers',
#         on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product,
#         verbose_name=_('Product'),
#         related_name='offerproducts',
#         on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     off_order = models.PositiveIntegerField(
#         _('Offer Order'), default=1)

#     def __str__(self):
#         return _("%(product)s to '%(offer)s'") % {
#             'product': self.product,
#             'offer': self.offer}


class ProductCategory(AbstractAutoDate):
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        related_name='productcategories',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productcategories',
        on_delete=models.CASCADE)
    is_main = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    prd_order = models.PositiveIntegerField(
        _('Product Order'), default=1)
    cat_order = models.PositiveIntegerField(
        _('Category Order'), default=1)

    def __str__(self):
        return _("%(product)s to '%(category)s'") % {
            'product': self.product,
            'category': self.category}

    class Meta:
        unique_together = ('product', 'category')
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


class FAQProduct(AbstractAutoDate):
    question = models.ForeignKey(
        FAQuestion,
        verbose_name=_('FAQuestion'),
        related_name='productfaqs',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productfaqs',
        on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    question_order = models.PositiveIntegerField(
        _('Question Order'), default=1)

    def __str__(self):
        return _("%(product)s to '%(question)s'") % {
            'product': self.product,
            'question': self.question}

    class Meta:
        unique_together = ('product', 'question')
        verbose_name = _('Product FAQ')
        ordering = ('-question_order', 'pk')
        verbose_name_plural = _('Product FAQs')


class ProductAttribute(AbstractAutoDate):
    attribute = models.ForeignKey(
        Attribute,
        verbose_name=_('Attribute'),
        related_name='productattributes',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productattributes',
        on_delete=models.CASCADE)
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
        _('Value Date'),
        max_digits=8, decimal_places=2,
        default=0.0)
    value_ltext = RichTextField(
        verbose_name=_('Value Large Text'), blank=True, default='')
    value_option = models.ForeignKey(
        'shop.AttributeOption', blank=True, null=True,
        verbose_name=_("Value option"))
    value_file = models.FileField(
        upload_to=get_upload_path_product_file, max_length=255,
        blank=True, null=True)
    value_image = models.ImageField(
        upload_to=get_upload_path_product_image, max_length=255,
        blank=True, null=True)
    value_entity = fields.GenericForeignKey(
        'entity_content_type', 'entity_object_id')
    entity_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, editable=False)
    entity_object_id = models.PositiveIntegerField(
        null=True, blank=True, editable=False)

    active = models.BooleanField(default=True)

    def __str__(self):
        return _("%(product)s to '%(attribute)s'") % {
            'product': self.product,
            'attribute': self.attribute}


class ProductPrice(AbstractAutoDate):
    value = models.DecimalField(
        _('Value Price'),
        max_digits=8, decimal_places=2,
        default=0.0)
    fake_value = models.DecimalField(
        _('Value Fake Price'),
        max_digits=8, decimal_places=2,
        default=0.0)
    active = models.BooleanField(default=True)
    currency = models.ForeignKey(
        Currency,
        verbose_name=_('Currency'),
        related_name='productprices',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productprices',
        on_delete=models.CASCADE)

    def __str__(self):
        return _("%(product)s to '%(currency)s'") % {
            'product': self.product,
            'currency': self.currency}

    class Meta:
        unique_together = ('product', 'currency')
        verbose_name = _('Product Currency')
        ordering = ('pk',)
        verbose_name_plural = _('Product Currencies')


class ProductExtraInfo(models.Model):
    """
    Model to add any extra information to a Product.
    """
    info_type = models.CharField(
        max_length=256,
        verbose_name=_('Type'),
    )

    product = models.ForeignKey(
        'shop.Product',
        verbose_name=_('Product'),
    )

    # GFK 'content_object'
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['info_type']

    def __str__(self):
        return '{0} - {1}'.format(self.product, self.type)


class ProductChapter(AbstractAutoDate):
    product = models.ForeignKey(
        Product,
        related_name='productstructure',
        on_delete=models.CASCADE)
    chapter = models.ForeignKey(
        Chapter,
        related_name='productstructure',
        on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return _("%(top)s to '%(cp)s'") % {
            'top': self.product,
            'cp': self.chapter}
    
    class Meta:
        unique_together = ('product', 'chapter')
        verbose_name = _('Product Chapter')
        ordering = ('-sort_order', 'pk')
        verbose_name_plural = _('Product Chapters')
