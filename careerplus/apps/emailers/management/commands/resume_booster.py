import textwrap
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from order.models import OrderItem
from core.mixins import TokenExpiry
from emailers.tasks import send_booster_recruiter_mail_task
from emailers.sms import SendSMS
from partner.models import BoosterRecruiter


class Command(BaseCommand):
    def handle(self, *args, **options):
        booster()
        print ("Booster mail send to recruiter.")


def booster():
    ''' Resume Boosters mail sending'''

    booster_ois = OrderItem.objects.filter(order__welcome_call_done=True,
        order__status__in=[1, 3], product__type_flow__in=[7,15], oi_status__in=[0, 5, 61, 62])

    booster_ois = booster_ois.select_related('order').order_by('created')
    days = 7
    candidate_data = {}
    recruiter_data = {}
    candidate_list = []
    international_booster_candidate_list = []
    item_emailoperation = []
    order_item_to_update_list = []

    for oi in booster_ois:
        if oi.oi_status == 61:
            closed_ois = oi.order.orderitems.filter(oi_status=4, product__type_flow=1, no_process=False)
            if closed_ois.exists():
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.oi_draft = closed_ois[0].oi_draft
                oi.draft_counter += 1
                oi.last_oi_status = last_oi_status
                oi.draft_added_on = timezone.now()
                oi.save()

                oi.orderitemoperation_set.create(
                    oi_draft=oi.oi_draft,
                    draft_counter=oi.draft_counter,
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to,
                )
            continue
        elif oi.oi_status == 62:
            last_oi_status = oi.oi_status
            oi.oi_status = 4
            oi.last_oi_status = 6
            oi.closed_on = timezone.now()
            oi.save()

            oi.orderitemoperation_set.create(
                oi_status=6,
                last_oi_status=62,
                assigned_to=oi.assigned_to,
            )

            oi.orderitemoperation_set.create(
                oi_status=4,
                last_oi_status=6,
                assigned_to=oi.assigned_to,
            )
            continue
        elif oi.oi_status == 0:
            last_oi_status = oi.oi_status
            oi.oi_status = 2
            oi.last_oi_status = last_oi_status
            oi.save()

            oi.orderitemoperation_set.create(
                oi_status=oi.oi_status,
                last_oi_status=oi.last_oi_status,
                assigned_to=oi.assigned_to,
            )
            continue

        item_emailoperation.append(oi)
        token = TokenExpiry().encode(oi.order.email, oi.pk, days)
        candidate_data.update({
            "email": oi.order.get_email(),
            "mobile": oi.order.get_mobile(),
            'subject': 'Your resume has been shared with relevant consultants',
            "username": oi.order.first_name,
        })

        if oi.oi_draft or oi.oi_resume:
            resumevar = "%s://%s/user/resume/download/?token=%s" % (
                settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)
            resumevar = textwrap.fill(resumevar, width=80)

            link_title = candidate_data.get('email') if candidate_data.get('email') else ''
            download_link = resumevar
            data_dict = {}
            data_dict.update({
                "title": link_title,
                "download_link": download_link,
            })
            if oi.product.type_flow == 7:
                candidate_list.append(data_dict)
            elif oi.product.type_flow == 15:
                international_booster_candidate_list.append(data_dict)
            order_item_to_update_list.append(oi.id)
        else:
            continue
    try:
        # send mail to rectuter
        mail_type = 'BOOSTER_RECRUITER'
        recruiter_data.update({"data": candidate_list})
        if candidate_list != []:
            recruiters = BoosterRecruiter.objects.get(type_recruiter=0).recruiter_list.split(',')
            send_booster_recruiter_mail_task.delay(recruiters, mail_type, recruiter_data, ois_to_update=order_item_to_update_list)

        recruiter_data.update({"data": international_booster_candidate_list})

        if international_booster_candidate_list != []:
            recruiters = BoosterRecruiter.objects.get(type_recruiter=1).recruiter_list.split(',')
            send_booster_recruiter_mail_task.delay(recruiters, mail_type, recruiter_data, ois_to_update=order_item_to_update_list)

    except Exception as e:
        logging.getLogger('error_log').error("%s" % (str(e)))
