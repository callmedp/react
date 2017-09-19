from django.core.management.base import BaseCommand
import logging
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from emailers.email import SendMail
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
                context_dict['subject'] = 'Turn your LinkedIn into resume'
                html = render_to_string("emailers/candidate/linkedin_tip1.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=109)
            elif 109 in email_sets:
                context_dict['subject'] = "Connect with more and more people"
                html = render_to_string("emailers/candidate/linkedin_tip2.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=110)
            elif 110 in email_sets:
                context_dict['subject'] = "Customize your LinkedIn URL"
                html = render_to_string("emailers/candidate/linkedin_tip3.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=111)
            elif 111 in email_sets:
                context_dict['subject'] = "Importance of joining groups on LinkedIn"
                html = render_to_string("emailers/candidate/linkedin_tip4.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=112)
            elif 112 in email_sets:
                context_dict['subject'] = "Will you trust a profile without a profile picture?"
                html = render_to_string("emailers/candidate/linkedin_tip5.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=113)
            elif 113 in email_sets:
                context_dict['subject'] = "You like writing?"
                html = render_to_string("emailers/candidate/linkedin_tip6.html", context_dict)
                return_val = send_email_for_base_task.delay(subject, html, to=[oi.order.email], headers=headers)
                if return_val.result:
                    oi.emailorderitemoperation_set.create(email_oi_status=114)
        except Exception as e:
            logging.getLogger('email_log').error("%s - %s" % (str(oi.id), str(e)))