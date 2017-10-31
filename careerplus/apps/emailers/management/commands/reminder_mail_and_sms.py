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
        draft_reminder_mail()


def draft_reminder_mail():
    try:
        orderitems = OrderItem.objects.filter(
            oi_status=24, product__type_flow__in=[1, 12, 13]).select_related('order', 'product')
        count = 0
        for oi in orderitems:
            count += 1
            if not oi.approved_on:
                oi.approved_on = timezone.now()
                oi.save()
            approved_date = oi.approved_on.date()
            today_date = timezone.now().date()
            draft_level = oi.draft_counter
            if oi.product.type_flow == 1:
                email_sets = oi.emailorderitemoperation_set.filter(email_oi_status=26) if draft_level == 1 else oi.emailorderitemoperation_set.filter(email_oi_status=27)           
                if draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=8) and len(email_sets) == 0:
                    to_emails = [oi.order.email]
                    mail_type = 'REMINDER'
                    data = {}
                    data.update({
                        "subject": "Reminder:Your developed resume document has been uploaded",
                        "draft_level": draft_level,
                        "first_name": oi.order.first_name,
                        "candidateid": oi.order.candidate_id,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, data, status=26, oi=oi.pk)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' - 8 day Reminder SMS Sent')
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=15) and len(email_sets) == 1:

                    to_emails = [oi.order.email]
                    mail_type = 'REMINDER'
                    data = {}
                    data.update({
                        "subject": "Reminder:Your developed resume document has been uploaded",
                        "draft_level": draft_level,
                        "first_name": oi.order.first_name,
                        "candidateid": oi.order.candidate_id,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, data, status=26, oi=oi.pk)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' - 15 day Reminder SMS Sent')
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=22) and len(email_sets) == 2:
                    to_emails = [oi.order.email]
                    mail_type = 'REMINDER'
                    data = {}
                    data.update({
                        "subject": "Reminder:Your developed resume document has been uploaded",
                        "draft_level": draft_level,
                        "first_name": oi.order.first_name,
                        "candidateid": oi.order.candidate_id,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, data, status=26, oi=oi.pk)             
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' - 22 day Reminder SMS Sent')
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif draft_level == 1 and today_date >= approved_date + datetime.timedelta(days=29):
                    to_emails = [oi.order.email]
                    mail_type = 'WRITING_SERVICE_CLOSED'
                    email_dict = {}
                    email_dict.update({
                        "subject": 'Closing your '+oi.product.name+' service',
                        "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'draft_added':oi.draft_added_on,
                        'mobile': oi.order.mobile,
                    })
                    if len(email_sets) == 0:
                        send_email_task.delay(to_emails, mail_type, email_dict, status=9, oi=oi.pk)
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                            oi.smsorderitemoperation_set.create(sms_oi_status=4)
                            print(str(count) + ' Service closed SMS Sent')
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

                elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=4) and len(email_sets) == 0:
                    to_emails = [oi.order.email]
                    mail_type = 'REMINDER'
                    data = {}
                    data.update({
                        "subject": "Reminder:Your developed resume document has been uploaded",
                        "draft_level": draft_level,
                        "first_name": oi.order.first_name,
                        "candidateid": oi.order.candidate_id,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, email_dict, status=27, oi=oi.pk)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' level 2 SMS Sent')
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=7) and len(email_sets) == 1:
                    to_emails = [oi.order.email]
                    mail_type = 'REMINDER'
                    data = {}
                    data.update({
                        "subject": "Reminder:Your developed resume document has been uploaded",
                        "draft_level": draft_level,
                        "first_name": oi.order.first_name,
                        "candidateid": oi.order.candidate_id,
                        'mobile': oi.order.mobile,
                    })
                    send_email_task.delay(to_emails, mail_type, email_dict, status=27, oi=oi.pk)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' level 2 2nd SMS Sent')
                    except Exception as e:
                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                elif draft_level == 2 and today_date >= approved_date + datetime.timedelta(days=10):
                    to_emails = [oi.order.email]
                    mail_type = 'WRITING_SERVICE_CLOSED'
                    email_dict = {}
                    email_dict.update({
                        "subject": 'Closing your '+oi.product.name+' service',
                        "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                        'draft_added':oi.draft_added_on,
                        'mobile': oi.order.mobile,
                    })


                    try:
                        SendMail().send(to_emails, mail_type, email_dict)
                        print(str(count) + ' Service closed Email Sent')
                    except Exception as e:
                        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                        print(str(count) + ' Service closed SMS Sent')
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