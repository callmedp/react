import requests
import json
import logging

from django.contrib.gis.geoip import GeoIP

from geolocation.models import Country


class RegistrationLoginApi(object):

    def user_registration(self, post_data):
        try:
            response_json = {"response": False}
            post_url = "https://sumosc1.shine.com/api/v2/web/candidate-profiles/?format=json"

            try:
                country_obj = Country.objects.get(pk=post_data['country_code'])
            except:
                country_obj = Country.objects.get(pk="105")

            headers = {'Content-Type': 'application/json'}
            post_data.update({"country_code": country_obj.phone})
            response = requests.post(
                post_url, data=json.dumps(post_data), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "new_user"})
                request.session['candidate_data'] = response_json

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "exist_user"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

        return response_json
        
    def user_login(self, login_dict):
        try:
            response_json = {"response": False}
            post_url = "https://sumosc1.shine.com/api/v2/user/access/?format=json"

            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                post_url, data=json.dumps(login_dict), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "login_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "error_pass"})

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

        return response_json
    
    def check_email_exist(self, email):
        try:
            response_json = {"response": False}
            email_url = "https://sumosc1.shine.com/api/v3/email-exists/?email={}&format=json".format(email,)
            headers = {'Content-Type': 'application/json'}
            response = requests.get(email_url, headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                response_json.update({'response': True})

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

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
