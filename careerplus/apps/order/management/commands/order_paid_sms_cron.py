# import python module
import logging

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
        ois = Order.objects.filter(status=1).exclude(
            orderitems__smsorderitemoperation__sms_oi_status=5,
            orderitems__oi_status=4)
        for oi in ois:
            """ Send sms """
            send_sms_for_base_task.delay(
                mob=oi.mobile, message=message1,
                oi=oi.pk, status=5)
        logging.getLogger("info_log").info("cron run succesfully")
    except Exception as e:
        logging.getLogger('error_log').error_log("{}".format(e))


def send_sms_paid_order_day2():
    """ send sms cron for paid order """
    try:
        message2 = "Shine.com does not offer cash back or\
        refund for its services through PayTM or any other channel.\
        Report any such fake recruiter calls\
        you get in name of Shine.com at 01206158822"
        ois = Order.objects.filter(status=1).exclude(
            orderitems__smsorderitemoperation__sms_oi_status=6,
            orderitems__oi_status=4)

        for oi in ois:
            """ Send sms """
            send_sms_for_base_task.delay(
                mob=oi.mobile, message=message2,
                oi=oi.pk, status=6)
        logging.getLogger("info_log").info("cron run succesfully")
    except Exception as e:
        logging.getLogger('error_log').error_log("{}".format(e))
