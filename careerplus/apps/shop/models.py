from django.utils import timezone
from datetime import datetime, date

from decimal import Decimal
from django.db import models
from django.utils.html import strip_tags
from django.utils import six        
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from ckeditor.fields import RichTextField
from seo.models import AbstractSEO, AbstractAutoDate
from meta.models import ModelMeta

from partner.models import Vendor
from faq.models import (
    FAQuestion, ScreenFAQ)
from geolocation.models import Country, Currency, CURRENCY_EXCHANGE
from .managers import (
    ProductManager,
    IndexableProductManager,
    BrowsableProductManager,
    SaleableProductManager)
from .utils import ProductAttributesContainer
from . import choices
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
    RELATION_CHOICES,
    BG_CHOICES,
    C_ATTR_DICT,
    R_ATTR_DICT,
    S_ATTR_DICT,
    convert_to_month,
    convert_inr,
    convert_usd,
    convert_aed,
    convert_gbp)
from search.choices import EXP_DICT

class ProductClass(AbstractAutoDate, AbstractSEO,):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _("Product Class")
        verbose_name_plural = _("Product Classes")

    def __str__(self):
        return self.name

    @property
    def has_attributes(self):
        return self.attributes.exists()


class Category(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
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
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'
        permissions = (
            ("console_add_category", "Can Add Category From Console"),
            ("console_change_category", "Can Change Category From Console"),
            ("console_change_category_seo", "Can Change Category SEO From Console"),
            ("console_change_category_main", "Can Change Category Main From Console"),
            ("console_delete_category_relation", "Can Delete Category Relation From Console"),
        )

    def __str__(self):

        return self.name + '(' + self.get_level + ')'

    @property
    def get_level(self):
        return dict(CATEGORY_CHOICES).get(self.type_level)

    def save(self, *args, **kwargs):
        if self.pk:
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
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(self.description, 'html.parser')
            cleantext = soup.get_text()
            cleantext = cleantext.strip()
        except:
            cleantext = ''
        return cleantext

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        return self.meta_desc

    def get_full_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        if self.is_skill:
            parent = self.get_parent()
            if parent:
                return reverse('skillpage:skill-page-listing',
                    kwargs={'fa_slug': parent[0].slug,'skill_slug': self.slug, 'pk': self.pk})
            return ''
        else:
            return reverse('skillpage:func_area_results',
                kwargs={'fa_slug': self.slug, 'pk': self.pk})

    def add_relationship(self, category):
        relationship, created = CategoryRelationship.objects.get_or_create(
            related_from=self,
            related_to=category,)
        return relationship

    def remove_relationship(self, category):
        CategoryRelationship.objects.filter(
            related_from=self,
            related_to=category).delete()
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
                to_category__active=True,
                type_level=1,
                active=True)
        elif self.type_level == 3:
            return self.related_to.filter(
                to_category__related_from=self,
                to_category__active=True,
                type_level=2,
                active=True)
        elif self.type_level == 4:
            return self.related_to.filter(
                to_category__related_from=self,
                to_category__active=True,
                type_level=3,
                active=True)
        return []

    def get_childrens(self):
        if self.type_level == 1:
            return self.category_set.filter(
                from_category__related_to=self,
                from_category__active=True,
                type_level=2,
                active=True)
        elif self.type_level == 2:
            return self.category_set.filter(
                from_category__related_to=self,
                from_category__active=True,
                type_level=3,
                active=True)
        elif self.type_level == 3:
            return self.category_set.filter(
                from_category__related_to=self,
                from_category__active=True,
                type_level=4,
                active=True)
        return []

    def get_products(self):
        # if self.type_level == 3:
        #     products = self.categoryproducts.filter(
        #         active=True,
        #         productcategories__active=True)
        #     childrens = self.get_childrens()
        #     for child in childrens:
        #         products |= child.categoryproducts.filter(
        #         active=True,
        #         productcategories__active=True)
        # else:
        products = self.categoryproducts.filter(
            active=True,
            productcategories__active=True)

        return products

    def check_products(self):
        if self.type_level == 3:
            products = self.categoryproducts.filter(
                active=True,
                productcategories__active=True)
            childrens = self.get_childrens()
            for child in childrens:
                products |= child.categoryproducts.filter(
                active=True,
                productcategories__active=True)
        else:
            products = self.categoryproducts.filter(
                active=True,
                productcategories__active=True)

        return products

    def split_career_outcomes(self):
        return self.career_outcomes.split(',')

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_childrens().count()

    def create_icon(self):
        if not self.image:
            return
        try:
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
        except:
            pass
        return

    def get_active(self):
        if self.active:
            return 'Active'
        else:
            return 'Inactive'

    def get_skillpage(self):
        if self.is_skill:
            return 'Yes'
        else:
            return 'No'


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
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    is_main_parent = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return _("%(pri)s  ===>  %(sec)s") % {
            'sec': self.related_from,
            'pri': self.related_to}

    class Meta:
        unique_together = ('related_from', 'related_to')
        verbose_name = _('Relationship')
        verbose_name_plural = _('Relationships')


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'), unique=True, max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Attribute Option Group')
        verbose_name_plural = _('Attribute Option Groups')
        


    @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)


