# python imports
import logging
import json
# django imports
from django.conf import settings

# local imports

# inter app imports
from order.models import Order
from order.mixins import OrderMixin

# third party imports
import requests
from celery.decorators import task


@task(name="add_reward_point_in_wallet")
def add_reward_point_in_wallet(order_pk=None):
    try:
        order = Order.objects.get(pk=order_pk)
        OrderMixin().addRewardPointInWallet(order=order)
    except Exception as e:
        logging.getLogger('error_log').error(
            "unable to add reward points  in wallet %s" % (str(e)))


@task
def put_epay_for_successful_payment(epl_id, epl_market_place_id):
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(settings.EPAYLATER_INFO.get('apiKey'))}

    url_to_hit = "{}transaction/v2/{}/confirmed/{}?delivered=true".format(
        settings.EPAYLATER_INFO.get('base_url'), epl_id, epl_market_place_id)
    response = requests.put(url_to_hit, headers=headers)
    if response.status_code == 202:
        logging.getLogger('info_log').info(
            "Successfully updated EPAY for {}".format(epl_market_place_id))
    else:
        logging.getLogger('error_log').error(
            "EPAY update failed for {}".format(epl_market_place_id))


@task
def make_logging_request(tracking_product_id, product_tracking_mapping_id, tracking_id, action, position, trigger_point, u_id, utm_campaign):
    shine_api_url = settings.SHINE_API_URL
    req_dict = {}
    headers = dict()
    headers['content-type'] = 'application/json'
    resp = None
    url_to_hit = "{}/learning-touchpoints-tracking/".format(
        settings.SHINE_API_URL)
    req_dict.update({'t_id': tracking_id, 'products':
                     [product_tracking_mapping_id],
                     'action': action,
                     'position': position, 'domain': 2,
                     'sub_product': tracking_product_id,
                     'trigger_point': trigger_point,
                     'u_id': u_id,
                     'utm_campaign':utm_campaign})
    try:
        resp = requests.post(
            url_to_hit, data=json.dumps(req_dict), headers=headers)
        if resp:
            logging.getLogger('info_log').info(
                "send tracking data {}".format(req_dict))
        elif not resp:
            logging.getLogger('error_log').error(
                "unable to send tracking data {}".format(req_dict))
        elif resp.status_code != 200:
            logging.getLogger('error_log').error(
                "Wrong values were sent {}".format(req_dict))
    except Exception as e:
        logging.getLogger('error_log').error(
            'thank you logging request failed.  %s' % str(e))
