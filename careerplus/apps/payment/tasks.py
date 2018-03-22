import logging

from celery.decorators import task

from order.mixins import OrderMixin
from order.models import Order


@task(name="add_reward_point_in_wallet")
def add_reward_point_in_wallet(order_pk=None):
    try:
        order = Order.objects.get(pk=order_pk)
        OrderMixin().addRewardPointInWallet(order=order)
    except Exception as e:
        logging.getLogger('error_log').error("unable to add reward points  in wallet %s" % (str(e)))