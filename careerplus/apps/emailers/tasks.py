import logging
from celery.decorators import task
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
        logging.getLogger('email_log').error(
            "%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))


@task(name="send_email_for_base_task")
def send_email_for_base_task(subject=None, body=None, to=[], headers=None, oi=None, status=None):
    try:
        SendMail().base_send_mail(subject=None, body=None, to=[], headers=None)
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.get(pk=oi)
            obj.emailorderitemoperation_set.create(email_oi_status=status)
    except Exception as e:
        logging.getLogger('email_log').error(
            "%s - %s" % (str(to), str(e)))
