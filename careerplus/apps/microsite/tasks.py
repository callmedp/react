from __future__ import absolute_import
import urllib
import hmac
import hashlib
import logging
import requests

from django.conf import settings
from datetime import datetime, timedelta

from celery.decorators import task
from cart.models import Subscription
from order.models import Order
from shop.models import Product


@task(name="post_roundone_order")
def post_roundone_order(data_dict):
    try:
        candidateid = data_dict.get('user')
        ord_obj = Order.objects.get(id=data_dict.get('order_id'))
        if ord_obj.status == 1 and candidateid:
            roundone_order, created = Subscription.objects.get_or_create(
                candidateid=candidateid, order=ord_obj)
            if roundone_order.status != 1:
                product = Product.objects.filter(
                    id=settings.ROUNDONE_PRODUCT_ID)
                prd_amount = product[0] if product else None
                roundone_api_dict = settings.ROUNDONE_API_DICT
                data_str = ''
                api_secret_key = roundone_api_dict.get('order_secret_key')

                try:
                    billingDate = ord_obj.payment_date.date().strftime("%Y-%m-%d")
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get billing date%s' % str(e))
                    billingDate = datetime.now().strftime("%Y-%m-%d")

                data_dict = {
                    'emailId': ord_obj.email,
                    'name': ord_obj.first_name,
                    'mobile': ord_obj.mobile,
                    'amount': prd_amount.inr_price,
                    'orderId': ord_obj.id,
                    'transactionId': ord_obj.number,
                    'billingDate': billingDate,
                    'isBundled': 0,
                    'organisationId': roundone_api_dict.get('organisationId', 11),
                    'password': candidateid
                }

                data_str = '&'.join('{}={}'.format(key, value) for key, value in data_dict.items())
                data_encoded = urllib.parse.quote_plus(data_str)
                hmac_value = hmac.new(bytes(api_secret_key, 'utf-8'), bytes(data_str,'utf-8'), hashlib.sha1).hexdigest()
                post_data = {'data': data_encoded, 'hash': hmac_value}
                resp = requests.post(roundone_api_dict.get('order_save_url'), data=post_data)

                try:
                    if resp and resp.status_code == 200:
                        resp_json = resp.json()
                        if resp_json:
                            status = resp_json.get('status')
                            roundone_order.status = status
                            if status == 1 or status == "1":
                                roundone_order.remark = resp_json.get('data', resp_json)
                                roundone_order.expire_on = datetime.now() + timedelta(6*365/12)
                            else:
                                roundone_order.remark = resp_json.get('error', resp_json)
                    else:
                        print (resp.json())
                        logging.getLogger('error_log').error("%s" % (resp.json()))
                except Exception as e:
                    logging.getLogger('error_log').error(str(e))
                roundone_order.save()

    except Exception as e:
        logging.getLogger('error_log').error(str(e))
