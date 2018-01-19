from django.core.management.base import BaseCommand

from order.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_product_buy_count()


def update_product_buy_count():
    """ updating product buy count """

    orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3],
        buy_count_updated=False).exclude(
        product=None).select_related('product')

    updated = 0
    for oi in orderitems:
        if oi.product:
            pd = oi.product
            pd.buy_count += 1
            pd.save()
            oi.buy_count_updated = True
            oi.save()
            updated += 1

    print(updated, 'product buy count updated out of', orderitems.count())
