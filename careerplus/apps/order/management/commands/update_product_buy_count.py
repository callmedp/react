import logging
from django.core.management.base import BaseCommand

from order.models import OrderItem
from shop.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_product_buy_count()


def update_product_buy_count():
    """ updating product buy count """

    updated = 0
    products = Product.objects.all()
    for product in products:
        count = OrderItem.objects.filter(
            product_id=product.id,
            order__status__in=[1, 2, 3]).count()
        if product.buy_count != count:
            product.buy_count = count
            product.save()
            updated += 1

    logging.getLogger('info_log').info(
        "{} product buy count updated out of {}".format(
            updated, products.count()))