class AttributeOption(models.Model):
    group = models.ForeignKey(
        'shop.AttributeOptionGroup', related_name='options',
        verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)
    code = models.CharField(_('Option Code'), max_length=4, unique=True)

    def __str__(self):
        return self.option

    class Meta:
        unique_together = ('group', 'code')
        verbose_name = _('Attribute option')
        verbose_name_plural = _('Attribute options')


class Attribute(AbstractAutoDate):
    product_class = models.ForeignKey(
        ProductClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Product Class'), related_name="attributes",
        help_text=_("Choose what type of product this is"))
    name = models.CharField(
        _('Name'), max_length=100,
        unique=True,
        help_text=_('Unique name going to decide the slug'))
    display_name = models.CharField(
        _('Display Name'), max_length=100,
        help_text=_('Name going to displayed'))
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    OPTION = "option"
    MULTI_OPTION = "multi_option"
    ENTITY = "entity"
    FILE = "file"
    IMAGE = "image"
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (OPTION, _("Option")),
        # (MULTI_OPTION, _("Multi Option")),
        (ENTITY, _("Entity")),
        (FILE, _("File")),
        (IMAGE, _("Image")),
    )
    type_attribute = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("Type"))
    required = models.BooleanField(_('Required'), default=False)
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


    is_visible = models.BooleanField(default=True)
    is_multiple = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_indexable = models.BooleanField(default=True)
    is_filterable = models.BooleanField(default=True)
    is_sortable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Atrribute')
        verbose_name_plural = _('Attributes')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'
        permissions = (
            ("console_add_attribute", "Can Add Attribute From Console"),
            ("console_change_attribute", "Can Change Attribute From Console"),
        )

    @property
    def get_class(self):
        if self.product_class:
            return self.product_class.name
        return ''

    @property
    def get_type(self):
        return self.type_attribute
        


    def _get_value(self):
        value = getattr(self, 'value_%s' % self.attribute.type_attribute)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        if self.attribute.is_option and isinstance(new_value, six.string_types):
            new_value = self.attribute.option_group.options.get(
                option=new_value)
        setattr(self, 'value_%s' % self.attribute.type_attribute, new_value)

    value = property(_get_value, _set_value)

    
    def __str__(self):
        return self.name

    @property
    def is_option(self):
        return self.type_attribute == self.OPTION

    @property
    def is_multi_option(self):
        return self.type_attribute == self.MULTI_OPTION

    @property
    def is_file(self):
        return self.type_attribute in [self.FILE, self.IMAGE]

    def __str__(self):
        return self.name

    def save_screen_value(self, productscreen, value):

        from shop.models import ProductAttributeScreen
        try:
            value_obj = productscreen.screenattributes.get(attribute=self)
        except ProductAttributeScreen.DoesNotExist:
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttributeScreen.objects.create(
                product=productscreen, attribute=self)

        if self.is_file:
            if value is None:
                return
            elif value is False:
                value_obj.delete()
            else:
                value_obj.value = value
                value_obj.save()
        elif self.is_multi_option:
            if value is None:
                value_obj.delete()
                return
            try:
                count = value.count()
            except (AttributeError, TypeError):
                count = len(value)
            if count == 0:
                value_obj.delete()
            else:
                value_obj.value = value
                value_obj.save()
        else:
            if value is None or value == '':
                value_obj.delete()
                return
            if value != value_obj.value:
                value_obj.value = value
                value_obj.save()

    
    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type_attribute)
        validator(value)

    def save_value(self, product, value):

        from shop.models import ProductAttribute
        try:
            value_obj = product.productattributes.get(attribute=self)
        except ProductAttribute.DoesNotExist:
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttribute.objects.create(
                product=product, attribute=self)

        if self.is_file:
            if value is None:
                return
            elif value is False:
                value_obj.delete()
            else:
                value_obj.value = value
                value_obj.save()
        elif self.is_multi_option:
            if value is None:
                value_obj.delete()
                return
            try:
                count = value.count()
            except (AttributeError, TypeError):
                count = len(value)
            if count == 0:
                value_obj.delete()
            else:
                value_obj.value = value
                value_obj.save()
        else:
            if value is None or value == '':
                value_obj.delete()
                return
            if value != value_obj.value:
                value_obj.value = value
                value_obj.save()

    
    def _validate_text(self, value):
        from django.utils import six
        if not isinstance(value, six.string_types):
            raise ValidationError(_("Must be str or unicode"))
    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise ValidationError(_("Must be a model instance"))

    def _validate_multi_option(self, value):
        try:
            values = iter(value)
        except TypeError:
            raise ValidationError(
                _("Must be a list or AttributeOption queryset"))
        valid_values = self.option_group.options.values_list(
            'option', flat=True)
        for value in values:
            self._validate_option(value, valid_values=valid_values)

    def _validate_option(self, value, valid_values=None):
        from shop.models import AttributeOption
        if not isinstance(value, AttributeOption):
            raise ValidationError(
                _("Must be an AttributeOption model object instance"))
        if not value.pk:
            raise ValidationError(_("AttributeOption has not been saved yet"))
        if valid_values is None:
            valid_values = self.option_group.options.values_list(
                'option', flat=True)
        if value.option not in valid_values:
            raise ValidationError(
                _("%(enum)s is not a valid choice for %(attr)s") %
                {'enum': value, 'attr': self})

    def _validate_file(self, value):
        from django.core.files.base import File
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))
    _validate_image = _validate_file


