from django.core.management.base import BaseCommand
from django.utils import timezone

from order.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        close_order()


def close_order():
    """ closing order using this cron """

    paid_orders = Order.objects.filter(status=1)
    closed_order = 0

    for od in paid_orders:
        open_ois = od.orderitems.filter(no_process=False).exclude(oi_status=4)
        if not open_ois.exists():
            od.status = 3
            od.closed_on = timezone.now()
            od.save()
            closed_order += 1

    print(closed_order, "orders are closed out of", paid_orders.count())
