from django.core.management.base import BaseCommand
import logging
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from emailers.email import SendMail


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_linkedin_tips()
        
def send_linkedin_tips():
    ''' tip emailers for linkedin '''

    orderitems = OrderItem.objects.filter(
        order__status=1, product__type_flow=8).exclude(oi_flow_status__in=[0,41,42,50])
    orderitems_obj = orderitems.select_related('order')

    for oi in orderitems_obj:
        try:
            context_dict = {}
            ord_obj = oi.order
            context_dict['username'] = ord_obj.first_name if ord_obj.first_name else ord_obj.candidate_id
            if oi.oi_flow_status == 50:
                subject = 'Turn your LinkedIn into resume'
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip1.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 51
                oi.save()
            elif oi.oi_flow_status == 51:
                subject = "Connect with more and more people"
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip2.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 52
                oi.save()
            elif oi.oi_flow_status == 52:
                subject = "Customize your LinkedIn URL"
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip3.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 53
                oi.save()
            elif oi.oi_flow_status == 53:
                subject = "Importance of joining groups on LinkedIn"
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip4.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 54
                oi.save()
            elif oi.oi_flow_status == 54:
                subject = "Will you trust a profile without a profile picture?"
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip5.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 55
                oi.save()
            elif oi.oi_flow_status == 55:
                subject = "You like writing?"
                header = {'Reply-To': settings.REPLY_TO}
                context_dict['subject'] = subject
                context_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                html = render_to_string("emailers/candidate/linkedin_tip6.html", context_dict)
                SendMail().base_send_mail(
                    subject, html, to=[oi.order.email], headers=headers)
                oi.oi_flow_status = 56
                oi.save()
        except Exception as e:
            logging.getLogger('email_log').error("%s - %s" % (str(oi.id), str(e)))