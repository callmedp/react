import logging
import datetime
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from order.models import Order, OrderItem, EmailOrderItemOperation
from emailers.email import SendMail
from linkedin.autologin import AutoLogin

def feedback_emailer():
    try:
        order_items = OrderItem.objects.filter(oi_status=4)
        today_date = timezone.now()
        data_dict = {}
        for oitem in order_items:
            oi_item = oitem
            email_status = oi_item.emailorderitemoperation_set.all()
            if email_status:
                for email_obj in email_status:
                    if today_date >= oi_item.closed_on + datetime.timedelta(days=4) and email_obj.email_oi_status != 6:
                        subject = 'Your order has been processed. Give feedback and earn discount on the next order'
                        data_dict['orderid'] = oi_item.order.id
                        data_dict['username'] = oi_item.order.first_name if oi_item.order.first_name else oi_item.order.candidate_id
                        data_dict['site'] = 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
                        token = AutoLogin().encode(oi_item.order.email, oi_item.order.candidate_id, oi_item.order.id)
                        data_dict['autologin'] = "http://%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode())
                        html = render_to_string(
                            'emailers/candidate/feedback.html', data_dict)
                        headers_dict = {'Reply-To': settings.REPLY_TO}
                        try:
                            SendMail().base_send_mail(
                                subject, html, to=[oi_item.order.email], headers=headers_dict)
                            email_obj.oi = oi_item
                            email_obj.email_oi_status = 6
                            email_obj.save()
                        except Exception as e:
                            logging.getLogger('email_log').error("feedback email %s" % (str(oi_item)))
            else:
                if today_date >= oi_item.closed_on + datetime.timedelta(days=4):
                    subject = 'Your order has been processed. Give feedback and earn discount on the next order'
                    data_dict['orderid'] = oi_item.order.id
                    data_dict['username'] = oi_item.order.first_name if oi_item.order.first_name else oi_item.order.candidate_id
                    token = AutoLogin().encode(oi_item.order.email, oi_item.order.candidate_id, oi_item.order.id)
                    data_dict['autologin'] = "http://%s/autologin/%s/" % (settings.SITE_DOMAIN, token)
                    html = render_to_string(
                        'emailers/candidate/feedback.html', data_dict)
                    headers_dict = {'Reply-To': settings.REPLY_TO}
                    try:
                        SendMail().base_send_mail(
                            subject, html, to=[oi_item.order.email], headers=headers_dict)
                        EmailOrderItemOperation.objects.create(oi=oi_item, email_oi_status = 6)
                    except Exception as e:
                        logging.getLogger('email_log').error("feedback email %s" % (str(oi_item)))  
    except:
        pass
    
