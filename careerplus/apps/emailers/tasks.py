import logging
from celery.decorators import task
from django.conf import settings
from emailers.email import SendMail


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
            "%s - %s - %s" % (str(e), str(mail_type), str(to_emails)))


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
            "%s - %s" % (str(to), str(e)))
