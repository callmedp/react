from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType

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
    SERVICE_CHOICES,
    CATEGORY_CHOICES,
    PRODUCT_CHOICES,
    FLOW_CHOICES,
    EXP_CHOICES,
    ATTRIBUTE_CHOICES,
    RELATION_CHOICES)


class Category(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    type_service = models.PositiveSmallIntegerField(
        _('Entity'), choices=SERVICE_CHOICES, default=0)
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

    def get_relationships(self, relation):
        return self.related_to.filter(
            to_category__relation=relation,
            to_category__related_from=self)

    def get_related_to(self, relation):
        return self.related_to.filter(
            from_category__relation=relation,
            from_category__related_to=self)

    def get_parent(self):
        return self.get_relationships(0)

    def get_childrens(self):
        return self.get_related_to(0)

    def get_main_parent(self):
        return self.related_to.filter(
            from_category__relation=0, from_category__related_to=self,
            is_main_parent=True)

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_childrens().count()


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


class Entity(AbstractAutoDate, AbstractSEO):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    
    class Meta:
        ordering = ['name']
        verbose_name = _("Product class")
        verbose_name_plural = _("Product classes")

    def __str__(self):
        return self.name

    @property
    def has_attributes(self):
        return self.attributes.exists()


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
    entity = models.ForeignKey(
        'shop.Entity', related_name='attributes', blank=True,
        null=True, verbose_name=_("Entity"))
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


# class Offer(AbstractAutoDate):
#     name = models.CharField(
#         _('Name'), max_length=100)
#     display_text = models.TextField(_('Display Text'), blank=True, default='')
#     active = models.BooleanField(default=True)
#     offerproducts = models.ManyToManyField(
#         'shop.Product',
#         verbose_name=_('Offer Product'),
#         through='ProductOffer',
#         through_fields=('offer', 'product'),
#         blank=True)

#     def __str__(self):
#         return self.name


class Keyword(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100, unique=True)
    active = models.BooleanField(default=True)
    keyproducts = models.ManyToManyField(
        'shop.Product',
        verbose_name=_('Keyword Product'),
        through='ProductKeyword',
        through_fields=('keyword', 'product'),
        blank=True)

    def __str__(self):
        return self.name


class Currency(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Name of Currency'))
    value = models.PositiveIntegerField(
        _('Value'), help_text=_('Integer Value'))
    # country = models.ManytoManyField()
    exchange_rate = models.DecimalField(
        _('Exchange'),
        max_digits=8, decimal_places=2,
        default=0.0)
    offset = models.DecimalField(
        _('Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
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
        _('Entity'), choices=SERVICE_CHOICES, default=0)
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
    image_alt = models.CharField(
        _('Image Alt'), blank=True, max_length=100)
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
    requires_delivery = models.BooleanField(_("Requires delivery?"),
                                            default=True)

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
    search_keywords = models.TextField(
        _('Search Keywords'),
        blank=True, default='')
    entity = models.ForeignKey(
        'shop.Entity', related_name='entityproducts', blank=True,
        null=True, verbose_name=_("Product Entity"))
    structure = models.ForeignKey(
        'faq.Topic', related_name='topicproducts', blank=True,
        null=True, verbose_name=_("Product Structure"))
    siblings = models.ManyToManyField(
        'self', verbose_name=_('Sibling Products'),
        related_name='siblingproduct+',
        symmetrical=True, blank=True)
    related = models.ManyToManyField(
        'self',
        through='RelatedProduct',
        related_name='relatedproduct+',
        through_fields=('primary', 'secondary'),
        verbose_name=_('Related Product'),
        symmetrical=False, blank=True)
    combo = models.ManyToManyField(
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
        through='ProductKeyword',
        through_fields=('product', 'keyword'),
        blank=True)
    # offers = models.ManyToManyField(
    #     'shop.Offer',
    #     verbose_name=_('Product Offer'),
    #     through='ProductOffer',
    #     through_fields=('product', 'offer'),
    #     blank=True)
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

    @property
    def has_attributes(self):
        return self.attributes.exists()


class ProductArchive(AbstractProduct):
    originalproduct = models.ForeignKey(
        Product,
        verbose_name=_('Original Product'),
        on_delete=models.SET_NULL,
        related_name='originalproduct',
        null=True)
    entity = models.CharField(
        _('Product Entity'),
        blank=True,
        max_length=20)

    siblings = models.CharField(
        _('Siblings Product'),
        blank=True,
        max_length=100)
    related = models.CharField(
        _('Related Product'),
        blank=True,
        max_length=100)
    combo = models.CharField(
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
    entity = models.CharField(
        _('Product Entity'),
        blank=True,
        max_length=20)

    siblings = models.CharField(
        _('Siblings Product'),
        blank=True,
        max_length=100)
    related = models.CharField(
        _('Related Product'),
        blank=True,
        max_length=100)
    combo = models.CharField(
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


class ProductKeyword(AbstractAutoDate):
    keyword = models.ForeignKey(
        Keyword,
        verbose_name=_('Keyword'),
        related_name='keywords',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='keywordproducts',
        on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    weight = models.PositiveIntegerField(
        _('Weight'), default=1)

    def __str__(self):
        return _("%(product)s to '%(keyword)s'") % {
            'product': self.product,
            'keyword': self.keyword}


class ProductCategory(AbstractAutoDate):
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        related_name='categories',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='categoryproducts',
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


class FAQProduct(AbstractAutoDate):
    question = models.ForeignKey(
        FAQuestion,
        verbose_name=_('FAQuestion'),
        related_name='faquestions',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='questionproducts',
        on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    question_order = models.PositiveIntegerField(
        _('Question Order'), default=1)

    def __str__(self):
        return _("%(product)s to '%(question)s'") % {
            'product': self.product,
            'question': self.question}


class ProductAttribute(AbstractAutoDate):
    attribute = models.ForeignKey(
        Attribute,
        verbose_name=_('Attribute'),
        related_name='attributes',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='attributeproducts',
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
    value_ltext = models.TextField(
        _('Value Large Text'), blank=True, default='')
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
        related_name='prices',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_('Product'),
        related_name='priceproducts',
        on_delete=models.CASCADE)

    def __str__(self):
        return _("%(product)s to '%(currency)s'") % {
            'product': self.product,
            'currency': self.currency}


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

