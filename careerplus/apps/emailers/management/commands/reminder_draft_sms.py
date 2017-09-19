import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from order.models import OrderItem
from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS


class Command(BaseCommand):
    """
        Daily Cron for draft reminder mail/Sms
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        draft_reminder_sms()


def draft_reminder_sms():
    try:
        orderitems = OrderItem.objects.filter(
            oi_status__in=[24, 46], product__type_flow__in=[1, 12, 13, 8]).select_related('order', 'product')
        for oi in orderitems:
            if not oi.approved_on:
                oi.approved_on = timezone.now()
                oi.save()
            approved_date = oi.approved_on.date()
            today_date = timezone.now().date()
            mail_type = 'REMINDER'
            data = {}           
            if today_date >= approved_date + datetime.timedelta(days=2):        
                data.update({
                    "first_name": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                })
                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                last_oi_status = oi.oi_status
                oi.oi_status = 4
                oi.last_oi_status = last_oi_status
                oi.closed_on = timezone.now()
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to)

    except Exception as e:
        logging.getLogger('email_log').error("%s - %s" % (
            "Reminder mail cron", str(e)))