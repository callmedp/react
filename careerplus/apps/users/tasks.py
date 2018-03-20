import string
import random
import logging

from celery.decorators import task

from django.conf import settings

from order.models import Order
from users.mixins import RegistrationLoginApi
from core.api_mixin import ShineCandidateDetail
from emailers.email import SendMail


def randompassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(6, 8)
    return ''.join(random.choice(chars) for x in range(size))


@task(name="register user on shine")
def user_register(data={}, order=None):
    try:
        # data dict contains following data email, raw_password, country_code, cell_phone, vendor_id
        raw_password = randompassword()
        if not data:
            order = Order.objects.get(pk=order)
            data.update({
                "email": order.email,
                "country_code": order.country_code,
                "cell_phone": order.mobile,
                "name": order.first_name + ' ' + order.last_name,
            })
        data.update({
            "vendor_id": settings.CP_VENDOR_ID,
            "raw_password": raw_password,
        })
        user_resp = RegistrationLoginApi.user_registration(data)
        candidate_id = None
        if user_resp.get('response', '') == 'exist_user':
            candidate_id = ShineCandidateDetail().get_shine_id(email=data.get('email'))
        else:
            candidate_id = user_resp.get('id')
            # send mail to new user with user_id and password
            to_emails = [data.get('email')]
            mail_type = "AUTO_REGISTER"
            email_data = {}
            email_data.update({
                "subject": 'Your login credentials on learning.shine.com',
                "name": data.get('name'),
                "mobile": data.get('cell_phone'),
                "email": data.get('email'),
                "password": data.get('raw_password'),
            })
            try:
                SendMail().send(to_emails, mail_type, email_data)
            except Exception as e:
                logging.getLogger('error_log').error("auto regitser user task %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
        if candidate_id and order:
            order.candidate_id = candidate_id
            order.save()
        return candidate_id
    except Exception as e:
        logging.getLogger('task_log').error(
            "%s error in user_registration task" % str(e))
        print (str(e))
