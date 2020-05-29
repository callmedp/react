import logging
import base64
import hmac
from hashlib import sha256

import requests
import json
from Crypto.Cipher import XOR

from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage


class ShineToken(object):
    def get_client_token(self):
        try:
            if cache.get('shine_client_access_token'):
                logging.getLogger('error_log').error('shine_client_access_token for 1177 %s'%str(cache.get('shine_client_access_token')))
                return cache.get('shine_client_access_token')
            headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) '
                                     'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
            client_access_url = settings.SHINE_SITE + '/api/v2/client/access/?format=json'
            client_data = {'key': settings.CLIENT_ACCESS_KEY, 'secret': settings.CLIENT_ACCESS_SECRET}
            client_access_resp = requests.post(client_access_url, data=client_data, headers=headers)
            client_access_resp_json = client_access_resp.json()
            if client_access_resp.status_code == 201:
                cache.set('shine_client_access_token', client_access_resp_json.get('access_token'), timeout=None)
                logging.getLogger('error_log').error('shine_client_access_token for 1177 %s'%str(cache.get('shine_client_access_token')))
                return client_access_resp_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error('error in getting client token%s'%str(e))
        return None

    def get_access_token(self):
        try:
            if cache.get('shine_user_access_token'):
                logging.getLogger('error_log').error('shine_user_access_token for 1177 %s'%str(cache.get('shine_user_access_token')))
                return cache.get('shine_user_access_token')
            headers = {
                "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) '
                              'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
            user_access_url = settings.SHINE_SITE + '/api/v2/user/access/?format=json'
            user_data = {"email": settings.SHINE_API_USER, "password": settings.SHINE_API_USER_PWD}
            user_access_resp = requests.post(user_access_url, data=user_data, headers=headers)
            user_access_resp_json = user_access_resp.json()
            if user_access_resp.status_code == 201:
                cache.set('shine_user_access_token', user_access_resp_json.get('access_token'), timeout=None)
                logging.getLogger('error_log').error('shine_user_access_token for 1177 %s'%str(cache.get('shine_user_access_token')))
                return user_access_resp_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error('error in accessing token %s' % str(e))
        return None

    def get_api_headers(self,token=None):
        try:
            client_token = self.get_client_token()
            if client_token:
                access_token = self.get_access_token()
                if access_token:
                    headers = {"User-Access-Token": access_token,
                               "Client-Access-Token": client_token,
                               "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) '
                                             'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 '
                                             'Mobile Safari/535.19'}
                    logging.getLogger('error_log').error('headers for 1177 %s'%str(headers))
                    return headers
        except Exception as e:
            logging.getLogger('error_log').error('error in getting header %s'%str(e))
        return None


class ShineCandidateDetail(ShineToken):

    def get_shine_id(self, email=None, headers=None):
        
        hit_candidate_api = False
        shine_id = None
        
        try:
            # try to get info from candidate solr 
            if email: 
                candidate_solr_url = settings.CANDIDATE_SOLR_URL
                solr_query = '?fl=id&wt=json&qt=edismax&rows=1&q=sEm:{}'.format(email)
                response = requests.get('{}{}'.format(candidate_solr_url, solr_query))
                logging.getLogger('error_log').error('solr query for 1177 %s'%str('{}{}'.format(candidate_solr_url, solr_query)))
                logging.getLogger('error_log').error('response for 1177 %s'%str(response.json()))
                if response.status_code == 200: 
                    response = response.json()
                    if not response and not isinstance(response, dict):
                        hit_candidate_api = True
                    response = response.get('response', {}).get('docs',[])
                    if not response or not isinstance(response, list):
                        hit_candidate_api = True

                    if not hit_candidate_api:
                        response = response[0]
                        shine_id = response.get('id', None)
                    if shine_id:
                        logging.getLogger('error_log').error('shine_id for 1177 %s'%str(shine_id))
                        return shine_id

            if not headers:
                headers = self.get_api_headers()
            if email and headers:
                shine_id_url = settings.SHINE_SITE +\
                    "/api/v2/candidate/career-plus/email-detail/?email=" +\
                    email + "&format=json"
                shine_id_response = requests.get(shine_id_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if shine_id_response.status_code == 401:
                    logging.getLogger('error_log').error('Token validity compromised, trying again')
                    cache.set('shine_client_access_token', None)
                    cache.set('shine_user_access_token', None)
                    headers = self.get_api_headers()
                    shine_id_response = requests.get(shine_id_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
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
                detail_url = settings.SHINE_SITE + "/api/v2/candidate-profiles/" + shine_id + "/?format=json"
                detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if detail_response.status_code == 401:
                    logging.getLogger('error_log').error('Token validity compromised, trying again')
                    cache.set('shine_client_access_token', None)
                    cache.set('shine_user_access_token', None)
                    headers = self.get_api_headers()
                    detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if detail_response.status_code == 200 and detail_response.json():
                    return detail_response.json()
                logging.getLogger('error_log').error('unable to get candidate details {} {}'.format(email, shine_id))
                return {}
            
            elif email:
                headers = self.get_api_headers()
                shine_id = self.get_shine_id(email=email, headers=headers)
                if shine_id:
                    detail_url = settings.SHINE_SITE + "/api/v2/candidate-profiles/" + shine_id + "/?format=json"
                    detail_response = requests.get(detail_url, headers=headers)
                    if detail_response.status_code == 401:
                        logging.getLogger('error_log').error('Token validity compromised, trying again')
                        cache.set('shine_client_access_token', None)
                        cache.set('shine_user_access_token', None)
                        headers = self.get_api_headers()
                        detail_response = requests.get(detail_url, headers=headers)
                    if detail_response.status_code == 200 and detail_response.json():
                        return detail_response.json()
                    
                    logging.getLogger('error_log').error('unable to get candidate details {} {}'.format(email,
                                                                                                        shine_id))
                    return {}
                
                logging.getLogger('error_log').error('unable to get candidate details {} {}'.format(email, shine_id))
                return {}

            logging.getLogger('error_log').error('unable to get candidate details {} {}'.format(email, shine_id))
            return {}
        except Exception as e:
            logging.getLogger('error_log').error('unable to get candidate details%s' % str(e))

        logging.getLogger('error_log').error('unable to get candidate details {} {}'.format(email, shine_id))
        return {}

    def get_candidate_public_detail(self, email=None, shine_id=None):

        headers = self.get_api_headers()
        
    
        if not shine_id and email:
            shine_id = self.get_shine_id(email=email, headers=headers)
        elif not email and not shine_id:
            logging.getLogger('error_log').error("Email ID or shine_id required for profile")
            return
        detail_url = settings.SHINE_SITE + "/api/v2/candidate-public-profiles/" + shine_id + "/?format=json"
        logging.getLogger('error_log').error('detail_url fpor 1177 {}'.format(detail_url))
        try:
            logging.getLogger('error_log').error('headers for 1177 {}'.format(headers))
            detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
            logging.getLogger('error_log').error('detail_response for 1177 {}'.format(detail_response.json()))
            if detail_response.status_code == 401:
                logging.getLogger('error_log').error('Token validity compromised, trying again')
                cache.set('shine_client_access_token', None)
                cache.set('shine_user_access_token', None)
                headers = self.get_api_headers()
                detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
            if detail_response.status_code == 200 and detail_response.json():
                return detail_response.json()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get detail response %s' % str(e))
        return

    def get_status_detail(self, email=None, shine_id=None, token=None):
        try:
            if shine_id:
                headers = self.get_api_headers()
                status_url = "{}/api/v2/candidate/{}/status/?format=json".format(settings.SHINE_SITE, shine_id)
                status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if status_response.status_code == 401:
                    logging.getLogger('error_log').error('Token validity compromised, trying again')
                    cache.set('shine_client_access_token', None)
                    cache.set('shine_user_access_token', None)
                    headers = self.get_api_headers()
                    status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if status_response.status_code == 200 and status_response.json():
                    return status_response.json()
            elif email:
                headers = self.get_api_headers()
                shine_id = self.get_shine_id(email=email, headers=headers)
                logging.getLogger('error_log').error('shine_id for 1177 %s'%str(shine_id))
                if shine_id:
                    status_url = settings.SHINE_SITE + "/api/v2/candidate/" + shine_id + "/status/?format=json"
                    status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    logging.getLogger('error_log').error('shine_id_response for 1177 %s'%str(status_response.json()))
                    if status_response.status_code == 401:
                        logging.getLogger('error_log').error('Token validity compromised for 1177, trying again')
                        cache.set('shine_client_access_token', None)
                        cache.set('shine_user_access_token', None)
                        headers = self.get_api_headers()
                        status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    if status_response.status_code == 200 and status_response.json():
                        logging.getLogger('error_log').error('shine_id_response for 1177 %s'%str(status_response.json()))
                        return status_response.json()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get status details for 1177%s'%str(e))
        return None

    def get_shine_candidate_resume(self, candidate_id=None, resume_id=None, data={}, headers=None):
        try:
            if candidate_id and resume_id:
                if not headers:
                    headers = self.get_api_headers()
                    headers.update({"Accept": 'application/json'})
                    api_url = settings.SHINE_SITE + '/api/v2/candidate/' + candidate_id + '/resumefiles/' + resume_id + '/'
                    response = requests.get(api_url, data=data, headers=headers)
                    if response.status_code == 401:
                        logging.getLogger('error_log').error('Token validity compromised, trying again')
                        cache.set('shine_client_access_token', None)
                        cache.set('shine_user_access_token', None)
                        headers = self.get_api_headers()
                        response = requests.get(api_url, data=data, headers=headers)
                    if response.status_code == 200:
                        return response
        except Exception as e:
            logging.getLogger('error_log').error('unable to return candidate resume response  %s' % str(e))
        return None
    
    def upload_resume_shine(self, data={}, file_path='', headers=None):
        file = None
        try:
            if not settings.IS_GCP:
                file = open(file_path, 'rb')
            else:
                file = GCPPrivateMediaStorage().open(file_path)
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
        files = {'resume_file': file}
        try:
            candidate_id = data.get('candidate_id', '')
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                    headers.update({"Accept": 'application/json'})
                    api_url = settings.SHINE_SITE + '/api/v2/candidate/' + candidate_id + '/resumefiles/'
                    response = requests.post(api_url, data=data, files=files, headers=headers)
                    if response.status_code == 401:
                        logging.getLogger('error_log').error('Token validity compromised, trying again')
                        cache.set('shine_client_access_token', None)
                        cache.set('shine_user_access_token', None)
                        headers = self.get_api_headers()
                        response = requests.post(api_url, data=data, files=files, headers=headers)
                    if status.is_success(response.status_code):
                        if not settings.IS_GCP:
                            file.close()
                        return True
        except Exception as e:
            logging.getLogger('error_log').error('unable to return candidate resume response  %s' % str(e))
        return None


class FeatureProfileUpdate(ShineToken):

    def update_feature_profile(self, candidate_id=None, data={}, headers=None):
        try:
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                    if data and headers:
                        headers.update({"Content-Type": 'application/json', "Accept": 'application/json'})
                        api_url = settings.SHINE_SITE + '/api/v2/candidate/' + candidate_id + '/career-plus/' \
                                                                                              'detail/?format=json'
                        response = requests.patch(api_url, data=json.dumps(data), headers=headers)
                        if response.status_code == 401:
                            logging.getLogger('error_log').error('Token validity compromised, trying again')
                            cache.set('shine_client_access_token', None)
                            cache.set('shine_user_access_token', None)
                            headers = self.get_api_headers()
                            response = requests.patch(api_url, data=json.dumps(data), headers=headers)
                        if response.status_code == 200:
                            return True
        except Exception as e:
            logging.getLogger('error_log').error('unable to update profile details %s'%str(e))
        return False


class ShineCertificateUpdate(ShineToken):

    def update_shine_certificate_data(self, candidate_id=None, data={}, headers=None):
        try:
            if candidate_id:
                if not headers:
                    headers = self.get_api_headers()
                if data and headers:
                    certificate_api_url = settings.SHINE_API_URL + "/candidate/" + candidate_id + "/certifications" \
                                                                                                  "/?format=json"
                    certification_response = requests.post(certificate_api_url, data=data, headers=headers)
                    if certification_response.status_code == 401:
                        logging.getLogger('error_log').error('Token validity compromised, trying again')
                        cache.set('shine_client_access_token', None)
                        cache.set('shine_user_access_token', None)
                        headers = self.get_api_headers()
                        certification_response = requests.post(certificate_api_url, data=data, headers=headers)
                    if certification_response.status_code == 201:
                        jsonrsp = certification_response.json()
                        logging.getLogger('info_log').info("api response:{}".format(jsonrsp))
                        return True, jsonrsp

                    elif certification_response.status_code != 201:
                        jsonrsp = certification_response.json()
                        logging.getLogger('error_log').error("api fail:{}".format(jsonrsp))
                        return False, jsonrsp
        except Exception as e:
            logging.getLogger('error_log').error('unable to update certificate %s'%str(e))
        return False, None


class ShineProfileDataUpdate(ShineToken):

    def update_shine_profile_data(self):
        headers = self.get_api_headers()
        headers.update({"Content-Type": 'application/json', "Accept": 'application/json'})
        api_url = settings.SHINE_SITE + '/api/v2/career-plus/profile_badge_cache_reset/'
        response = requests.post(api_url, headers=headers)
        if response.status_code == 401:
            logging.getLogger('error_log').error('Token validity compromised, trying again')
            cache.set('shine_client_access_token', None)
            cache.set('shine_user_access_token', None)
            headers = self.get_api_headers()
            response = requests.post(api_url, headers=headers)
        if response.status_code == 200:
            return True


class UploadResumeToShine(ShineToken):

    def sync_candidate_resume_to_shine(self, candidate_id=None, files={}, data={}, headers=None):
        if not candidate_id:
            return False

        if headers:
            return False

        headers = self.get_api_headers()
        if not data:
            return False
        if not headers:
            return False

        headers.update({"Accept": 'application/json'})
        api_url = settings.SHINE_SITE + '/api/v2/candidate/' + candidate_id + '/resumefiles/'
        try:
            response = requests.post(api_url, files=files, data=data, headers=headers)
            if response.status_code == 401:
                logging.getLogger('error_log').error('Token validity compromised, trying again')
                cache.set('shine_client_access_token', None)
                cache.set('shine_user_access_token', None)
                headers = self.get_api_headers()
                response = requests.post(api_url, files=files, data=data, headers=headers)
            if response.status_code in [200, 201]:
                return True
        except Exception as e:
            logging.getLogger('error_log').error("%s error in sync_candidate_resume_to_shine function" % (str(e)))
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


class AmcatApiMixin(object):

    def get_api_signature(self, token, secret, data, api_url, method_type):
        data = dict(sorted(data.items()))
        msg = 'POST' + '|' + api_url + "\n"

        for key, value in data.items():
            msg += key + value

        msg = (msg + token).strip()

        # $signature = base64_encode(hash_hmac(‘sha256’, $longStr, $secret, false));
        msg = msg.encode()
        secret = secret.encode()
        digest = hmac.new(secret, msg=msg, digestmod=sha256).hexdigest()

        signature = base64.b64encode(digest.encode())

        return signature

    def get_headers(self, data, api_url, method_type):
        token = settings.AMCAT_API_TOKEN
        secret = settings.AMCAT_API_SECRET
        api_signature = self.get_api_signature(token, secret, data, api_url, method_type)
        headers = {
            'X-Api-AuthToken': token,
            'X-Api-Signature': api_signature,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return headers

    def get_all_certiticate_data(self, data):
        api_url = settings.VENDOR_URLS['amcat']['all_certificates']
        headers = self.get_headers(data, api_url, 'POST')
        response = requests.post(api_url, data=data, headers=headers)
        if response.status_code == 200:
            jsonrsp = response.json()
            jsonrsp = jsonrsp['data']
            logging.getLogger('info_log').info(
                "amcat import certificate for email {} api response:{}".format(str(data), jsonrsp)
            )
            return True, jsonrsp
        else:
            jsonrsp = response.json()
            logging.getLogger('info_log').info(
                "amcat  import certificate for email {} api response:{}".format(str(data), jsonrsp)
            )
            return False, response.json()

    def get_auto_login_url(self, data):
        api_url = settings.VENDOR_URLS['amcat']['get_autologin_url']
        headers = self.get_headers(data, api_url, 'POST')
        resp = requests.post(api_url, data=data, headers=headers)
        if resp.status_code == 200:
            resp = resp.json()
            autologin_url = resp['data']['autoLoginUrl']
            logging.getLogger('info_log').info(
                "AutoLogin url for data %s successfully retrieved" % (str(data))
            )
            return autologin_url
        else:
            logging.getLogger('error_log').error(
                "Failed fetching autologin for data:- %s , Error:- %s" % (str(data), str(resp.content))
            )
            return False


        return None


class NeoApiMixin(object):

    def get_headers(self):
        data = {
            'username': settings.NEO_USERNAME,
            'password': settings.NEO_PASSWORD,
        }
        url_to_hit = settings.NEO_URL['jwt_token']

        resp = requests.post(url_to_hit, json=data)
        if resp.status_code == 200:
            json_rep = resp.json()
            token = json_rep.get('token', None)
            if token:
                return {'x-DynEd-Tkn': token}

    def get_user_neo_id(self, email):
        url_to_hit = settings.NEO_URL['user_detail']
        url_to_hit += 'email=' + email
        headers = self.get_headers()
        resp = requests.get(url_to_hit, headers=headers)
        if resp.status_code == 200:
            json_rep = resp.json()
            if 'data' in json_rep and json_rep['data']:
                user_id = json_rep['data'][0]['id']
                return user_id

    def board_user_on_neo(self, email, data_dict):
        user_id = self.get_user_neo_id(email)
        headers = self.get_headers()
        if user_id:
            data_dict['user_id'] = user_id
            url_to_hit = settings.NEO_URL['board_user']
            resp = requests.post(url_to_hit, data=data_dict, headers=headers)
            if resp.status_code == 200:
                return True
            else:
                logging.getLogger('error_log').error('Unable to board user because {}'.format(resp.content))
        else:
            logging.getLogger('error_log').error('Unable to board user {} as user id not found'.format(email))


    def update_student_sso_profile(self, data, email):
        '''
            account_type -> trial/regular
            account_active -> true/false
            account_start_date -> yyyy-mm-dd hh:mm:ss
            account_expired_date -> yyyy-mm-dd hh:mm:ss
            dsa_access -> true/false
            live_access -> true/false
        '''
        url_to_hit = settings.NEO_URL['update-sso-profile']
        url_to_hit = url_to_hit.format(email)
        headers = self.get_headers()
        resp = requests.post(url_to_hit, data=data, headers=headers)
        if resp.status_code == 200:
            json_rep = resp.json()
            return True


    def get_pt_result(self, email):
        ''' Return placement test result for provided email'''
        data = {
            'token': settings.NEO_TOKEN,
            'email': email
        }
        url_to_hit = settings.NEO_URL['pt_result']
        resp = requests.post(url_to_hit, data=data)
        if resp.status_code == 200:
            json_rep = resp.json()
            data = {'status': 200, 'data': json_rep}
            return data
        if resp.status_code == 400:
            return {'status': 400}

    def get_student_status_on_neo(self, email):
        '''
          Return status of provided email on Neo site.
          Values can be - Not Boarded / Pending / Boarded
        '''
        url_to_hit = settings.NEO_URL['user_detail']
        url_to_hit += 'email=' + email
        headers = self.get_headers()
        resp = requests.get(url_to_hit, headers=headers)
        if resp.status_code == 200:
            json_rep = resp.json()
            if 'data' in json_rep and json_rep['data']:
                status = json_rep['data'][0]['status']
                return status

    def get_student_account_type(self, email):
        student_sso = self.get_student_sso_profile(email)
        if student_sso:
            account_type = student_sso.get('acl', {}).get('account', {}).get('type','')
            if not account_type:
                return
            return account_type

    def get_student_sso_profile(self, email):
        url_to_hit = settings.NEO_URL['get-sso-profile']
        url_to_hit = url_to_hit.format(settings.NEO_USERNAME, email)
        headers = self.get_headers()
        resp = requests.get(url_to_hit, headers=headers)
        if resp.status_code == 200:
            json_rep = resp.json()
            return json_rep
