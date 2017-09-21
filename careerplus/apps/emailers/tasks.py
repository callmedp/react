import logging
from celery.decorators import task
from emailers.email import SendMail

@task(name="send_email_task")
def send_email_task(to_emails, mail_type, email_dict, status=None, oi=None):
    try:
        SendMail().send(to_emails, mail_type, email_dict)
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.get(pk=oi)
            obj.emailorderitemoperation_set.create(email_oi_status=status)
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))



@task(name="send_email_for_base_task")
def send_email_for_base_task(subject=None, body=None, to=[], headers=None):
    flag = False
    try:
        SendMail().base_send_mail(subject=None, body=None, to=[], headers=None)
        flag = True
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s" % (str(to), str(e), (flag)))
    return flag
