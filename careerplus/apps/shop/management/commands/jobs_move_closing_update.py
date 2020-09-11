import MySQLdb
import math
import datetime
import pytz
from dateutil import relativedelta
import logging
import time

from django.conf import settings
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from ...models import Product
from review.models import Review
from users.tasks import user_register
from order.models import OrderItem
from shop.models import JobsLinks
from shop.choices import S_ATTR_DICT, A_ATTR_DICT


class Command(BaseCommand):
    """
        Custom command to Update Jobs form Shine to Products.
    """
    help = ''' Whatsapp Job Order Closing/
            Custom command to Update Whatsapp jobs links that was supposed to be send till now.
            '''

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        jobs_move_items = OrderItem.objects.filter(
            order__status__in=[1, 3],
            product__type_flow__in=[5],
            oi_status__in=[31, 32],
            product__sub_type_flow=502
        )
        jobs_move_items = jobs_move_items.select_related('order')
        jobs_move_close_count = 0

        for obj in jobs_move_items:
            candidate_id = None

            if obj.order.candidate_id:
                candidate_id = obj.order.candidate_id
            else:
                user_register(data={}, order=obj.order.pk)

            featured_op = obj.orderitemoperation_set.filter(
                oi_status__in=[5, 23, 31]).order_by('id').order_by('id').first()

            try:
                activation_date = featured_op.created
            except Exception as e:
                logging.getLogger('error_log').error(
                    "unable to create activation date%s" % (str(e)))
                continue

            duration_days = obj.get_duration_days

            delta_time = activation_date + \
                datetime.timedelta(days=duration_days)
        
            obj.update_pending_links_count()

            # Close the order if condition satisfies else
            if candidate_id:
                if (delta_time < timezone.now()) and obj.pending_links_count == 0:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 4
                    obj.closed_on = timezone.now()
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to)
                    jobs_move_close_count += 1
                else:
                    sevice_started_op = obj.orderitemoperation_set.all().filter(
                        oi_status__in=[5, 23, 31]).order_by('id').first()

                    if sevice_started_op:
                        if obj.pending_links_count > 0 and obj.oi_status == 32:
                            last_oi_status = obj.oi_status
                            obj.oi_status = 31
                            obj.save()
                            obj.orderitemoperation_set.create(
                                oi_status=obj.oi_status,
                                last_oi_status=last_oi_status,
                                assigned_to=obj.assigned_to
                            )

        out_str = '%s jobs on the move item expired out of %s  items' % (
            jobs_move_close_count, jobs_move_items.count())

        logging.getLogger('info_log').info("{}".format(out_str))
