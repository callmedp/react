from django.core.management.base import BaseCommand
import logging
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from emailers.tasks import send_email_for_base_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_linkedin_tips()


def send_linkedin_tips():
    ''' tip emailers for linkedin '''

    orderitems = OrderItem.objects.filter(
        order__status=1, product__type_flow=8).select_related('order')
    for oi in orderitems:
        try:
            context_dict = {}
            username = oi.order.first_name if oi.order.first_name else oi.order.candidate_id
            context_dict['username'] = username
            headers = {'Reply-To': settings.REPLY_TO}
            counter = oi.draft_counter
            email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
            ops_sets = list(oi.orderitemoperation_set.all().values_list('oi_status',flat=True).distinct())

            if 46 in ops_sets and (counter == 1 and 109 not in email_sets):
                subject = 'Turn your LinkedIn into resume'
                context_dict['subject'] = subject
                html = render_to_string("emailers/candidate/linkedin_tip1.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=109)
            elif 109 in email_sets:
                subject = "Connect with more and more people"
                context_dict['subject'] = "Connect with more and more people"
                html = render_to_string("emailers/candidate/linkedin_tip2.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=110)
            elif 110 in email_sets:
                subject = "Customize your LinkedIn URL"
                context_dict['subject'] = "Customize your LinkedIn URL"
                html = render_to_string("emailers/candidate/linkedin_tip3.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=111)
            elif 111 in email_sets:
                subject = "Importance of joining groups on LinkedIn"
                context_dict['subject'] = "Importance of joining groups on Linkedin"
                html = render_to_string("emailers/candidate/linkedin_tip4.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=112)
            elif 112 in email_sets:
                subject = "Will you trust a profile without a profile picture?"
                context_dict['subject'] = "Will you trust a profile without a profile picture?"
                html = render_to_string("emailers/candidate/linkedin_tip5.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=113)
            elif 113 in email_sets:
                subject = "You like writing?"
                context_dict['subject'] = "You like writing?"
                html = render_to_string("emailers/candidate/linkedin_tip6.html", context_dict)
                send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers, oi=oi.pk, status=114)
        except Exception as e:
            logging.getLogger('email_log').error("%s - %s" % (str(oi.id), str(e)))