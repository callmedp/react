import logging
import base64
import requests
import json
from Crypto.Cipher import XOR

from django.conf import settings


class ShineToken(object):
    def get_client_token(self):
        try:
            headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
            client_access_url = settings.SHINE_SITE + '/api/v2/client/access/?format=json'
            client_data = {'key': settings.CLIENT_ACCESS_KEY, 'secret': settings.CLIENT_ACCESS_SECRET}
            client_access_resp = requests.post(client_access_url, data=client_data, headers=headers)
            client_access_resp_json = client_access_resp.json()
            if client_access_resp.status_code == 201:
                return client_access_resp_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting client token%s'%str(e))
        return None

    def get_access_token(self):
        try:
            headers = {
                "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
            user_access_url = settings.SHINE_SITE + '/api/v2/user/access/?format=json'
            user_data = {"email": settings.SHINE_API_USER, "password": settings.SHINE_API_USER_PWD}
            user_access_resp = requests.post(user_access_url, data=user_data, headers=headers)
            user_access_resp_json = user_access_resp.json()
            if user_access_resp.status_code == 201:
                return user_access_resp_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error('error in accessing token %s'%str(e))
        return None

    def get_api_headers(self):
        try:
            client_token = self.get_client_token()
            if client_token:
                access_token = self.get_access_token()
                if access_token:
                    headers = {"User-Access-Token": access_token,
                               "Client-Access-Token": client_token,
                               "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
                    return headers
        except Exception as e:
            logging.getLogger('error_log').error('error in getting header %s'%str(e))
        return None


class ShineCandidateDetail(ShineToken):

    def get_shine_id(self, email=None, headers=None):
        try:
            if not headers:
                headers = self.get_api_headers()
            if email and headers:
                shine_id_url = settings.SHINE_SITE +\
                    "/api/v2/candidate/career-plus/email-detail/?email=" +\
                    email + "&format=json"
                shine_id_response = requests.get(
                    shine_id_url, headers=headers,
                    timeout=settings.SHINE_API_TIMEOUT)
                if shine_id_response and shine_id_response.status_code == 200 and shine_id_response.json():
                    shine_id_json = shine_id_response.json()
                    if shine_id_json:
                        shine_id = shine_id_json[0].get("id", None)
                        return shine_id
        except Exception as e:
            logging.getLogger('error_log').error('unable to get shine id  %s'%str(e))
        return None

    def get_candidate_detail(self, email=None, shine_id=None):
        try:
            if shine_id:
                headers = self.get_api_headers()
                detail_url = settings.SHINE_SITE +\
                        "/api/v2/candidate-profiles/" +\
                        shine_id + "/?format=json"
                detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if detail_response.status_code == 200 and detail_response.json():
                    return detail_response.json()
                logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
                    format(email,shine_id))
                return {}
            
            elif email:
                headers = self.get_api_headers()
                shine_id = self.get_shine_id(email=email, headers=headers)
                if shine_id:
                    detail_url = settings.SHINE_SITE +\
                        "/api/v2/candidate-profiles/" +\
                        shine_id + "/?format=json"
                    detail_response = requests.get(detail_url, headers=headers)
                    if detail_response.status_code == 200 and detail_response.json():
                        return detail_response.json()
                    
                    logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
                    format(email,shine_id))
                    return {}
                
                logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
                    format(email,shine_id))
                return {}

            logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
                    format(email,shine_id))
            return {}
        except Exception as e:
            logging.getLogger('error_log').error('unable to get candidate details%s'%str(e))

        logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
                    format(email,shine_id))
        return {}

    def get_candidate_public_detail(self, email=None, shine_id=None):

        headers = self.get_api_headers()

        if not shine_id and email:
            shine_id = self.get_shine_id(email=email, headers=headers)
        elif not email and not shine_id:
            logging.getLogger('error_log').error("Email ID or shine_id required for profile")
            return
        detail_url = settings.SHINE_SITE + \
            "/api/v2/candidate-public-profiles/" + \
                shine_id + "/?format=json"
        try:
            detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
            if detail_response.status_code == 200 and detail_response.json():
                return detail_response.json()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get detail response %s'%str(e))
        return

    def get_status_detail(self, email=None, shine_id=None, token=None):
        try:
            if shine_id:
                headers = self.get_api_headers()
                status_url = "{}/api/v2/candidate/{}/status/?format=json".format(settings.SHINE_SITE, shine_id)
                status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if status_response.status_code == 200 and status_response.json():
                    return status_response.json()
            elif email:
                headers = self.get_api_headers()
                shine_id = self.get_shine_id(email=email, headers=headers)
                if shine_id:
                    status_url = settings.SHINE_SITE +\
                        "/api/v2/candidate/" +\
                        shine_id + "/status/?format=json"
                    status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    if status_response.status_code == 200 and status_response.json():
                        return status_response.json()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get status details %s'%str(e))
        return None

    def get_shine_candidate_resume(self, candidate_id=None, resume_id=None, data={}, headers=None):
        try:
            if candidate_id and resume_id:
                if not headers:
                    headers = self.get_api_headers()
                    headers.update({
                        "Accept": 'application/json',
                    })
                    api_url = settings.SHINE_SITE +\
                        '/api/v2/candidate/' +\
                        candidate_id + '/resumefiles/' +\
                        resume_id + '/'
                    response = requests.get(
                        api_url,
                        data=data, headers=headers)
                    if response.status_code == 200:
                        return response
        except Exception as e:
            logging.getLogger('error_log').error('unable to return candidate resume response  %s'%str(e))
        return None


