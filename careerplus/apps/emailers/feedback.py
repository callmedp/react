import logging
import datetime
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from linkedin.autologin import AutoLogin
from emailers.tasks import send_email_for_base_task


def feedback_emailer():
    order_items = OrderItem.objects.filter(oi_status=4)
    today_date = timezone.now()
    data_dict = {}
    for oi_item in order_items:
        email_sets = list(
            oi_item.emailorderitemoperation_set.all().values_list(
                'email_oi_status', flat=True).distinct())
        try:
            if today_date >= oi_item.closed_on + datetime.timedelta(days=4) and 5 not in email_sets:
                subject = 'Your order has been processed. Give feedback and earn discount on the next order'
                data_dict['orderid'] = oi_item.order.id
                data_dict['username'] = oi_item.order.first_name
                data_dict['site'] = settings.SITE_PROTOCOL + '://' + settings.SITE_DOMAIN + settings.STATIC_URL
                token = AutoLogin().encode(
                    oi_item.order.email, oi_item.order.candidate_id,
                    oi_item.order.id)
                data_dict['autologin'] = "%s://%s/autologin/%s/?next=dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token.decode())
                data_dict['order_detail'] = "%s://%s/autologin/%s/?next=/dashboard/myorder/" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token.decode())
                html = render_to_string(
                    'emailers/candidate/feedback.html', data_dict)
                headers_dict = {'Reply-To': settings.REPLY_TO}
                send_email_for_base_task.delay(
                    subject, html, to=[oi_item.order.email],
                    headers=headers_dict, oi=oi_item.pk, status=5)
        except Exception as e:
            logging.getLogger('email_log').error(
                "%s - %s" % (str(oi_item), str(e)))