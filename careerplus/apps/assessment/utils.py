import requests
import json
import logging

from django.conf import settings
from .config import *

from .models import Question

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
            response = json.loads(response.text)
        else:
            logging.getLogger('info_log').info('Unable to get status 200 in single test id {}'. \
                                               format(test_id))
            response = None
        return response


class VskillParser:

    def prepare_questions(self,data_list,test):

        if not data_list or not isinstance(data_list, list):
            return

        create_dict = {'test_id': test}

        for data in data_list:
            for key, values in PARSER_FIELDS.get('Vskills').items():
                if key == "question_options":
                    val = self.prepare_json_options(data.get(values))
                    create_dict.update({key: val})
                create_dict.update({key: data.get(values)})
            Question.objects.get_or_create(**create_dict)

    def prepare_json_options(self, data):
        if not data or not isinstance(data, list):
            return
        option_dict = {}
        option_list = []
        for option in data:
            if option.get('option_image'):
                option_dict.update({"question_options": option.get('option') + str(option.get('option_image'))})
            else:
                option_dict.update({"question_options": option.get("option")})

            option_dict.update({"option_id": option.get("option_id"),
                                "is_correct": [option.get("is_correct")]})
            option_list.append(option_dict)

        return json.dumps(option_list)

