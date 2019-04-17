#python imports
import logging

#django imports
from django.conf import settings

#local imports

#inter app imports
from order.models import Order
from order.mixins import OrderMixin

#third party imports
import requests
from celery.decorators import task


@task(name="add_reward_point_in_wallet")
def add_reward_point_in_wallet(order_pk=None):
    try:
        order = Order.objects.get(pk=order_pk)
        OrderMixin().addRewardPointInWallet(order=order)
    except Exception as e:
        logging.getLogger('error_log').error("unable to add reward points  in wallet %s" % (str(e)))


@task
def put_epay_for_successful_payment(epl_id,epl_market_place_id):
    headers = {"Content-Type":"application/json",
        "Authorization":"Bearer {}".format(settings.EPAYLATER_INFO.get('apiKey'))}

    url_to_hit = "{}transaction/v2/{}/confirmed/{}?delivered=true".format(\
        settings.EPAYLATER_INFO.get('base_url'),epl_id,epl_market_place_id)
    response = requests.put(url_to_hit,headers=headers)
    if response.status_code == 202:
        logging.getLogger('info_log').info("Successfully updated EPAY for {}".format(epl_market_place_id))
    else:
        logging.getLogger('error_log').error("EPAY update failed for {}".format(epl_market_place_id))


