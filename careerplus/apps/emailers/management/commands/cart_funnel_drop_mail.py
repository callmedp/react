# python imports
import logging
from datetime import datetime, date

# django imports
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.utils import timezone


# local imports
from emailers.email import SendMail

# inter app imports
from core.api_mixin import ShineCandidateDetail
from shop.models import Product
from linkedin.autologin import AutoLogin
from core.mixins import TokenGeneration

# third party imports


class Command(BaseCommand):
    """
    command to send mail
    """
    def handle(self, *args, **options):
        cart_funnel_drop_mail()

def check_interval(tracking_data):
    date_time = tracking_data.get('date_time', '')
    action = tracking_data.get('action', '')
    if not date_time and not action:
        return False
    end_hr = 2 if not settings.DEBUG else 0
    # start_interval = timezone.now() - timezone.timedelta(hours = 4)
    end_interval = timezone.now() - timezone.timedelta(hours = end_hr)
    if date_time <= end_interval and action == 'product_page':
        return True
    return False 

def send_cart_funnel_mail(send_email_list):
    mail_type = 'CART_FUNNEL_DROP'
    try:
        for email_data in send_email_list:
            u_id = email_data.get('u_id', '')
            job_title, email, name = '', '', 'Candidate'
            product = email_data.get('product', '')
            if isinstance(product, int):
                product = str(product)
            if not u_id:
                logging.getLogger('error_log').error("invalid candidate id")
                continue
            candidate_data = ShineCandidateDetail().get_candidate_detail(shine_id=u_id)
            personal_detail = candidate_data.get('personal_detail',[])
            if personal_detail and isinstance(personal_detail, list) and len(personal_detail) > 0:
                personal_detail = personal_detail[0]
                f_name = personal_detail.get('first_name', '')
                l_name = personal_detail.get('l_name', '')
                name = "{} {}".format(f_name, l_name)
                if not name.strip():
                    name = "Candidate"
                email = personal_detail.get('email', '')
            jobs = candidate_data.get('jobs', [])
            if jobs and isinstance(personal_detail, list) and len(jobs) > 0:
                job = jobs[0]
                job_title = job.get('job_title', '')

            if not email:
                logging.getLogger('error_log').error("No email available, candidate_id : {}".format(u_id))
                continue                

            email_list_spent = cache.get("email_sent_for_the_day", [])
            if email in email_list_spent:
                logging.getLogger('info_log').info(
                    "Candidate already recieved an email for the day, email: {}".format(email))
                continue
            to_email = [email]
            product_id = email_data.get('sub_product', '')
            try: 
                prod = Product.objects.filter(id=product_id).first()
            except Exception as e:
                logging.getLogger('error_log').error("product does not exist: {}".format(product_id))
                continue
            data = dict()
            data['name'] = name
            data['product_name'] = prod.heading
            data['product_url'] = prod.url
            data['product_price'] = round(prod.inr_price, 2)
            data['product_description'] = prod.meta_desc
            subject_name = "{}, ".format(name) if name != "Candidate" else ""
            data['subject'] = '{}Forgot Something?'.format(subject_name)

            token = AutoLogin().encode(email, u_id, days=None)

            data['autologin'] = "{}://{}/autologin/{}/?next=/search/results/?q={}".format(settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token, job_title)
            if product == '8':
                token = TokenGeneration().encode(email, 2, 30)
                data['autologin'] = "{}/myshine/login/?tc={}&next=/myshine/myprofile/".format(settings.SHINE_SITE, token) ## add autologin token

            email_list_spent.append(email)
            cache.set("email_sent_for_the_day", email_list_spent, timeout = None)
            try:
                SendMail().send(to_email, mail_type, data)
                logging.getLogger('info_log').info("cart product removed mail successfully sent {}".format(email))
            except Exception as e:
                logging.getLogger('error_log').error("Unable to sent mail: {}".format(e))
            # make_logging_request.delay(
            #     tracking_product_id, product_tracking_mapping_id, tracking_id, 'remove_product_mail_sent', position, trigger_point, u_id, utm_campaign, domain)
        
    except Exception as e:
         logging.getLogger('error_log').error("Unable to send mail, reason: {}".format(e))

def cart_funnel_drop_mail():
    """
    function too send mail to users who 
    looked at the products but didn't add the product to cart
    """
    end_hr = 2 if not settings.DEBUG else 0
    end_interval = timezone.now() - timezone.timedelta(hours = end_hr)
    tracking_data = cache.get('tracking_last_action', {})
    send_email_list, tracking_dict = [] , {}

    for key in tracking_data:
        track_dict = tracking_data[key]
        if track_dict.get('date_time', '') and track_dict.get('date_time') > end_interval:
            tracking_dict.update({ key : track_dict })
        elif track_dict.get('date_time', '') and check_interval(track_dict):
            user_data = {
                "tracking_id" : key,
                "u_id" : track_dict.get('u_id', ''),
                "product" : track_dict.get('products', ''),
                "sub_product" : track_dict.get('sub_product', ''),
            }
            send_email_list.append(user_data)


    cache.set('tracking_last_action', tracking_dict, timeout=None)
    logging.getLogger('info_log').info('cart mail drop tracking data has been filtered')

    send_cart_funnel_mail(send_email_list)


