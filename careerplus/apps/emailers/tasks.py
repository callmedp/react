import logging
from celery.decorators import task
from .email import *


@task(name="send_email_task")
def send_email_task(to_emails, mail_type, email_dict):
    flag = False
    try:
        SendMail().send(to_emails, mail_type, email_dict)
        flag = True
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s -%s" % (str(to_emails), str(e), str(mail_type), (flag)))
    return flag


@task(name="send_email_for_base_task")
def send_email_for_base_task(subject=None, body=None, to=[], headers=None):
    flag = False
    try:
        SendMail().base_send_mail(subject=None, body=None, to=[], headers=None)
        flag = True
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s" % (str(to), str(e), (flag)))
    return flag
