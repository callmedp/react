import logging
from celery.decorators import task
from celery.utils.log import get_task_logger
from emailers.email import SendEmail

# logger = get_task_logger(__name__)

@task(name="pendind_item_mail")
def pendind_item_mail(to_emails, mail_type, email_dict):
	try:
		SendMail().send(to_emails, mail_type, email_dict)
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))
	