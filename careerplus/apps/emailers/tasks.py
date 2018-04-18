import logging
from celery.decorators import task
from django.conf import settings
from emailers.email import SendMail
from emailers.sms import SendSMS
from order.models import Order


@task(name="send_email_task")
def send_email_task(to_emails, mail_type, email_dict, status=None, oi=None):
    try:
        SendMail().send(to_emails, mail_type, email_dict)
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.filter(pk=oi)
            for oi_item in obj:
                to_email = to_emails[0] if to_emails else oi_item.order.email
                oi_item.emailorderitemoperation_set.create(
                    email_oi_status=status,
                    to_email=to_email, status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "emailing sending failed %s - %s - %s" % (str(e), str(mail_type), str(to_emails)))


@task(name="send_email_for_base_task")
def send_email_for_base_task(subject=None, body=None, to=[], headers=None, oi=None, status=None):
    try:
        SendMail().base_send_mail(subject, body, to=[], headers=None, bcc=[settings.DEFAULT_FROM_EMAIL])
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.get(pk=oi)
            to = to[0] if to else obj.order.email
            obj.emailorderitemoperation_set.create(
                email_oi_status=status,
                to_email=to, status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "emailing from base task failed%s - %s" % (str(to), str(e)))


@task(name="send_sms_for_base_task")
def send_sms_for_base_task(mob=None, message=None, oi=None, status=None):
    try:
        SendSMS().base_send_sms(mob, message)
        if oi:
            obj = Order.objects.get(pk=oi)
            oi_objs = obj.orderitems.all()
            for oi in oi_objs:
                oi.smsorderitemoperation_set.create(
                    sms_oi_status=status,
                    to_mobile=mob, status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "sms from base task failed%s - %s" % (str(mob), str(e)))
