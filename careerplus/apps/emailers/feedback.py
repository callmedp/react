import logging
import datetime
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import Order, OrderItem, EmailOrderItemOperation
from emailers.email import SendMail
from linkedin.autologin import AutoLogin
from emailers.tasks import send_email_for_base_task

def feedback_emailer():
    try:
        order_items = OrderItem.objects.filter(oi_status=4)
        today_date = timezone.now()
        data_dict = {}
        for oitem in order_items:
            email_sets = list(oitem.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
            if today_date >= oi_item.closed_on + datetime.timedelta(days=4) and 5 not in email_sets:
                subject = 'Your order has been processed. Give feedback and earn discount on the next order'
                data_dict['orderid'] = oi_item.order.id
                data_dict['username'] = oi_item.order.first_name if oi_item.order.first_name else oi_item.order.candidate_id
                data_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                token = AutoLogin().encode(oi_item.order.email, oi_item.order.candidate_id, oi_item.order.id)
                data_dict['autologin'] = "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())
                html = render_to_string(
                        'emailers/candidate/feedback.html', data_dict)
                headers_dict = {'Reply-To': settings.REPLY_TO}
                return_val = send_email_for_base_task.delay(subject, html, to=[oi_item.order.email], headers=headers_dict)
                if return_val.result:
                    oitem.emailorderitemoperation_set.create(email_oi_status=5)                     
    except:
        pass
    
