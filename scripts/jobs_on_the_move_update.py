# python imports
import os
import django
import sys
from datetime import date, datetime, timedelta


import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "careerplus.config.settings_staging")

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

#  setup django
django.setup()
from order.models import OrderItem, Order, OrderItemOperation
from users.tasks import user_register
from django.utils import timezone



def get_jobs_move_items(oi_status, sub_type_flow):
    return OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow__in=[5], oi_status__in=oi_status,
        product__sub_type_flow__in=sub_type_flow).select_related('order')

def update_jobs_on_the_move():
    oi_status = [31, 32]
    sub_type_flow = [502]
    jobs_move_items = get_jobs_move_items(oi_status, sub_type_flow)
    import ipdb; ipdb.set_trace()
    for oi in jobs_move_items:
        oi_op = OrderItemOperation.objects.filter(
            oi=oi.id, oi_status__in=[31, 32]).first()
        oi.start_date = oi_op.created
        oi.end_date = oi_op.created + \
            timedelta(days=oi.product.day_duration)
        oi.save()
    return


if __name__ == '__main__':
    update_jobs_on_the_move()
