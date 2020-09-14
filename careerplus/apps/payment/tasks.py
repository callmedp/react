# python imports
import logging
import json
from django.utils import timezone
# django imports
from django.conf import settings
from django.core.cache import cache
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
def make_logging_request(tracking_product_id, product_tracking_mapping_id, tracking_id, action, position, trigger_point, u_id, utm_campaign, domain):
    shine_api_url = settings.SHINE_API_URL
    req_dict, tracking_data = {} ,{}
    headers = dict()

    headers['content-type'] = 'application/json'
    resp = None
    url_to_hit = "{}/learning-touchpoints-tracking/".format(
        settings.SHINE_API_URL)
    tracking_id = tracking_id.strip() if isinstance(tracking_id, str) else tracking_id
    u_id = u_id.strip() if isinstance(u_id, str) else u_id
    req_dict.update({'t_id': tracking_id, 
                     'products': [product_tracking_mapping_id] if product_tracking_mapping_id else [],
                     'action': action,
                     'position': int(position) if isinstance(position, int) or position != '' else -1, 
                     'domain': domain,
                     'sub_product': tracking_product_id,
                     'trigger_point': trigger_point,
                     'u_id': u_id,
                     'utm_campaign':utm_campaign.strip() if utm_campaign.strip().lower() != 'null' else ''})
    if not product_tracking_mapping_id:
        logging.getLogger('error_log').error(
                "tracking details is missing data : {}".format(req_dict))
    try:
        resp = requests.post(
            url_to_hit, data=json.dumps(req_dict), headers=headers)
        if resp.status_code == 200:
            logging.getLogger('info_log').info(
                "send tracking data {}".format(req_dict))
            cache_data = cache.get('tracking_last_action',{})
            cache_data.update({
                str(tracking_id) : {
                        "u_id" : u_id,
                        "action" : action,
                        "products" : product_tracking_mapping_id,
                        "sub_product" : tracking_product_id,
                        "date_time" : timezone.now(),
                        "domain" : 2
                    }
                })
            cache.set('tracking_last_action',cache_data, timeout=None)
        elif not resp:
            logging.getLogger('error_log').error(
                "unable to send tracking data {}".format(req_dict))
        elif resp.status_code != 200:
            logging.getLogger('error_log').error(
                "Wrong values were sent {}".format(req_dict))
    except Exception as e:
        logging.getLogger('error_log').error(
            'thank you logging request failed.  %s' % str(e))
