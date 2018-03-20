import logging
from django.core.management.base import BaseCommand

from order.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_allocation_date()


def update_allocation_date():
    """ update Allocation date of orderitems """

    orderitems = OrderItem.objects.filter(
        order__status__in=[1, 3],
        assigned_date=None, no_process=False).exclude(
        assigned_to=None)

    updated = 0
    for oi in orderitems:
        if oi.assigned_to:
            ops = oi.orderitemoperation_set.filter(oi_status=1).order_by('id')
            if ops.exists():
                oi.assigned_date = ops[0].created
                oi.save()
                updated += 1

    logging.getLogger('info_log').info(
        "{} allocation date out of {}".format(updated, orderitems.count()))
