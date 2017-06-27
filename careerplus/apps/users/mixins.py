import requests
import json
import logging

from django.contrib.gis.geoip import GeoIP
from django.conf import settings

from geolocation.models import Country


class RegistrationLoginApi(object):

    @staticmethod
    def user_registration(post_data):
        response_json = {"response": "exist_user"}
        post_url = "{}/api/v2/web/candidate-profiles/?format=json".format(settings.SHINE_SITE)

        try:
            country_obj = Country.objects.get(phone=post_data['country_code'])
        except Country.DoesNotExist:
            country_obj = Country.objects.get(phone='91')

        headers = {'Content-Type': 'application/json'}
        post_data.update({"country_code": country_obj.phone})
        try:
            response = requests.post(
                post_url, data=json.dumps(post_data), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "new_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "exist_user"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            logging.getLogger('error_log').error("Error getting response from shine for"
                                                 " registration. %s " % str(e))

        return response_json

    @staticmethod
    def user_login(login_dict):
        response_json = {"response": False}
        post_url = "{}/api/v2/user/access/?format=json".format(settings.SHINE_SITE)

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                post_url, data=json.dumps(login_dict), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "login_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "error_pass"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for login. %s " % str(e))

        return response_json

    @staticmethod
    def check_email_exist(email):
        response_json = {"response": False}
        email_url = "{}/api/v3/email-exists/?email={}&format=json".format(settings.SHINE_SITE, email)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(email_url, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                response_json.update({'response': True})

        except Exception as e:
            logging.getLogger('error_log').error("Error in getting response from shine for existing email check. "
                                                 "%s " % str(e))
        return response_json


class UserMixin(object):
    def get_client_ip(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except:
            pass
        return None

    def get_client_country(self, request):
        g = GeoIP()
        ip = self.get_client_ip(request)
        try:
            if ip:
                code2 = g.country(ip)['country_code']
            else:
                code2 = 'IN'
        except:
            code2 = 'IN'

        if not code2:
            code2 = 'IN'

        code2 = code2.upper()

        try:
            country_obj = Country.objects.get(code2=code2)
        except:
            country_obj = Country.objects.get(code2='IN')

        return country_obj
