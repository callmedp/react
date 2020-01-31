import logging
import datetime
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import OrderItem
from linkedin.autologin import AutoLogin
from emailers.tasks import send_email_for_base_task
from core.decorators import run_cron

@run_cron
def feedback_emailer(cron_name):
    today_date = timezone.now() - datetime.timedelta(days=4)
    order_items = OrderItem.objects.filter(
        oi_status=4, closed_on__lte=today_date).exclude(
        emailorderitemoperation__email_oi_status=5).select_related('order')
    data_dict = {}
    for oi_item in order_items:
        try:
            subject = 'Your order has been processed. Give feedback and earn discount on the next order'
            data_dict['orderid'] = oi_item.order.id
            data_dict['item_id'] = oi_item.id
            data_dict['username'] = oi_item.order.first_name
            data_dict['static_site_url'] = settings.STATIC_URL

            token = AutoLogin().encode(
                oi_item.order.email, oi_item.order.candidate_id,
                oi_item.order.id)
            data_dict['autologin'] = "%s://%s/autologin/%s/?next=/dashboard/" % (
                settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                token)
            data_dict['order_detail'] = "%s://%s/autologin/%s/?next=/dashboard/myorder/" % (
                settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                token)
            html = render_to_string(
                'emailers/candidate/feedback.html', data_dict)
            headers_dict = {'Reply-To': settings.REPLY_TO}
            send_email_for_base_task.delay(
                subject, html, to=[oi_item.order.get_email()],
                headers=headers_dict, oi=oi_item.pk, status=5)
        except Exception as e:
            logging.getLogger('error_log').error(
                "%s - %s" % (str(oi_item), str(e)))