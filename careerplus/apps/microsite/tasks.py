from __future__ import absolute_import
import urllib
import hmac
import hashlib
import logging
import csv
import requests

from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from order.models import Order

from celery.decorators import task
from cart.models import Subscription

@task
def post_roundone_order(data_dict):
    try: 
        candidateid = data_dict.get('user')
        order = data_dict.get('order')
        if order and candidateid:
            roundone_order, created = Subscription.objects.get_or_create(
                candidateid=candidateid, order=order)
            if order.status != 2:
                roundone_api_dict = settings.ROUNDONE_API_DICT
                data_str = ''
                api_secret_key = roundone_api_dict.get('order_secret_key')

                try:
                    billingDate = order.date_placed.date().strftime("%Y-%m-%d")
                except:
                    billingDate = datetime.now().strftime("%Y-%m-%d")

                data_dict = {
                    'emailId': order.email,
                    'name': order.first_name,
                    'common': order.mobile,
                    'amount': roundone_api_dict.get('amount', 1999),
                    'orderId': order.id,
                    'transactionId': order.number,
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
                                # roundone_order.remark = resp_json.get('data', resp_json)
                                roundone_order.added_on = datetime.now()
                                roundone_order.expire_on = datetime.now() + timedelta(6*365/12)
                            else:
                                pass
                                # roundone_order.remark = resp_json.get('error', resp_json)
                except Exception as e:
                    logging.getLogger('error_log').error(str(e))
                roundone_order.save()

    except Exception as e:
        logging.getLogger('error_log').error(str(e))

