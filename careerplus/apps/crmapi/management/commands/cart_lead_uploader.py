import requests
import json
import logging
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from cart.models import Cart
from cart.mixins import CartMixin


class Command(BaseCommand):
    help = """Send Lead to SHINECPCRM who didnot complete their
        transaction after inputting email address and mobile at the payment page.
        It will run at every one hour and upload to CRM"""

    def handle(self, *args, **options):

        try:
            upload_cart_leads()
        except Exception as e:
            logging.getLogger('error_log').error("unable to upload cart leads%s" % str(e))


def upload_cart_leads():
    cart_objs = Cart.objects.filter(
        status__in=[2, 3],
        owner_id__isnull=False,
        lead_archive=False).exclude(owner_id__exact='')
    headers = {}
    headers['content-type'] = 'application/json'
    headers['Authorization'] = 'Token ' + settings.SHINECPCRM_DICT.get('token')
    post_url = settings.SHINECPCRM_DICT.get('base_url') + \
        settings.SHINECPCRM_DICT.get('update_cartleads_url')
    count = 0
    for cart_obj in cart_objs:
        try:
            lead = {}
            name = "{} {}".format(cart_obj.first_name, cart_obj.last_name)
            mobile = cart_obj.mobile
            if cart_obj.country_code:
                country_code = cart_obj.country_code
            else:
                country_code = 91
            cart_mixin = CartMixin()
            payment_dict = cart_mixin.getPayableAmount(cart_obj, 0)
            amount_payable = payment_dict.get('total_payable_amount', 0)
            lead["id"] = cart_obj.id
            lead["name"] = str(name)
            lead["email"] = str(cart_obj.email)
            lead["country_code"] = str(country_code)
            lead["mobile"] = str(mobile)
            lead["message"] = 'total amount {}'.format(str(amount_payable))
            lead["status"] = 0
            lead["source"] = str('Cart Leads')
            lead["lsource"] = int(16)
            lead["product"] = str('product')
            lead["medium"] = int(0)
            try:
                response = requests.post(
                    post_url,
                    data=json.dumps(lead),
                    headers=headers,
                    timeout=settings.SHINECPCRM_DICT.get('timeout'))
                if response.status_code == 200:
                    count += 1
                    pass
                    cart_obj.lead_archive = True
                    cart_obj.save()
                time.sleep(1)
                logging.getLogger('info_log').info("{} Leads Updated".format(count))
            except Exception as e:
                logging.getLogger('error_log').error("%s" % str(e))
        except Exception as e:
            logging.getLogger('error_log').error("Error in cart lead cron : %s" % str(e))
