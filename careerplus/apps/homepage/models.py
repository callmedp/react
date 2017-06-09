from django.db import models
from django.utils.translation import ugettext_lazy as _

from seo.models import AbstractAutoDate


class TopTrending(AbstractAutoDate):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(
        "shop.Product",
        through='TrendingProduct',
        related_name='trendingcourses')

    view_all = models.CharField(
        max_length=255,
        help_text=_('provide full url to redirect on click.'))

    is_jobassistance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['-priority']

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
        ordering = ['-priority']

    def __str__(self):
        return self.trendingcourse.name + '-' + self.product.name