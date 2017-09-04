import logging
from celery.decorators import task
from emailers.email import SendEmail


@task(name="send_email_task")
def send_email_task(to_emails, mail_type, email_dict):
	try:
		SendMail().send(to_emails, mail_type, email_dict)
    except Exception as e:
        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))