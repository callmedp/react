import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from order.models import OrderItem
from emailers.email import SendMail
from emailers.sms import SendSMS


class Command(BaseCommand):
    """
        Daily Cron for draft reminder mail/Sms
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        draft_reminder_mail()


def draft_reminder_mail():
    try:
        orderitems = OrderItem.objects.filter(
            oi_status=24, product__type_flow__in=[1, 12, 13]).select_related('order', 'product')
        for oi in orderitems:
            if not oi.approved_on:
                oi.approved_on = timezone.now()
                oi.save()
            approved_date = oi.approved_on.date()
            today_date = timezone.now().date()
            draft_level = oi.draft_counter
            if draft_level == 1 and today_date == approved_date + datetime.timedelta(days=8):
                to_emails = [oi.order.email]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    "candidateid": oi.order.candidate_id,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date == approved_date + datetime.timedelta(days=15):

                to_emails = [oi.order.email]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    "candidateid": oi.order.candidate_id,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date == approved_date + datetime.timedelta(days=22):
                to_emails = [oi.order.email]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    "candidateid": oi.order.candidate_id,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 1 and today_date == approved_date + datetime.timedelta(days=29):
                to_emails = [oi.order.email]
                mail_type = 'AUTO_CLOSER'
                email_dict = {}
                email_dict.update({
                    "info": 'Auto closer mail',
                    "draft_level": oi.draft_counter,
                    "name": oi.order.first_name + ' ' + oi.order.last_name,
                    "mobile": oi.order.mobile,
                })

                try:
                    SendMail().send(to_emails, mail_type, email_dict)
                except Exception as e:
                    logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

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

            elif draft_level == 2 and today_date == approved_date + datetime.timedelta(days=4):
                to_emails = [oi.order.email]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    "candidateid": oi.order.candidate_id,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 2 and today_date == approved_date + datetime.timedelta(days=7):
                to_emails = [oi.order.email]
                mail_type = 'REMINDER'
                data = {}
                data.update({
                    "subject": "Reminder:Your developed resume document has been uploaded",
                    "draft_level": draft_level,
                    "first_name": oi.order.first_name,
                    "candidateid": oi.order.candidate_id,
                })
                try:
                    SendMail().send(to_emails, mail_type, data)
                except Exception as e:
                    logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

                try:
                    SendSMS().send(sms_type=mail_type, data=data)
                except Exception as e:
                    logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

            elif draft_level == 2 and today_date == approved_date + datetime.timedelta(days=10):
                to_emails = [oi.order.email]
                mail_type = 'AUTO_CLOSER'
                email_dict = {}
                email_dict.update({
                    "info": 'Auto closer Email',
                    "draft_level": oi.draft_counter,
                    "name": oi.order.first_name + ' ' + oi.order.last_name,
                    "mobile": oi.order.mobile,
                })

                try:
                    SendMail().send(to_emails, mail_type, email_dict)
                except Exception as e:
                    logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

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