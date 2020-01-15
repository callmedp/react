# python imports

#django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# local imports
from .config import PAGECHOICES, STATIC_PAGE_NAME_CHOICES

# interapp imports
from seo.models import AbstractAutoDate
from shop.models import FunctionalArea

# third party imports
from ckeditor.fields import RichTextField


class TopTrending(AbstractAutoDate):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(
        "shop.Product",
        through='TrendingProduct',
        related_name='trendingcourses')

    view_all = models.CharField(
        max_length=255,
        help_text=_('provide full url with http:// to redirect on click.'))

    is_jobassistance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    fa = models.ManyToManyField(FunctionalArea,null=True, blank=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    def get_trending_products(self):
        tprds = self.trendingproduct_set.filter(is_active=True).select_related('product')
        tprds = tprds.filter(product__type_product__in=[0, 1, 3])
        return tprds


class TrendingProduct(AbstractAutoDate):
    trendingcourse = models.ForeignKey(
        TopTrending,
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE)

    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('trendingcourse', 'product')
        ordering = ['priority']

    def __str__(self):
        return self.trendingcourse.name + '-' + self.product.name


class Testimonial(AbstractAutoDate):
    page = models.PositiveIntegerField(
        default=0, choices=PAGECHOICES)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)
    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"))
    title = models.CharField(max_length=255, null=True, blank=True)
    review = models.TextField(max_length=1024)
    rating = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=2.5)
    designation = models.CharField(max_length=200)
    # location = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        _('Profile Image'),
        upload_to='images/testimonial/', null=True, blank=True)
    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    # for university/Course skill page
    object_id = models.PositiveIntegerField(
        null=True, blank=True)

    def __str__(self):
        return str(self.user_name) + ' - ' + str(self.id)

    class Meta:
        ordering = ['priority']

    def get_image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'shinelearn/images/executive/default-user-pic.jpg'

    def page_choice_text(self):
        currency_dict = dict(PAGECHOICES)
        return currency_dict.get(self.page)


class TestimonialCategoryRelationship(AbstractAutoDate):
    category = models.ForeignKey('shop.Category')
    testimonial = models.ForeignKey('homepage.Testimonial')


class StaticSiteContent(models.Model):
    page_type = models.PositiveIntegerField(
        default=-1, choices=STATIC_PAGE_NAME_CHOICES , help_text=_('page id'))

    content = RichTextField(
        verbose_name=_('content'), help_text=_('html content'))
    
    @property
    def page_name(self):
        return STATIC_PAGE_NAME_CHOICES[self.page_type-1][1]

    def __str__(self):
        return str(STATIC_PAGE_NAME_CHOICES[self.page_type-1][1])