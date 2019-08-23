import requests
import json
import logging
from requests import Response
from django.conf import settings

from console.models import CandidateAgentInteraction

class ExotelInteraction(object):
    url = settings.EXOTEL_DICT.get('url', '')
    token = settings.EXOTEL_DICT.get('token', '')
    sid = settings.EXOTEL_DICT.get('sid', '')
    caller_id = settings.EXOTEL_DICT.get('callerid', '')
    dnd_check_url = settings.EXOTEL_DICT.get('check_dnd_url', '')

    def make_call(self, to, agent_number):
        req_dict = {}
        resp = None
        url_to_hit = self.url.format(sid=self.sid, token=self.token)
        req_dict.update({'To': '0' + str(to), 'From': str(agent_number), 'CallerId': self.caller_id})
        try:
            resp = requests.post(url_to_hit, data=req_dict)
        except Exception as e:
            logging.getLogger('error_log').error('response for {} - {}'.format(to, str(e)))
            return Response()
        return resp

    def is_number_dnd(self,number):
        url_to_hit = self.dnd_check_url.format(sid=self.sid,token=self.token,number=number)
        resp = None
        try:
            resp = requests.get(url_to_hit)
        except Exception as e:
            logging.getLogger('error_log').error('response for {} - {}'.format(number, str(e)))
            return
        if not resp.status_code == 200:
            logging.getLogger('info_log').info('response for {} - {}'.format(number, resp.text))
            return

        res_in_json = resp.json()
        return bool(res_in_json.get('Numbers', {}).get('DND',"").lower() == "yes")

    def create_user_agent_interaction(self,order,user,recording_url=None,queue_name=0):
        if not order or not user:
            return
        user = user if user else ""
        order = order if order else ""
        candidate_id = order.candidate_id if order else ""
        create_dict = {'recording_url':recording_url, 'candidate_id':candidate_id,\
                       'called_by':user, 'queue_name':queue_name, 'order' : order}
        if recording_url:
            create_dict.update({'connected': True})
        caid=CandidateAgentInteraction(**create_dict)
        caid.save()








