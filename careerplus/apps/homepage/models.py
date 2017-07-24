from django.db import models
from django.utils.translation import ugettext_lazy as _

from seo.models import AbstractAutoDate

from .config import PAGECHOICES


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
    page = models.PositiveIntegerField(default=1, choices=PAGECHOICES)
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
    company = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        _('Profile Image'),
        upload_to='images/testimonial/', null=True, blank=True)
    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['priority']
