# import python module
import logging

# import django module
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime

# import apps module
from emailers.tasks import send_sms_for_base_task
from order.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_sms_paid_order_day1()
        send_sms_paid_order_day2()


def send_sms_paid_order_day1():
    two_days_date = timezone.now() - datetime.timedelta(days=2)
    """ send sms cron for paid order """
    try:
        message1 = "Thank you for becoming a valued\
        ShineLearning.com customer.\
        Kindly note that while we endeavor to enhance your career prospects,\
        we do not guarantee any jobs."
        orders = Order.objects.filter(status=1, payment_date__gt=two_days_date).exclude(
            orderitems__smsorderitemoperation__sms_oi_status=5)
        for order in orders:
            """ Send sms """
            send_sms_for_base_task.delay(
                mob=order.mobile, message=message1,
                oi=order.pk, status=5)
            logging.getLogger("info_log").info("Paid order day 1 sms sent for {}".format(order.id))
        logging.getLogger("info_log").info("Paid order day 1 sms cron run succesfully")
    except Exception as e:
        logging.getLogger('error_log').error("{}".format(e))


def send_sms_paid_order_day2():
    """ send sms cron for paid order """
    one_day_date = timezone.now() - datetime.timedelta(days=1)
    try:
        message2 = "Shine.com does not offer cash back or\
        refund for its services through PayTM or any other channel.\
        Report any such fake recruiter calls\
        you get in name of Shine.com at 01206158822"
        orders = Order.objects.filter(status=1, orderitems__smsorderitemoperation__sms_oi_status=5).exclude(
            orderitems__smsorderitemoperation__sms_oi_status=6)

        for order in orders:
            """ Send sms """
            orderitems = order.orderitems.filter(smsorderitemoperation__sms_oi_status=5)
            if orderitems:
                oi = orderitems[0]
                sms_op = oi.smsorderitemoperation_set.filter(sms_oi_status=5, created__lt=one_day_date)
                if sms_op:
                    send_sms_for_base_task.delay(
                        mob=order.mobile, message=message2,
                        oi=order.pk, status=6)
                    logging.getLogger("info_log").info("Paid order day 2 sms sent for {}".format(order.id))
        logging.getLogger("info_log").info("Paid order day 2 sms cron run succesfully")
    except Exception as e:
        logging.getLogger('error_log').error("{}".format(e))
