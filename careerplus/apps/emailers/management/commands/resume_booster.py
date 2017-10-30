import textwrap
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from order.models import OrderItem
from core.mixins import TokenExpiry
from emailers.tasks import send_email_task
from emailers.sms import SendSMS


class Command(BaseCommand):
    def handle(self, *args, **options):
        booster()
        print ("Booster mail send to recruiter.")


def booster():
    ''' Resume Boosters mail sending'''

    booster_ois = OrderItem.objects.filter(order__status__in=[1, 3], product__type_flow=7, oi_status=5)
    booster_ois = booster_ois.select_related('order')
    days = 7
    candidate_data = {}
    recruiter_data = {}
    
    for oi in booster_ois:
        token = TokenExpiry().encode(oi.order.email, oi.pk, days)
        to_emails = [oi.order.email]
        email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
        candidate_data.update({
            "email": oi.order.email,
            "mobile": oi.order.mobile,
            'subject': 'Your resume has been shared with relevant consultants',
            "user_name": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
        })

        if oi.oi_draft:
            resumevar = "%s://%s/user/resume/download/?token=%s" % (
                settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)
            resumevar = textwrap.fill(resumevar, width=80)

            email = candidate_data.get('email') if candidate_data.get('email') else ''
            download_link = resumevar
            recruiter_data.update({
                email: download_link,
            })

            try:
                # send mail to candidate
                if 93 not in email_sets:
                    mail_type = 'BOOSTER_CANDIDATE'
                    send_email_task.delay(to_emails, mail_type, candidate_data, status=93, oi=oi.pk)
                # send sms to candidate
                SendSMS().send(sms_type="BOOSTER_CANDIDATE", data=candidate_data)
                last_oi_status = oi.oi_status
                oi.oi_status = 62
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=62,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to,
                )

            except Exception as e:
                logging.getLogger('cron_log').error("%s" % (str(e)))
        else:
            continue
    try:
        # send mail to rectuter
        recruiters = settings.BOOSTER_RECRUITERS
        mail_type = 'BOOSTER_RECRUITER'
        send_email_task.delay(recruiters, mail_type, recruiter_data)
        for oi in booster_ois:
            oi.emailorderitemoperation_set.create(email_oi_status=92)
    except Exception as e:
        logging.getLogger('cron_log').error("%s" % (str(e)))
