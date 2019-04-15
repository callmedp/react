import requests
import json
import logging
from django.conf import settings


URL = settings.EXOITEL.get('url', '')
TOKEN = settings.EXOITEL.get('token', '')
SID = settings.EXOITEL.get('sid', '')
CALLER_ID = settings.EXOITEL.get('callerid', '')
DND_CHECK_URL = settings.EXOITEL.get('check_dnd_url', '')

class ExotelMixin(object):

    def make_call(self, to, agent_number):
        req_dict = {}
        resp = None
        url_to_hit = URL.format(sid=SID, token=TOKEN)
        req_dict.update({'To': '0' + str(to), 'From': str(agent_number), 'CallerId': CALLER_ID})
        try:
            resp = requests.post(url_to_hit, data=req_dict)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return resp

    def get_dnd_info(self,number):
        url_to_hit = DND_CHECK_URL.format(sid=SID,token=TOKEN,number=number)
        resp = None
        try:
            resp = requests.get(url_to_hit)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return
        if resp.status_code == 200:
            res_in_json = resp.json()
            number = res_in_json.get('Numbers',None)
            if not number:
                return
            dnd = number.get('DND','')
            if not dnd:
                return
            return dnd

        else:
            logging.getLogger('info_log').info('dnd for {} - {}'.format(number, str(e)))
            return