class Keyword(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'
        permissions = (
            ("console_add_keyword", "Can Add Keyword From Console"),
            ("console_change_keyword", "Can Change Keyword From Console"),
        )


class AbstractProduct(AbstractAutoDate, AbstractSEO):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    cp_id = models.IntegerField(
        _('CP Variation'),
        blank=True,
        null=True,
        editable=False)
    cpv_id = models.IntegerField(
        _('CP Variation'),
        blank=True,
        null=True,
        editable=False)
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    fixed_slug = models.BooleanField(default=False)

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
    prg_structure = RichTextField(
        verbose_name=_('Program Structure'), blank=True, default='')
    
    inr_price = models.DecimalField(
        _('INR Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    fake_inr_price = models.DecimalField(
        _('Fake INR Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    usd_price = models.DecimalField(
        _('USD Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    fake_usd_price = models.DecimalField(
        _('Fake USD Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    aed_price = models.DecimalField(
        _('AED Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    fake_aed_price = models.DecimalField(
        _('Fake AED Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    gbp_price = models.DecimalField(
        _('GBP Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    fake_gbp_price = models.DecimalField(
        _('Fake GBP Price'),
        max_digits=12, decimal_places=2,
        default=0.0) 
    
    class Meta:
        abstract = True

    @property
    def get_type(self):
        return dict(PRODUCT_CHOICES).get(self.type_product)

    def get_product_class(self):
        return self.product_class
    
    @property
    def var_child(self):
        return self.type_product == 2

    @property
    def var_parent(self):
        return self.type_product == 1

    @property
    def is_combo(self):
        return self.type_product == 3

    @property
    def is_virtual(self):
        return self.type_product == 4

    def get_active(self):
        if self.active:
            return 'Active'
        else:
            return 'Inactive'

    def get_vendor(self):
        if self.vendor:
            return self.vendor.name
        else:
            return ''

    @property
    def has_attributes(self):
        return self.attributes.exists()


class Product(AbstractProduct, ModelMeta):
    product_class = models.ForeignKey(
        ProductClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Product Class'), related_name="products",
        help_text=_("Choose what type of product this is"))
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
    keywords = models.ManyToManyField(
        'shop.Keyword',
        verbose_name=_('Product Keyword'),
        related_name='productkeyword',
        blank=True)
    categories = models.ManyToManyField(
        'shop.Category',
        verbose_name=_('Product Category'),
        through='ProductCategory',
        through_fields=('product', 'category'),
        blank=True)
    related = models.ManyToManyField(
        'self',
        through='RelatedProduct',
        related_name='relatedproduct',
        through_fields=('primary', 'secondary'),
        verbose_name=_('Related Product'),
        symmetrical=False, blank=True)
    childs = models.ManyToManyField(
        'self',
        through='ChildProduct',
        related_name='comboproduct',
        through_fields=('father', 'children'),
        verbose_name=_('Child Product'),
        symmetrical=False, blank=True)
    
    vendor = models.ForeignKey(
        'partner.Vendor', related_name='productvendor', blank=True,
        null=True, verbose_name=_("Product Vendor"))
    countries = models.ManyToManyField(
        Country,
        verbose_name=_('Country Available'),
        related_name='countryavailable',
        blank=True)
    variation = models.ManyToManyField(
        'self',
        through='VariationProduct',
        related_name='variationproduct',
        through_fields=('main', 'sibling'),
        verbose_name=_('Variation Product'),
        symmetrical=False, blank=True)
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
    archive_json = models.TextField(
        _('Archive JSON'),
        blank=True,
        editable=False
        )
    cp_page_view = models.IntegerField(
        _('CP Page View'),default= 0)
    active = models.BooleanField(default=False)
    is_indexable = models.BooleanField(default=False)

    objects = ProductManager()
    indexable = IndexableProductManager()
    saleable = SaleableProductManager()
    browsable = BrowsableProductManager()

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'title',
        'description': 'meta_desc',
        'og_description': 'meta_desc',
        'keywords': 'meta_keywords',
        'published_time': 'created',
        'modified_time': 'modified',
        'url': 'get_absolute_url',
    }

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'
        permissions = (
            ("console_add_product", "Can Add Product From Console"),
            ("console_change_product", "Can Change Product From Console"),
            ("console_moderate_product", "Can Moderate Product From Console"),
            ("console_delete_product_relations", "Can Delete Product From Console"),
            ("console_live_product", "Can Live Product From Console"),
        )

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        if self.product_class:
            self.attr = ProductAttributesContainer(product=self)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            if self.name:    
                if not self.heading:
                    self.heading = self.get_heading()
                if not self.title:
                    self.title = self.get_title()
                if not self.image_alt:
                    self.image_alt = self.name
                if not self.meta_desc:
                    self.meta_desc = self.get_meta_desc()
        super(Product, self).save(*args, **kwargs)
        if getattr(self, 'attr', None):
            self.attr.save()

    @property
    def category_main(self):
        main_prod_cat = self.categories.filter(
            productcategories__is_main=True,
            productcategories__active=True,
            active=True)
        if main_prod_cat:
            if main_prod_cat[0].type_level == 4:
                main_prod_cat = main_prod_cat[0].get_parent()[0] if main_prod_cat[0].get_parent() else None 
                return main_prod_cat
            return main_prod_cat[0]
        else:
            prod_cat = self.categories.filter(
                productcategories__is_main=False,
                productcategories__active=True,
                active=True)
            if prod_cat:
                if prod_cat[0].type_level == 4:
                    prod_cat = prod_cat[0].get_parent()[0] if prod_cat[0].get_parent() else None 
                    return prod_cat
                return prod_cat[0]
        return None

    def category_attached(self):
        main_prod_cat = self.categories.filter(
            productcategories__is_main=True,
            productcategories__active=True,
            active=True)
        if main_prod_cat:
            return main_prod_cat[0]
        else:
            prod_cat = self.categories.filter(
                productcategories__is_main=False,
                productcategories__active=True,
                active=True)
            if prod_cat:
                return prod_cat[0]
        return None

    @property
    def is_course(self):
        if self.product_class and self.product_class.slug in settings.COURSE_SLUG:
            return True
        else:
            return False
    @property
    def is_writing(self):
        if self.product_class and self.product_class.slug in settings.WRITING_SLUG:
            return True
        else:
            return False

    @property
    def is_service(self):
        if self.product_class and self.product_class.slug in settings.SERVICE_SLUG:
            return True
        else:
            return False

    @property
    def get_name(self):
        # display name
        return self.heading if self.heading else self.name

    def get_heading(self):
        if self.is_course:
            return '%s Certification Course' % (
                self.name,
            )
        elif self.is_service or self.is_writing:
            if self.category_main:
                return '%s  for %s' % (
                    self.category_main.name,
                    EXP_DICT.get(self.get_exp(), ''),
                )

        return ''

    def get_title(self):
        if self.is_course:
            return '%s Certification Course INR %s  Learning.Shine' % (
                self.name,
                str(round(self.inr_price, 0)),
            )
        elif self.is_service or self.is_writing:
            if self.category_main:
                try:
                    return dict(getattr(choices, choice))[int(value) if value.isdigit() else value]
                except:
                    return 'Others'

                return '%s -  for %s -  Online Services  Learning.Shine' % (
                    self.category_main.name,
                    EXP_DICT.get(self.get_exp(), ''),
                )            
        return ''

    def get_meta_desc(self):
        if self.is_course:
            return '%s - Get Online Access, Supports from Experts, Study Materials, course module, fee structure and other details at Learning.Shine' % (
                self.name,
            )
        elif self.is_service or self.is_writing:
            if self.category_main:
                return 'Online %s - Services for %s. Get expert advice & tips for %s at learning.shine' % (
                        self.category_main.name,
                        EXP_DICT.get(self.get_exp(), ''),
                        self.category_main.name,
                    )            
        
        return ''

    def get_icon_url(self, relative=False):
        if self.icon:
            return self.get_full_url(url=self.icon.url) if not relative else self.icon.url
        return ''

    def get_image_url(self, relative=False):
        if self.image:
            return self.get_full_url(url=self.image.url) if not relative else self.image.url
        return '/media/attachment/default_product_image.jpg'
    
    def get_url(self, relative=False):
        return self.get_full_url(self.get_absolute_url()) if not relative else self.get_absolute_url()

    def get_absolute_url(self, prd_slug=None, cat_slug=None):
        if not cat_slug:
            cat_slug = self.category_main
            cat_slug = cat_slug.get_parent()
        cat_slug = cat_slug.slug if cat_slug else None
        if self.is_course:
            return reverse('course-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        else:
            return reverse('service-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})

        # else self.is_writing:
        #     return reverse('resume-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        # elif self.is_service:
        #     return reverse('job-assist-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})
        # else:
        #     return reverse('other-detail', kwargs={'prd_slug': self.slug, 'cat_slug': cat_slug, 'pk': self.pk})

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
        AR = float(self.avg_rating)
        if 0.0 <= AR <= 0.5:
            return 0
        elif 0.5 < AR <= 1.5:
            return 1
        elif 1.5 < AR <= 2.5:
            return 2
        elif 2.5 < AR <= 3.5:
            return 3
        elif 3.5 < AR <= 4.5:
            return 4
        elif 4.5 < AR <= 5.0:
            return 5
        else:
            return 2.5
    def get_screen(self):
        if self.screenproduct.all().exists():
            return self.screenproduct.all()[0]
        else:
            return None

    @property
    def get_bg(self):
        return dict(BG_CHOICES).get(self.image_bg)

    def pv_name(self):
        if self.is_course:
            return self.name + ' ( ' + str(EXP_DICT.get(self.get_exp(), '')) + ' ) '
        elif self.is_writing:
            return self.name + ' ( ' + str(EXP_DICT.get(self.get_exp(), '')) + ' ) '
        elif self.is_course:
            return self.name + ' by ' + self.vendor.name
        return self.name

    def get_price(self):
        
        if self.inr_price:
            return round(self.inr_price, 0)
        return Decimal(0)

    def get_fakeprice(self):
        if self.inr_price:
            inr_price = self.inr_price
            fake_inr_price = self.fake_inr_price
            if fake_inr_price > Decimal('0.00'):
                diff = float(fake_inr_price) - float(inr_price)
                percent_diff = round((diff / float(fake_inr_price)) * 100, 0)
                return (round(fake_inr_price, 0), percent_diff)
        return None

    def verify_category(self, cat_slug=None):
        try:
            prod_cat = Category.objects.filter(
                slug=cat_slug,
                active=True)
            if prod_cat:
                return prod_cat[0]
            else:
                return self.category_main
        except:
            pass
        return None

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

    def get_parent(self):
        if self.type_product == 2:
            return self.variationproduct.all()[0] if self.variationproduct.exists() else None
        else:
            return None

    def get_variations(self):
        if self.type_product == 1:
            return self.variation.filter(
                siblingproduct__active=True, active=True).order_by('-siblingproduct__sort_order')
        else:
            return []

    def get_fbts(self):
        if self.type_product in [0, 1, 3, 5]:
            return self.related.filter(
                secondaryproduct__active=True, active=True).order_by('-secondaryproduct__sort_order')
        else:
            return []

    def get_combos(self):
        if self.type_product == 3:
            return self.childs.filter(
                active=True, childrenproduct__active=True).order_by('-childrenproduct__sort_order')
        else:
            return []

    def get_pops(self):
        # Products from other vendors
        if self.type_product in [0, 1, 3, 5]:
            category = self.category_attached()
            if category:
                if self.is_course:
                    pop_list = category.get_products().filter(
                        type_product__in=[0,1,3,5]).exclude(vendor=self.vendor).distinct()
                    return pop_list
                elif self.is_writing or self.is_service:
                    pop_list = category.get_products().filter(
                        type_product__in=[0,1,3,5]).exclude(pk=self.pk).distinct()
                    return pop_list
            return []
        else:
            return []

    def get_delivery_types(self):
        delivery_objs = self.productextrainfo_set.filter(info_type='delivery_service')
        delivery_obj_ids = list(delivery_objs.all().values_list('object_id', flat=True))

        delivery_services = DeliveryService.objects.filter(
            id__in=delivery_obj_ids, active=True)

        flag = delivery_services.filter(
            slug="normal", inr_price=0.0,
            usd_price=0.0, aed_price=0.0,
            gbp_price=0.0).exists()
        if flag and delivery_services.count() > 1:
            return delivery_services.order_by('inr_price')
        else:
            return delivery_services.none()

    def get_exp(self):
        # for code return
        if self.is_writing:
            return getattr(self.attr, R_ATTR_DICT.get('EXP')).code \
                if getattr(self.attr, R_ATTR_DICT.get('EXP'), None) \
                else ''
        elif self.is_service:
            return getattr(self.attr, S_ATTR_DICT.get('EXP')).code \
                if getattr(self.attr, S_ATTR_DICT.get('EXP'), None) \
                else ''
        else:
            return ''

    def get_exp_db(self):
        # return display value
        if self.is_writing:
            return choices.EXP_DICT.get(getattr(self.attr, R_ATTR_DICT.get('EXP')).code) \
                if getattr(self.attr, R_ATTR_DICT.get('EXP'), None) \
                else ''
        elif self.is_service:
            return choices.EXP_DICT.get(getattr(self.attr, S_ATTR_DICT.get('EXP')).code) \
                if getattr(self.attr, S_ATTR_DICT.get('EXP'), None) \
                else ''
        else:
            return ''

    def get_studymode(self):
        # for Solr
        if self.is_course:
            return getattr(self.attr, C_ATTR_DICT.get('SM')).code \
                if getattr(self.attr, C_ATTR_DICT.get('SM'), None) \
                else ''
        else:
            return ''

    def get_studymode_db(self):
        # return display value
        if self.is_course:
            return choices.STUDY_MODE.get(getattr(self.attr, C_ATTR_DICT.get('SM')).code)\
                if getattr(self.attr, C_ATTR_DICT.get('SM'), None) \
                else ''
        else:
            return ''

    def get_courselevel(self):
        # return code
        if self.is_course:
            return getattr(self.attr, C_ATTR_DICT.get('CL')).code \
                if getattr(self.attr, C_ATTR_DICT.get('CL'), None) \
                else ''
        else:
            return ''

    def get_courselevel_db(self):
        # for db return display value
        if self.is_course:
            return getattr(self.attr, C_ATTR_DICT.get('CL')) \
                if getattr(self.attr, C_ATTR_DICT.get('CL'), None) \
                else ''
        else:
            return ''
    
    def get_coursetype(self):
        if self.is_course:
            return getattr(self.attr, C_ATTR_DICT.get('CT')).code \
                if getattr(self.attr, C_ATTR_DICT.get('CT'), None) \
                else ''
        else:
            return ''

    def get_coursetype_db(self):
        # return dispaly value
        if self.is_course:
            return choices.COURSE_TYPE_DICT.get(getattr(self.attr, C_ATTR_DICT.get('CT')).code) \
                if getattr(self.attr, C_ATTR_DICT.get('CT'), None) \
                else ''
        else:
            return ''

    def get_cert(self):
        if self.is_course:
            return getattr(self.attr, C_ATTR_DICT.get('CERT')) \
                if getattr(self.attr, C_ATTR_DICT.get('CERT'), None) \
                else 0
        else:
            return 0

    def get_duration(self):
        if self.is_course:
            dd = getattr(self.attr, C_ATTR_DICT.get('DD')) \
                if getattr(self.attr, C_ATTR_DICT.get('DD'), None) \
                else 0
            return convert_to_month(dd)
        else:
            return ''

    def get_duration_db(self):
        # return display value
        if self.is_course:
            dd = getattr(self.attr, C_ATTR_DICT.get('DD')) \
                if getattr(self.attr, C_ATTR_DICT.get('DD'), None) \
                else 0
            return choices.DURATION_DICT.get(convert_to_month(dd))
        else:
            return ''

    def get_profile_country(self):
        pf_obj = self.productextrainfo_set.filter(info_type='profile_update')
        if pf_obj:
            return Country.objects.get(pk=pf_obj[0].object_id).code2
        else:
            return ''

    def get_delivery(self):
        pf_obj = self.productextrainfo_set.filter(info_type='delivery_service')
        if pf_obj:
            return ''
            # country_obj = Country.objects.filter(pk=profile_obj.object_id)[0].code2 
        else:
            return ''

    def get_inr_price(self):
        price = self.inr_price

        return convert_inr(price)

    def get_usd_price(self):
        if self.usd_price:
            price = self.usd_price
        else:
            price = self.inr_price * dict(CURRENCY_EXCHANGE).get('US')
        return convert_usd(price)    
    
    def get_aed_price(self):
        if self.aed_price:
            price = self.aed_price
        else:
            price = self.inr_price * dict(CURRENCY_EXCHANGE).get('AE')
        return convert_aed(price)
    
    def get_gbp_price(self):
        if self.gbp_price:
            price = self.gbp_price
        else:
            price = self.inr_price * dict(CURRENCY_EXCHANGE).get('GB')
        return convert_gbp(price)

    def get_canonical_url(self):
        return self.get_absolute_url()

class ProductScreen(AbstractProduct):
    product_class = models.ForeignKey(
        ProductClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Product Class'), related_name="productscreens",
        help_text=_("Choose what type of product this is"))
    product = models.ForeignKey(
        Product,
        verbose_name=_('Original Product'),
        on_delete=models.SET_NULL,
        related_name='screenproduct',
        null=True)
    comment = RichTextField(
        verbose_name=_('Comments'), blank=True, default='')
    
    STATUS_CHOICES = (
        (6, _('Reverted')),
        (5, _('Rejected')),
        (4, _('InActive')),
        (3, _('Active')),
        (2, _('Moderation')),
        (1, _('Changed')),
        (0, _('Added')),)
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only product with their status set to 'Active' will be "
                    "displayed."))
    vendor = models.ForeignKey(
        'partner.Vendor', related_name='screenvendor', blank=True,
        null=True, verbose_name=_("Product Vendor"))
    countries = models.ManyToManyField(
        Country,
        verbose_name=_('Country Available'),
        related_name='countryscreen',
        blank=True)
    variation = models.ManyToManyField(
        'self',
        through='VariationProductScreen',
        related_name='variationproduct',
        through_fields=('main', 'sibling'),
        verbose_name=_('Variation Product'),
        symmetrical=False, blank=True)
    faqs = models.ManyToManyField(
        FAQuestion,
        verbose_name=_('Product FAQ'),
        through='FAQProductScreen',
        through_fields=('product', 'question'),
        blank=True)
    attributes = models.ManyToManyField(
        Attribute,
        verbose_name=_('Product Attribute'),
        through='ProductAttributeScreen',
        through_fields=('product', 'attribute'),
        blank=True)
    
    class Meta:
        verbose_name = _('Product Screen')
        verbose_name_plural = _('Product Screens ')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __init__(self, *args, **kwargs):
        super(ProductScreen, self).__init__(*args, **kwargs)
        if self.product_class:
            self.attr = ProductAttributesContainer(product=self)

    def save(self, *args, **kwargs):
        super(ProductScreen, self).save(*args, **kwargs)
        if getattr(self, 'attr', None):
            self.attr.save_screen()


    def __str__(self):
        return self.name
    
    def create_product(self):
        if not self.product:
            if self.name and self.product_class:
                product = Product.objects.create(
                    name=self.name,
                    product_class=self.product_class,
                    type_product=self.type_product,
                    upc=self.upc,
                    vendor=self.vendor,
                    inr_price=self.inr_price)
                self.product = product
                self.save()
        return self.product

    def add_variant(self, variant):
        if self.type_product == 1:
            if variant.type_product == 2:
                variation, created = VariationProductScreen.objects.get_or_create(
                    main=self,
                    sibling=variant,)
                return True
        return False


    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def get_parent(self):
        if self.type_product == 2:
            return self.variationproduct.all()[0] if self.variationproduct.exists() else None
        else:
            return None


# class ProductArchive(AbstractProduct):
#     product = models.ForeignKey(
#         Product,
#         verbose_name=_('Original Product'),
#         on_delete=models.SET_NULL,
#         related_name='archiveproduct',
#         null=True)
    

#     class Meta:
#         verbose_name = _('Product Archive')
#         verbose_name_plural = _('Product Archives ')
#         ordering = ("-modified", "-created")
#         get_latest_by = 'created'

#     def __str__(self):
#         return self.name


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
        return _("%(category)s ==> '%(product)s'") % {
            'product': self.product,
            'category': self.category}

    class Meta:
        unique_together = ('product', 'category')
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


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


class VariationProductScreen(AbstractAutoDate):
    main = models.ForeignKey(
        ProductScreen,
        related_name='mainproduct',
        on_delete=models.CASCADE)
    sibling = models.ForeignKey(
        ProductScreen,
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
        verbose_name = _('Product Screen Variation')
        verbose_name_plural = _('Product Screen Variations')

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
        _('Text'), max_length=100,
        blank=True)
    value_integer = models.PositiveSmallIntegerField(
        _('Integer'), default=0)
    value_image = models.ImageField(
        _('Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    value_boolean = models.BooleanField(
        _('Boolean'), default=False)
    value_file = models.ImageField(
        _('File'), upload_to=get_upload_path_product_file,
        blank=True, null=True)
    value_date = models.DateTimeField(
        _('Date'), blank=True, null=True)
    value_ltext = RichTextField(
        verbose_name=_('Rich Text'), blank=True, default='')
    value_option = models.ForeignKey(
        'shop.AttributeOption', blank=True, null=True,
        verbose_name=_("Value option"))
    value_multi_option = models.ManyToManyField(
        'shop.AttributeOption', blank=True,
        related_name='multi_valued_attribute_screen_values',
        verbose_name=_("Value multi option"))
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

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.attribute.type_attribute)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        if self.attribute.is_option and isinstance(new_value, six.string_types):
            new_value = self.attribute.option_group.options.get(
                option=new_value)
        setattr(self, 'value_%s' % self.attribute.type_attribute, new_value)

    value = property(_get_value, _set_value)


    def __str__(self):
        return _("%(product)s to '%(attribute)s'") % {
            'product': self.product,
            'attribute': self.summary()}

    def summary(self):
        return u"%s: %s" % (self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        property_name = '_%s_as_text' % self.attribute.type_attribute
        return getattr(self, property_name, self.value)

    @property
    def _multi_option_as_text(self):
        return ', '.join(str(option) for option in self.value_multi_option.all())

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)

    @property
    def _entity_as_text(self):
        return six.text_type(self.value)


class ProductAttributeScreen(AbstractAutoDate):
    attribute = models.ForeignKey(
        Attribute,
        verbose_name=_('Attribute'),
        related_name='screenattributes',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductScreen,
        verbose_name=_('Product'),
        related_name='screenattributes',
        on_delete=models.CASCADE)
    value_text = models.CharField(
        _('Value Text'), max_length=100,
        blank=True)
    value_integer = models.PositiveSmallIntegerField(
        _('Value Integer'), default=0)
    value_image = models.ImageField(
        _('Value Image'), upload_to=get_upload_path_product_image,
        blank=True, null=True)
    value_boolean = models.BooleanField(
        _('Boolean'), default=False)
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
    value_multi_option = models.ManyToManyField(
        'shop.AttributeOption', blank=True,
        related_name='multi_valued_attribute_values',
        verbose_name=_("Value multi option"))
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

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.attribute.type_attribute)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        if self.attribute.is_option and isinstance(new_value, six.string_types):
            new_value = self.attribute.option_group.options.get(
                option=new_value)
        setattr(self, 'value_%s' % self.attribute.type_attribute, new_value)

    value = property(_get_value, _set_value)


    def __str__(self):
        return _("%(product)s to '%(attribute)s'") % {
            'product': self.product,
            'attribute': self.summary()}

    def summary(self):
        return u"%s: %s" % (self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        property_name = '_%s_as_text' % self.attribute.type_attribute
        return getattr(self, property_name, self.value)

    @property
    def _multi_option_as_text(self):
        return ', '.join(str(option) for option in self.value_multi_option.all())

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)

    @property
    def _entity_as_text(self):
        return six.text_type(self.value)


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
        return _("'%(question)s'") % {
            'question': self.question}

    class Meta:
        unique_together = ('product', 'question')
        verbose_name = _('Product FAQ')
        ordering = ('-question_order', 'pk')
        verbose_name_plural = _('Product FAQs')


class FAQProductScreen(AbstractAutoDate):
    question = models.ForeignKey(
        FAQuestion,
        verbose_name=_('FAQuestion'),
        related_name='screenfaqs',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductScreen,
        verbose_name=_('Product'),
        related_name='screenfaqs',
        on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    question_order = models.PositiveIntegerField(
        _('Question Order'), default=1)

    def __str__(self):
        return _("'%(question)s'") % {
            'question': self.question}

    class Meta:
        unique_together = ('product', 'question')
        verbose_name = _('Product Screen FAQ')
        ordering = ('-question_order', 'pk')
        verbose_name_plural = _('Product Screen FAQs')


class ProductExtraInfo(models.Model):
    """
    Model to add any extra information to a Product.
    """
    CHOICES = (
        ('default', 'Default'),
        ('profile_update', 'Profile Update Country'),
        ('delivery_service', 'Delivery Service'),)

    info_type = models.CharField(
        choices=CHOICES,
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
        return '{0} - {1}'.format(self.product, self.info_type)


class Chapter(AbstractAutoDate):
    STATUS_CHOICES = (
        (2, _('Active')),
        (1, _('Inactive')),
        (0, _('Moderation')),)

    heading = models.CharField(_('chapter'), max_length=255)
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    
    ordering = models.PositiveSmallIntegerField(
        _('ordering'), default=1,
        help_text=_(u'An integer used to order the chapter \
            amongst others related to the same chapter. If not given this \
            chapter will be last in the list.'))
    status = models.BooleanField(
        _('status'),
        default=False,
        help_text=_("Only questions with 'Active' will be "
                    "displayed."))
    product = models.ForeignKey(
        Product,
        related_name='chapter_product',
        null=True, blank=True)
    
    class Meta:
        ordering = ['ordering']
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')
        permissions = (
            ("console_add_chapter", "Can Add Product Chapter From Console"),
            ("console_change_chapter", "Can Change Product Chapter From Console"),
            ("console_moderate_chapter", "Can Moderate Product Chapter From Console"),
            )
    
    def __str__(self):
        return (self.heading[:75] + '...') if len(self.heading) > 75 else self.heading
    
    def get_screen(self):
        if self.orig_ch.exists():
            return self.orig_ch.all()[0]
        else:
            return None

    def create_screen(self):
        if not self.get_screen():
            if self.heading and self.product:
                schapter = ScreenChapter.objects.create(
                    heading=self.heading,
                    answer=self.answer,
                    status=self.status,
                    product=self.product.get_screen(),
                    ordering=self.ordering,
                    chapter=self)
                return schapter
        return self.get_screen()
    

class ScreenChapter(AbstractAutoDate):
    STATUS_CHOICES = (
        (2, _('Active')),
        (1, _('Inactive')),
        (0, _('Moderation')),)

    heading = models.CharField(_('chapter'), max_length=255)
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    
    ordering = models.PositiveSmallIntegerField(
        _('ordering'), default=1,
        help_text=_(u'An integer used to order the chapter \
            amongst others related to the same chapter. If not given this \
            chapter will be last in the list.'))
    status = models.BooleanField(
        _('status'),
        default=False,
        help_text=_("Only questions with 'Active' will be "
                    "displayed."))
    
    product = models.ForeignKey(
        ProductScreen,
        related_name='chapter_product',
        null=True, blank=True)
    chapter = models.ForeignKey(
        Chapter,
        related_name='orig_ch',
        null=True, blank=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = _('Screen Chapter')
        verbose_name_plural = _('Screen Chapters')
    
    def __str__(self):
        return (self.heading[:75] + '...') if len(self.heading) > 75 else self.heading
    
    def create_chapter(self):
        if not self.chapter:
            if self.heading and self.product:
                chapter = Chapter.objects.create(
                    heading=self.heading,
                    answer=self.answer,
                    status=self.status,
                    product=self.product.product,
                    ordering=self.ordering)
                self.chapter = chapter
                self.save()
                return chapter
        return self.chapter


class DeliveryService(AbstractAutoDate, AbstractSEO):
    name = models.CharField(
        _('Delivery Service Name'), max_length=200,
        help_text=_('Name will be unique to decide slug'))

    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=250, help_text=_('Unique slug'))

    inr_price = models.DecimalField(
        _('INR Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    usd_price = models.DecimalField(
        _('USD Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    aed_price = models.DecimalField(
        _('AED Price'),
        max_digits=12, decimal_places=2,
        default=0.0)
    gbp_price = models.DecimalField(
        _('GBP Price'),
        max_digits=12, decimal_places=2,
        default=0.0)

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_price(self, *args, **kwargs):
        
        if self.inr_price:
            return round(self.inr_price, 0)
        return Decimal(0)


class FunctionalArea(AbstractAutoDate, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100, unique=True)
    faproducts = models.ManyToManyField(
        'shop.Product',
        verbose_name=_('FA Product'),
        through='ProductFA',
        through_fields=('fa', 'product'),
        blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('FA')
        verbose_name_plural = _('FAs')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_products(self):
        products = self.faproducts.filter(
            active=True,
            productfas__active=True)
        return products


class ProductFA(AbstractAutoDate):
    fa = models.ForeignKey(
        FunctionalArea,
        verbose_name=_('FA'),
        related_name='productfas',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productfas',
        on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'fa')
        verbose_name = _('Product FA')
        verbose_name_plural = _('Product FAs')


class Skill(AbstractAutoDate, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100, unique=True)
    skillproducts = models.ManyToManyField(
        'shop.Product',
        verbose_name=_('Skill Product'),
        through='ProductSkill',
        through_fields=('skill', 'product'),
        blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def get_products(self):
        products = self.skillproducts.filter(
            active=True,
            productskills__active=True)
        return products


class ProductSkill(AbstractAutoDate):
    skill = models.ForeignKey(
        Skill,
        verbose_name=_('Skill'),
        related_name='productskills',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='productskills',
        on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'skill')
        verbose_name = _('Product Skill')
        verbose_name_plural = _('Product Skills')


