import textwrap
from django.core.management.base import BaseCommand
from django.conf import settings

from order.models import OrderItem
from core.common import TokenExpiry
from emailers.email import SendMail
from emailers.sms import SendSMS


class Command(BaseCommand):
    def handle(self, *args, **options):
        booster()
        print ("Booster mail send to recruter.")


def booster():
    ''' Resume Boosters mail sending'''

    booster_ois = OrderItem.objects.filter(order__status__in=[1, 3], product__type_flow=7, oi_status=5)
    booster_ois = booster_ois.select_related('order')
    days = 7
    candidate_data = {}
    recruiter_data = {}

    for oi in booster_ois:
        token = TokenExpiry().encode(oi.order.email, oi.pk, days)
        candidate_data.update({
            "email": oi.order.email,
            "mobile": oi.order.mobile,
            'subject': 'Your resume has been shared with relevant consultants',
            "user_name": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
        })

        if oi.oi_draft:
            resumevar = "http://%s/user/resume/download/?token=%s" % (
                settings.SITE_DOMAIN, token)
            resumevar = textwrap.fill(resumevar, width=80)

            link_title = candidate_data.get('user_name') if candidate_data.get('user_name') else candidate_data.get('email')
            download_link = resumevar
            recruiter_data.update({
                "link_title": link_title,
                "download_link": download_link,
            })

            try:
                # send mail to rectuter
                recruiters = settings.BOOSTER_RECRUITERS
                SendMail().send(
                    to=recruiters, mail_type="BOOSTER_RECRUITER", data=recruiter_data)

                # send mail to candidate
                SendMail().send(
                    to=[candidate_data.get('email')], mail_type="BOOSTER_CANDIDATE", data=candidate_data)

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
                print (str(e))
        else:
            continue
