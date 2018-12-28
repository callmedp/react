import subprocess
from subprocess import check_output

from django.core.mail import EmailMessage
from django.conf import settings

from celery.decorators import task
from .config import CRON_TO_ID_MAPPING

def send_email_after_completion(cron_id):
    cron_id = int(cron_id)
    html_content = "The cron {} has been completed.".format(CRON_TO_ID_MAPPING[cron_id])

    email = EmailMessage(
        subject="Cron {} Completion".format(CRON_TO_ID_MAPPING[cron_id]), body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL, to=['priya.kharb@hindustantimes.com'])
    email.content_subtype = "html"
    return email.send(fail_silently=False)


@task(name='cron_initiate')
def cron_initiate(cron_id):
    cron_id = int(cron_id)
    python = check_output(["which", "python"]).decode('utf-8').strip() + " "
    command = settings.PROJECT_DIR + "/manage.py "
    cron_shell_command = python + " " + command + CRON_TO_ID_MAPPING[cron_id]+"  --settings=careerplus.config.settings_staging"
    subprocess.call(cron_shell_command, shell=True)
    send_email_after_completion(cron_id)
