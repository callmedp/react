import logging
import json
import requests
import sys,os,django


#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()


from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from order.models import WelcomeCallOperation
from emailers.email import SendMail


#GLOBAL CONSTANTS

URL = settings.EXOTEL_DICT.get('record_url')
SID = settings.EXOTEL_DICT.get('sid')
TOKEN = settings.EXOTEL_DICT.get('token')
FAILS, SUCCESS,TOTAL = 0, 0, 0

def get_call_recording_request(callid):
    url_to_hit = URL.format(sid=SID,token=TOKEN,callid=callid)
    try:
        response = requests.get(url_to_hit)
        status = response.status_code
        response_in_json = response.json()

    except Exception as e:
        logging.getLogger('error_log').error('{}-{}'.format(callid, str(e)))
        return

    if not status == 200:
        logging.getLogger('info_log').info('{} - {} Request not completed'.format(callid, response))
        return

    callrecord = response_in_json.get('Call', '')
    if not callrecord:
        logging.getLogger('info_log').info('{} - Not Call record Found'.format(callid))
        return

    record_url = callrecord.get('RecordingUrl', None)
    if not record_url:
        logging.getLogger('info_log').info('{} - Not Call recording found Found'.format(callid))
        return
    return record_url


def get_call_record_link(call_rec_dict):
    global TOTAL
    for key, value in call_rec_dict.items():
        record_url = None
        if not value:
            record_url = get_call_recording_request(key)
            if not record_url:
                continue
            call_rec_dict.update({key: record_url})
        else:
            continue
    if call_rec_dict:
        TOTAL += 1
        return json.dumps(call_rec_dict)


def fetch_call_recording_links():
    global SUCCESS, FAILS
    current_time = timezone.now() - timedelta(days=1)
    welcome_calls = WelcomeCallOperation.objects.filter(modified__gte=current_time)
    for wc in welcome_calls:
        order = wc.order
        call_rec_json = order.welcome_call_records
        if not call_rec_json:
            continue
        call_rec_dict = json.loads(call_rec_json)
        if not call_rec_dict:
            FAILS += 1
            continue
        json_value_to_storedb = get_call_record_link(call_rec_dict)
        if not json_value_to_storedb:
            FAILS += 1
            continue
        order.welcome_call_records = json_value_to_storedb
        order.save()
        SUCCESS += 1

def mail_report():

    global TOTAL, SUCCESS, FAILS
    send_dict = {}

    send_dict['subject'] = "Welcome Call Recording Report " + timezone.now().strftime("%Y-%m-%d ")
    send_dict['to'] = ["vishal.gupta@hindustantimes.com", "animesh.sharma@hindustantimes.com"]
    send_dict['cc'] = ["gaurav.chopra1@hindustantimes.com"]

    send_dict['body'] = '<html><head></head><body>' \
                        '<table  style="border: 1px solid black;"> <tr  style="border: 1px solid black;">' \
                        '<th style="border: 1px solid black;">Total Count</th><th  style="border: 1px solid black;">' \
                        'Success</th><th style="border: 1px solid black;">Fails</th></tr>' \
                        '<tr style="border: 1px solid black;"><td style="border: 1px solid black;">' \
                        ''+str(TOTAL)+'</td><td style="border: 1px solid black;">'+str(SUCCESS)+\
                        '</td><td style="border: 1px solid black;">'+str(FAILS) +\
                        '</td></table></body></html>'

    send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
    SendMail().base_send_mail(subject=send_dict['subject'], body=send_dict['body'], to=send_dict['to'],\
                              cc=send_dict['cc'], from_email=send_dict['from_email'], mimetype='text')


if __name__ == "__main__":

    fetch_call_recording_links()
    logging.getLogger('info_log').info('{} Total - {} Success - {} Failures '.format(TOTAL,SUCCESS,FAILS))
    mail_report()

