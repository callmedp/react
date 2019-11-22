# python imports
from datetime import datetime,timedelta
# django imports
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django_redis import get_redis_connection

# local imports

# interapp imports

# 3rd party imports


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
