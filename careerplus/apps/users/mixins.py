import requests
import json

from cities_light.models import Country


class RegistrationLoginApi(object):

    def user_registration(self, request=None):
        try:
            post_data = {}
            response_json = {"response": False}
            post_url = "https://sumosc1.shine.com/api/v2/web/candidate-profiles/?format=json"

            try:
                country_obj = Country.objects.get(pk=request.POST.get('country_code'))
            except:
                country_obj = Country.objects.get(pk="105")

            post_data.update({
                "email": request.POST.get('email'),
                "raw_password": request.POST.get('raw_password'),
                "cell_phone": request.POST.get('cell_phone'),
                "country_code": country_obj.phone,
                "vendor_id": request.POST.get('vendor_id'),
            })

            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                post_url, data=json.dumps(post_data), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                request.session['candidate_data'] = response_json
                response_json.update({'response': "new_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "exist_user"})

            elif response.status_code == 400:
                response_json = response.json()
                response_json.update({'response': "form_error"})

        except Exception as e:
            raise e

        return response_json
        
    def user_login(self, request=None):
        try:
            post_data = {}
            response_json = {"response": False}
            post_url = "https://sumosc1.shine.com/api/v2/user/access/?format=json"

            post_data.update({
                "email": request.POST.get('email'),
                "password": request.POST.get('password') if request.POST.get('password') else request.POST.get('raw_password'),
            })

            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                post_url, data=json.dumps(post_data), headers=headers)

            if response.status_code == 201:
                response_json = response.json()
                response_json.update({'response': "login_user"})

            elif "non_field_errors" in response.json():
                response_json = response.json()
                response_json.update({'response': "error_pass"})

        except Exception as e:
            raise e

        return response_json 