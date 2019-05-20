import requests
import json
import logging

from django.conf import settings

class VskillTest(object):

    def get_token(self):
        headers = {'Content-Type': 'application/json'}
        token, response = None, None
        try:
            response = requests.post(settings.VSKILLS_EXAM_DICT.get('login_url'), headers=headers \
                                     , data=settings.VSKILLS_EXAM_DICT.get('credential'), allow_redirects=False)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting vskill login response  {}'.format(str(e)))

        if response.status_code == 200:
            response_json = json.loads(response.text)
            token = response_json.get('jwt')
        else:
            logging.getLogger('info_log').info('Unable to get status 200 in login ')
        return token


    def get_all_test(self, token):
        response = None
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(settings.VSKILLS_EXAM_DICT.get('get_all_test_url').format(token), \
                                    headers=headers, data=settings.VSKILLS_EXAM_DICT.get('credential'),
                                    allow_redirects=False)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting vskill all test response  {}'. \
                                                 format(str(e)))

        if response.status_code == 200:
            response = json.loads(response.text)
        else:
            logging.getLogger('info_log').info('Unable to get status 200 in all test ')
        return response


    def get_test_by_id(self, token, test_id):
        if not test_id or not token:
            return
        response = None
        headers = {
            'Content-Type': 'application/json'}
        files = {}
        data = {'testid': test_id}
        try:
            response = requests.get(settings.VSKILLS_EXAM_DICT.get('get_single_test_url') \
                                    .format(token, test_id), headers=headers, data=json.dumps(data), files=files,
                                    allow_redirects=False)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting vskill single test id {} response  {}' \
                                                 .format(test_id, str(e)))

        if response.status_code == 200:
            response = response.text
        else:
            logging.getLogger('info_log').info('Unable to get status 200 in single test id {}'. \
                                               format(test_id))
            response = None
        return response
