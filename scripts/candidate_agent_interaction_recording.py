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

from console.models import CandidateAgentInteraction


#GLOBAL CONSTANTS

URL = settings.EXOTEL_DICT.get('record_url')
SID = settings.EXOTEL_DICT.get('sid')
TOKEN = settings.EXOTEL_DICT.get('token')



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
        return json.dumps(call_rec_dict)


def fetch_call_recording_links():
    current_time = timezone.now() - timedelta(days=1)
    userinteraction_objects = CandidateAgentInteraction.objects.filter(modified_on__gte=current_time,\
                                                                       connected=True).exclude(recording_url=None)
    for interaction_object in userinteraction_objects:
        call_rec_json = interaction_object.recording_url
        if not call_rec_json:
            continue
        call_rec_dict = json.loads(call_rec_json)
        if not call_rec_dict:
            continue
        json_value_to_storedb = get_call_record_link(call_rec_dict)
        if not json_value_to_storedb:
            continue
        interaction_object.recording_url = json_value_to_storedb
        interaction_object.save()


if __name__ == "__main__":
    fetch_call_recording_links()

