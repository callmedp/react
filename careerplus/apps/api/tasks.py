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
    python = '/var/www/virtualenvs/learning/bin/python '
    command = settings.PROJECT_DIR + "/manage.py "
    setting_command = "  --settings=careerplus.config.settings_staging"
    cron_shell_command = python + " " + command + CRON_TO_ID_MAPPING[cron_id]
    if cron_id == 20:
        cron_shell_command += " --noinput"
    cron_shell_command += setting_command
    subprocess.call(cron_shell_command, shell=True)
    send_email_after_completion(cron_id)


@task(name='create_assignment_lead')
def create_assignment_lead(obj_id=None):
    from crmapi.models import UserQuries, DEFAULT_SLUG_SOURCE
    from crmapi.tasks import create_lead_crm

    from order.models import OrderItem
    lead_source = 30
    slug_source = dict(DEFAULT_SLUG_SOURCE)
    campaign_slug = slug_source.get(int(lead_source))
    if obj_id:
        oi = OrderItem.objects.get(id=obj_id)
        score = oi.assesment.overallScore if getattr(oi, 'assesment') else 'N.A'
        msg = "Overall Score:- {}".format(score)
        medium = 0
        first_name = oi.order.first_name
        last_name = oi.order.last_name if oi.order.last_name else ''
        name = first_name + last_name
        lead = UserQuries.objects.create(
            name=name,
            email=oi.order.email,
            country=oi.order.country,
            phn_number=oi.order.mobile,
            message=msg,
            lead_source=lead_source,
            product=oi.product.name,
            product_id=oi.product.id,
            medium=medium,
            campaign_slug=campaign_slug,
        )
        flag = create_lead_crm.delay(pk=lead.pk)
        if flag:
            lead.lead_created = True
            lead.save()
