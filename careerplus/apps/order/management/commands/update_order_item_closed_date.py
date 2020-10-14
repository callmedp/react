import logging

from django.core.management.base import BaseCommand
from django.db.models import Q

from order.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_close_date()


def update_close_date():
    """ updating order item closed date """

    closed_ois = OrderItem.objects.filter(
        Q(oi_status=4, closed_on=None) |
        Q(oi_status=4, closed_on__isnull=True))

    ct = 0

    for oi in closed_ois:
        if oi.oi_status == 4:
            ops_set = oi.orderitemoperation_set.filter(oi_status=4)
            if ops_set.exists():
                oi.closed_on = ops_set[0].created
                oi.save()
                ct += 1
            else:
                logging.getLogger('error_log').error("orderitem id %s is closed but closed operation not found" % (oi.id))

    logging.getLogger('info_log').info(
        "close date updated on {} orderitems out of {}".format(
            ct, closed_ois.count()))