class PriorityApplicantUpdate(ShineToken):

    def update_applicant_priority(self, candidate_id=None, data={}, headers=None):
        try:
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                    if data and headers:
                        headers.update({
                            "Content-Type": 'application/json',
                            "Accept": 'application/json',
                        })
                        api_url = settings.SHINE_SITE + '/api/v2/candidate/' +\
                            candidate_id + '/career-plus/detail/?format=json'
                        response = requests.patch(api_url, data=json.dumps(data), headers=headers)
                        if response.status_code == 200:
                            return True
        except Exception as e:
            logging.getLogger('error_log').error('unable to update profile details %s'%str(e))
        return False


class FeatureProfileUpdate(ShineToken):

    def update_feature_profile(self, candidate_id=None, data={}, headers=None):
        try:
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                    if data and headers:
                        headers.update({
                            "Content-Type": 'application/json',
                            "Accept": 'application/json',
                        })
                        api_url = settings.SHINE_SITE + '/api/v2/candidate/' +\
                            candidate_id + '/career-plus/detail/?format=json'
                        response = requests.patch(api_url, data=json.dumps(data), headers=headers)
                        if response.status_code == 200:
                            return True
        except Exception as e:
            logging.getLogger('error_log').error('unable to update profile details %s'%str(e))
        return False


class UploadResumeToShine(ShineToken):

    def sync_candidate_resume_to_shine(self, candidate_id=None, files={}, data={}, headers=None):
        try:
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                    if data and headers:
                        headers.update({
                            "Accept": 'application/json',
                        })
                        api_url = settings.SHINE_SITE +\
                            '/api/v2/candidate/' +\
                            candidate_id + '/resumefiles/'
                        response = requests.post(
                            api_url, files=files,
                            data=data, headers=headers)
                        if response.status_code in [200, 201]:
                            return True
        except Exception as e:
            logging.getLogger('error_log').error(
                "%s error in sync_candidate_resume_to_shine function" % (str(e)))
        return False


class AdServerShine(object):

    def encode(self, email, mobile, timestamp):
        inp_str = '{key}|{email}|{mobile}|{timestamp}'.format(**{'key': settings.MOBILE_ADSERVER_ENCODE_KEY, 'email': email, 'timestamp': timestamp, 'mobile': mobile})
        xor_cipher = XOR.new(settings.MOBILE_ADSERVER_ENCODE_KEY)
        return base64.urlsafe_b64encode(xor_cipher.encrypt(inp_str))

    def decode(self, encoded_str):
        if encoded_str:
            import urllib.parse
            token = urllib.parse.unquote(encoded_str)
            xor_cipher = XOR.new(settings.MOBILE_ADSERVER_ENCODE_KEY)
            inp_str = xor_cipher.decrypt(token).decode("utf-8")
            inp_list = inp_str.split('|') if "|" in inp_str else []
            # inp_list = inp_str.split('|')
            if inp_list and len(inp_list) == 4 and inp_list[0] == settings.MOBILE_ADSERVER_ENCODE_KEY:
                return inp_list
        return None


class AcrossShine(object):

    def encode(self, email):
        inp_str = '{email}|{key}'.format(**{'key': settings.ACROSS_ENCODE_KEY, 'email': email})
        xor_cipher = XOR.new(settings.ACROSS_ENCODE_KEY)
        return base64.urlsafe_b64encode(xor_cipher.encrypt(inp_str))

    def decode(self, encoded_str):
        if encoded_str:
            token = base64.urlsafe_b64decode(str(encoded_str))
            xor_cipher = XOR.new(settings.ACROSS_ENCODE_KEY)
            inp_str = xor_cipher.decrypt(token)
            inp_list = inp_str.split('|')
            if inp_list and len(inp_list) > 1 and inp_list[1] == settings.ACROSS_ENCODE_KEY:
                return inp_list[0]
        return None


class CrmApiMixin(object):

    def get_api_headers(self):
        try:
            headers = {
                "Authorization": 'Token ' + settings.SHINECPCRM_DICT.get('token'),
                "Content-Type": 'application/json',
                "Accept": 'application/json', }
            return headers
        except Exception as e:
            logging.getLogger('error_log').error('unable to return header %s'%str(e))
        return None

    def create_lead_by_api(self, data_dict={}):
        try:
            headers = self.get_api_headers()
            lead_create_api = settings.SHINECPCRM_DICT.get('base_url') + settings.SHINECPCRM_DICT.get('create_lead_url')

            client_data = data_dict
            resp = requests.post(lead_create_api, data=json.dumps(client_data), headers=headers)
            if resp.status_code == 201:
                return True
        except Exception as e:
            logging.getLogger('error_log').error('error in creating lead by api %s'%str(e))
        return None