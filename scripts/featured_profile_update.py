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
from emailers.utils import BadgingMixin
from order.models import OrderItem, Order, OrderItemOperation
from users.tasks import user_register
from django.utils import timezone




def get_featured_oi(oi_status, sub_type_flow):
    return OrderItem.objects.filter(
        order__status__in=[1, 3], product__type_flow__in=[5], oi_status__in=oi_status,
        product__sub_type_flow__in=sub_type_flow).select_related('order')


def get_candidate_id(oi):
    candidate_id = oi.order.candidate_id

    if not candidate_id:
        user_register(data={}, order=oi.order.pk)
        order = Order.objects.get(pk=oi.order.pk)
        candidate_id = oi.order.candidate_id

    return candidate_id


def update_featured_oi():
    oi_status = [28, 34, 35]
    sub_type_flow = [501, 503]
    featured_orderitems = get_featured_oi(oi_status, sub_type_flow)
    for oi in featured_orderitems:
        candidate_id = get_candidate_id(oi)
        badge_data = BadgingMixin().get_badging_data(
            candidate_id=candidate_id, curr_order_item=oi, feature=True
        )
        if 'ec' in badge_data.keys():
            if 1 in badge_data.get('ec') or 4 in badge_data.get('ec'):
                oi_op = OrderItemOperation.objects.filter(
                    oi=oi.id, oi_status__in=[5,23,31], last_oi_status=6).first()
                if oi_op:
                    oi.start_date = oi_op.created
                    oi.end_date = oi_op.created + \
                        timedelta(days=oi.product.day_duration)
                    oi.save()
    return


if __name__ == '__main__':
    update_featured_oi()
