import requests
import json
import logging
from datetime import datetime,timedelta

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django_redis import get_redis_connection

from .config import *

from .models import Question

class VskillTest(object):

    def get_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
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

    def get_all_test(self):
        token = self.get_token()
        if not token:
            logging.getLogger('info_log').info('unable to create token')
            return
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

    def get_all_test_id(self):
        all_test = self.get_all_test()
        if not all_test:
            return []
        return [prod.get('shine_id') for prod in all_test.get('data',[])]

    def get_test_by_id(self, test_id):
        token = self.get_token()
        if not test_id or not token:
            return
        response = None
        headers = {}
        data = {}
        try:
            response = requests.get(settings.VSKILLS_EXAM_DICT.get('get_single_test_url') \
                                    .format(token, test_id), headers=headers, data=data,
                                    allow_redirects=False)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting vskill single test id {} response  {}' \
                                                 .format(test_id, str(e)))

        if response.status_code == 200:
            response = json.loads(response.text)
        else:
            logging.getLogger('info_log').info('Unable to get status 200 in single test id {}'. \
                                               format(test_id))
        return response


class VskillParser:

    def get_question_type(self,option_list):
        return 2 if len([option.get('option_id') for option in option_list\
                if option.get('is_correct') and bool(eval(option.get('is_correct'))\
                if isinstance(option.get('is_correct'), str) else option.get(
                'is_correct'))]) > 1 else 1


    def prepare_questions(self,data_list,test):
        if not data_list:
            return
        data_list = data_list.get('data')
        prepared_test = 0
        if not data_list or not isinstance(data_list, list):
            return
        for data in data_list:
            create_dict = {'test_id': test}
            question_type = None
            question = Question.objects.create()

            if not question:
                logging.getLogger('error_log').error('unable to create '
                                                     'question')
                continue
            prepared_test += 1

            for key, values in PARSER_FIELDS.get('Vskills').items():
                if key == "question_options":
                    val,question_type = self.prepare_json_options(data.get(values),
                                                    question.id)
                    create_dict.update({key: val})
                    continue
                create_dict.update({key: data.get(values)})
            if question_type == 2:
                create_dict.update({'question_type': question_type})
            for key, value in create_dict.items():
                setattr(question, key, value)
            question.save()
        logging.getLogger('info_log').info('total {} question object '
                                           'created'.format(prepared_test))

    def prepare_json_options(self, data, question_id):
        if not data or not isinstance(data, list) or not question_id:
            return

        option_list = []
        for index, option in enumerate(data,start=1):
            option_dict = {}
            option_dict.update({'option_image': str(option.get(
                'option_image'))})
            option_dict.update({"option": option.get("option")})

            # we are creating our own option_ids

            option_dict.update({"option_id": str(question_id) +
                                             str(ANSWER_MAPPING_DICT.get(
                                                 index)),
                                "is_correct": option.get("is_correct")})
            option_list.append(option_dict)
        quest_type = self.get_question_type(option_list)

        return json.dumps(option_list), quest_type


class TestCacheUtil:
    VSKILL_CACHE_TIMEOUT = 24*60*60

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        if not self.request:
            raise ImproperlyConfigured
        self.session_id = self.request.session.session_key
        self.time_format = "%m/%d/%Y, %H:%M:%S"
        self.test_timeout = None

    def get_cache(self,key):
        cache_key = self.session_id + str(key)
        return cache.get(cache_key) if cache.get(cache_key) else {}

    def show_test_remove_local_storage(self,key):
        test_dict = self.get_cache(key)
        if not test_dict:
            return True, True
        test_duration_time = test_dict.get('test_duration')
        if not test_duration_time:
            return True, True
        timestamp_obj = datetime.strptime(test_duration_time, self.time_format)
        if timestamp_obj < datetime.now() or self.get_test_submit(key):
            if not self.get_test_time_out(key) and not self.get_test_submit(key):
                self.set_test_time_out(key)
            return False, False
        return True, False

    def set_test_duration_cache(self,key,duration):

        test_dict = self.get_cache(key)
        data = {}
        timestamp_with_tduration = (datetime.now() + timedelta(seconds=duration)) \
            .strftime(self.time_format)
        data.update({'test_duration': timestamp_with_tduration})
        if not test_dict:
            return self.set_cache_data(key,data)
        test_dict.update(**data)
        return self.set_cache_data(key,test_dict)

    def get_test_duration_cache(self,key,duration):
        test_dict = self.get_cache(key)
        if not test_dict or not test_dict.get('test_duration'):
            return self.set_test_duration_cache(key,duration)
        return test_dict.get('test_duration')

    def set_start_test_time_cache(self, key):
        test_dict = self.get_cache(key)
        data = {}
        start_test_time = datetime.now().strftime(self.time_format)
        data.update({'start_test_time': start_test_time})
        if not test_dict:
            return self.set_cache_data(key,data)
        test_dict.update({**data})
        return self.set_cache_data(key,test_dict)

    def get_start_test_cache(self,key):
        if not self.get_cache(key) or not self.get_cache(key).get('start_test_time'):
            return self.set_start_test_time_cache(key).get('start_test_time')
        return self.get_cache(key).get('start_test_time')

    def get_test_time_out(self,key):
        return False if not self.get_cache(key) else self.get_cache(key).get('timeout')

    def set_test_time_out(self,key, data=True):
        data = {'timeout':data}
        test_dict = self.get_cache(key)
        test_dict.update(**data)
        return self.set_cache_data(key,test_dict)

    def get_test_submit(self,key):
        return False if not self.get_cache(key) else self.get_cache(key).get('test_submit')

    def set_test_submit(self, key, data=True):
        data = {'test_submit': data}
        test_dict = self.get_cache(key)
        test_dict.update(**data)
        return self.set_cache_data(key,test_dict)

    def set_cache_data(self, key, data):
        key = self.session_id + key
        timeout = None
        if not self.test_timeout:
            conn = get_redis_connection('test_lookup')
            redis_key = str.encode(':' + str(settings.CACHES.get('test_lookup').get('LOCATION')[0].split("/")[-1])+":"+key)
            timeout = conn.pttl(redis_key)
        if not timeout or timeout == -2:
            timeout = self.VSKILL_CACHE_TIMEOUT
        cache.set(key,data,timeout)
        return cache.get(key)




        #
        # if not timestamp:
        #     timestamp_with_tduration = (datetime.now() + timedelta(seconds=duration)).strftime(timeformat)
        #     test_ids = {'ongoing_' + str(test_id): timestamp_with_tduration}
        #     cache.set(test_session_key, test_ids, 60 * 60 * 24)
        #
        # elif timestamp and not timestamp.get('ongoing_' + str(test_id)):
        #     timestamp_with_tduration = (datetime.now() + timedelta(seconds=duration)).strftime(
        #         "%m/%d/%Y, %H:%M:%S")
        #     test_ids = {'ongoing_' + str(test_id): timestamp_with_tduration}
        #     cache.set(test_session_key, test_ids, 60 * 60 * 24)
        #
        # if not cache.get(session_id + 'startTest-' + str(test_id)):
        #     cache.set(session_id + 'startTest-' + str(test_id), datetime.now().strftime(timeformat),
        #               60 * 60 * 24)
        # return Response({'testStartTime': cache.get(session_id + 'startTest-' + str(test_id))})
