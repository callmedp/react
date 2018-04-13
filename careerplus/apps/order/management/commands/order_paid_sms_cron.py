# import python module
import logging
import datetime

# import django module
from django.core.management.base import BaseCommand

# import apps module
from emailers.tasks import send_sms_for_base_task
from order.models import Order, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_sms_paid_order_day1()
        send_sms_paid_order_day2()


def send_sms_paid_order_day1():
    """ send sms cron for paid order """
    try:
        message1 = "Thank you for becoming a valued\
        ShineLearning.com customer.\
        Kindly note that while we endeavor to enhance your career prospects,\
        we do not guarantee any jobs."
        ois = Order.objects.filter(status=1)
        pk_list = list(ois.values_list('pk', flat=True))
        oi_lists = OrderItem.objects.filter(
            order__pk__in=pk_list).values_list(
            'smsorderitemoperation__sms_oi_status',
            flat=True).exclude(
            oi_status=4, smsorderitemoperation__sms_oi_status=5)

        for oi in ois:
            if 5 not in list(oi_lists):
                """ Send sms """
                send_sms_for_base_task.delay(
                    mob=oi.mobile, message=message1,
                    oi=oi.pk, status=5)
    except Exception as e:
        logging.getLogger('error_log').error_log("{}".format(e))


def send_sms_paid_order_day2():
    """ send sms cron for paid order """
    try:
        message2 = "Shine.com does not offer cash back or\
        refund for its services through PayTM or any other channel.\
        Report any such fake recruiter calls\
        you get in name of Shine.com at 01206158822"
        ois = Order.objects.filter(status=1)
        pk_list = list(ois.values_list('pk', flat=True))
        oi_lists = OrderItem.objects.filter(
            order__pk__in=pk_list).values_list(
            'smsorderitemoperation__sms_oi_status',
            flat=True).exclude(
            oi_status=4, smsorderitemoperation__sms_oi_status=6)

        for oi in ois:
            if 6 not in list(oi_lists):
                """ Send sms """
                send_sms_for_base_task.delay(
                    mob=oi.mobile, message=message2,
                    oi=oi.pk, status=6)
    except Exception as e:
        logging.getLogger('error_log').error_log("{}".format(e))
