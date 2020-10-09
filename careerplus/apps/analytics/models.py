from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductRecord(models.Model):
    """
    Model To Record Product Views, Reviews, Selling.
    """

    product = models.OneToOneField(
        'shop.Product', verbose_name=_("Product"),
        related_name='stats')
    num_views = models.PositiveIntegerField(_('Views'), default=0)
    num_cart_additions = models.PositiveIntegerField(
        _('Basket Additions'), default=0)
    num_purchases = models.PositiveIntegerField(
        _('Purchases'), default=0, db_index=True)

    # To be used within search
    score = models.FloatField(_('Score'), default=0.00)

    class Meta:
        ordering = ['-num_purchases']
        verbose_name = _('Product Record')
        verbose_name_plural = _('Product Records')

    def __str__(self):
        return _("Record for '%s'") % self.product


class UserRecord(models.Model):
    """
    A record of a user's activity.
    """

    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"),)
    user_email = models.CharField(
        max_length=100,
        verbose_name=_("User Email"),)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)


    # Updated using browsing stats
    num_product_views = models.PositiveIntegerField(
        _('Product Views'), default=0)
    num_basket_additions = models.PositiveIntegerField(
        _('Basket Additions'), default=0)

    # Updated using order stats
    num_orders = models.PositiveIntegerField(
        _('Orders'), default=0, db_index=True)
    num_order_items = models.PositiveIntegerField(
        _('Order Items'), default=0, db_index=True)
    total_spent = models.DecimalField(_('Total Spent'), decimal_places=2,
                                      max_digits=12, default=Decimal('0.00'))
    date_last_order = models.DateTimeField(
        _('Last Order Date'), blank=True, null=True)

    class Meta:
        verbose_name = _('User Record')
        verbose_name_plural = _('User Records')


class UserProductView(models.Model):

    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"),)
    user_email = models.CharField(
        max_length=100,
        verbose_name=_("User Email"),)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)
    product = models.ForeignKey('shop.Product', verbose_name=_("Product"))

    class Meta:
        verbose_name = _('User Product View')
        verbose_name_plural = _('User Product Views')

    def __str__(self):
        return _("%(user)s viewed '%(product)s'") % {
            'user': self.user_id, 'product': self.product}


class UserSearch(models.Model):

    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"),)
    user_email = models.CharField(
        max_length=100,
        verbose_name=_("User Email"),)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)
    query = models.CharField(_("Search term"), max_length=255, db_index=True)

    class Meta:
        verbose_name = _("User Search Query")
        verbose_name_plural = _("User Search Queries")

    def __str__(self):
        return _("%(user)s searched for '%(query)s'") % {
            'user': self.user_id,
            'query': self.query}
