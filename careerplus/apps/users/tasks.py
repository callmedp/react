import string
import random

from order.models import Order
from users.mixins import RegistrationLoginApi


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
            "vendor_id": '12345',
            "raw_password": raw_password,
        })
        user_resp = RegistrationLoginApi.user_registration(data)
        candidate_id = user_resp.get('id')
        order.candidate_id = candidate_id
        order.save()
        # send mail to new user with user_id and password
    except Exception as e:
        print (str(e))
