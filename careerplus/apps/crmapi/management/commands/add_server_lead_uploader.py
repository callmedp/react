import requests
import json
import logging
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from crmapi.models import AdServerLead
from cart.models import Cart


class Command(BaseCommand):
    help = """Send Lead to SHINECPCRM who didnot complete their
        transaction after inputting email address and mobile at the payment page.
        It will run at every half hour and upload to CRM"""

    def handle(self, *args, **options):

        try:
            upload_addserver_leads()
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))


def upload_addserver_leads():
    cur_datetime = timezone.now()

    cur_date_end = datetime(
        cur_datetime.year, cur_datetime.month, cur_datetime.day, 23, 59, 59)

    date_end = cur_date_end
    date_start = datetime(
        cur_datetime.year, cur_datetime.month, cur_datetime.day, 0, 0, 0)
    date_start = timezone.make_aware(
        date_start, timezone.get_current_timezone())
    date_end = timezone.make_aware(
        date_end, timezone.get_current_timezone())
    threshold_time = cur_datetime - timedelta(minutes=30)
    lead_list = AdServerLead.objects.filter(
        created=False, inactive=False, timestamp__lte=threshold_time)
    headers = {}
    headers['content-type'] = 'application/json'
    headers['Authorization'] = 'Token ' + settings.SHINECPCRM_DICT.get('token')
    post_url = settings.SHINECPCRM_DICT.get('base_url') + \
        settings.SHINECPCRM_DICT.get('ad_server_url')
    count = 0
    for ld in lead_list:
        try:
            timediff = timezone.now() - ld.timestamp
            minute_diff = timediff.seconds / 60
            if minute_diff < 30:
                continue
            else:
                cart_list = Cart.objects.filter(
                    owner_email=ld.email,
                    created__range=(date_start, date_end),
                    lead_archive=False)

                if cart_list.exists():
                    continue

                lead = {}
                email = ld.email
                country_code = ld.country_code
                mobile = ld.mobile
                lead_source = ld.source
                url = ld.url
                timestamp = ld.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                lead.update({
                    'email': email,
                    'country_code': country_code,
                    'mobile': mobile,
                    'lead_source': lead_source,
                    'timestamp': timestamp,
                    'path': url
                })
                try:
                    response = requests.post(
                        post_url,
                        data=json.dumps(lead),
                        headers=headers,
                        timeout=settings.SHINECPCRM_DICT.get('timeout'))
                    response_json = response.json()
                    if response.status_code == 200 and response_json.get('status') == 1:
                        count += 1
                        ld.created = True
                    elif response.status_code == 200 and response_json.get('status') == 0:
                        ld.inactive = True
                    ld.save()
                    print (str(count) + ' Leads Updated')
                    time.sleep(1)

                except Exception as e:
                    logging.getLogger('error_log').error("%s" % str(e))

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))

    print (str(count) + ' lead created out of ' + str(lead_list.count()))