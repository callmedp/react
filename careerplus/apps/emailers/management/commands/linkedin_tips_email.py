from django.core.management.base import BaseCommand
import logging
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from order.functions import send_email_from_base


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_linkedin_tips()


def send_linkedin_tips():
    ''' tip emailers for linkedin '''
    orderitems = OrderItem.objects.filter(
        order__status=1, product__type_flow=8).select_related('order')
    count1 = count2 = count3 = count4 = count5 = count6 = 0
    for oi in orderitems:
        try:
            context_dict = {}
            username = oi.order.first_name
            context_dict['username'] = username
            headers = {'Reply-To': settings.REPLY_TO}
            counter = oi.draft_counter
            email_sets = list(oi.emailorderitemoperation_set.all().values_list(
                'email_oi_status', flat=True).distinct())
            if 102 in email_sets and (counter == 1 and 109 not in email_sets):
                subject = 'Turn your LinkedIn into resume'
                context_dict['subject'] = subject
                html = render_to_string(
                    "emailers/candidate/linkedin_tip1.html", context_dict)
                send_email_from_base(
                    subject, html, to=[oi.order.get_email()], headers=headers,
                    oi=oi.pk, status=109)
                count1 += 1
                logging.getLogger('info_log').info("{} tip1 mail sent".format(count1))
            elif 110 not in email_sets:
                subject = "Connect with more and more people"
                context_dict['subject'] = "Connect with more and more people"
                html = render_to_string(
                    "emailers/candidate/linkedin_tip2.html", context_dict)
                send_email_from_base(
                    subject, html,
                    to=[oi.order.get_email()], headers=headers,
                    oi=oi.pk, status=110)
                count2 += 1
                logging.getLogger('info_log').info("{} tip2 mail sent".format(count2))
            elif 111 not in email_sets:
                subject = "Customize your LinkedIn URL"
                context_dict['subject'] = "Customize your LinkedIn URL"
                html = render_to_string(
                    "emailers/candidate/linkedin_tip3.html", context_dict)
                send_email_from_base(
                    subject, html,
                    to=[oi.order.get_email()],
                    headers=headers, oi=oi.pk, status=111)
                count3 += 1
                logging.getLogger('info_log').info("{} tip3 mail sent".format(count3))
            elif 112 not in email_sets:
                subject = "Importance of joining groups on LinkedIn"
                context_dict['subject'] = "Importance of joining groups on Linkedin"
                html = render_to_string(
                    "emailers/candidate/linkedin_tip4.html", context_dict)
                send_email_from_base(
                    subject, html,
                    to=[oi.order.get_email()],
                    headers=headers, oi=oi.pk, status=112)
                count4 += 1
                logging.getLogger('info_log').info("{} tip4 mail sent".format(count4))
            elif 113 not in email_sets:
                subject = "Will you trust a profile without a profile picture?"
                context_dict['subject'] = "Will you trust a profile without a profile picture?"
                html = render_to_string(
                    "emailers/candidate/linkedin_tip5.html", context_dict)
                send_email_from_base(
                    subject, html,
                    to=[oi.order.get_email()],
                    headers=headers, oi=oi.pk, status=113)
                count5 += 1
                logging.getLogger('info_log').info("{} tip5 mail sent".format(count5))
            elif 114 not in email_sets:
                subject = "You like writing?"
                context_dict['subject'] = "You like writing?"
                html = render_to_string(
                    "emailers/candidate/linkedin_tip6.html", context_dict)
                send_email_from_base(
                    subject, html,
                    to=[oi.order.get_email()],
                    headers=headers, oi=oi.pk, status=114)
                logging.getLogger('info_log').info("{} tip6 mail sent".format(count6))
        except Exception as e:
            logging.getLogger('error_log').error(
                "%s - %s" % (str(oi.id), str(e)))

        logging.getLogger('info_log').info(
            "{} of {} tip mails sent".format(
                count1 + count2 + count3 + count4 + count5 + count6,
                orderitems.count()))
