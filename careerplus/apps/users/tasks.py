import string
import random
import logging

from django.conf import settings

from order.models import Order
from users.mixins import RegistrationLoginApi
from core.api_mixin import ShineCandidateDetail
from emailers.email import SendMail
from emailers.sms import SendSMS


def randompassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(6, 8)
    return ''.join(random.choice(chars) for x in range(size))


# @task(name="register user on shine")
def user_register(data={}, order=None):
    try:
        # data dict contains following data email, raw_password, country_code, cell_phone, vendor_id
        order = Order.objects.get(pk=order)
        raw_password = randompassword()
        data.update({
            "email": order.email,
            "country_code": order.country_code,
            "cell_phone": order.mobile,
            "name": order.first_name + ' ' + order.last_name,
            "vendor_id": settings.CP_VENDOR_ID,
            "raw_password": raw_password,
        })
        user_resp = RegistrationLoginApi.user_registration(data)
        candidate_id = None
        if user_resp.get('response', '') == 'exist_user':
            candidate_id = ShineCandidateDetail().get_shine_id(email=order.email)
        else:
            candidate_id = user_resp.get('id')
            # send mail to new user with user_id and password
            to_emails = [order.email]
            mail_type = "AUTO_REGISTER"
            email_data = {}
            email_data.update({
                "info": 'Your login credentials',
                "subject": 'Shine Userid and password',
                "name": order.first_name + ' ' + order.last_name,
                "mobile": order.mobile,
                "userid": order.email,
                "password": raw_password,
            })
            try:
                SendMail().send(to_emails, mail_type, email_data)
            except Exception as e:
                logging.getLogger('email_log').error("reminder cron %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))

            # try:
            #     SendSMS().send(sms_type=mail_type, data=email_data)
            # except Exception as e:
            #     logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
        if candidate_id:
            order.candidate_id = candidate_id
            order.save()
    except Exception as e:
        logging.getLogger('task_log').error(
            "%s error in user_registration task" % str(e))
        print (str(e))
