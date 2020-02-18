import logging
import requests
from core.api_mixin import ShineToken
from core.api_mixin import ShineCandidateDetail as SCD
from django.conf import settings

#
# class ShineToken(object):
#     def get_client_token(self):
#         try:
#             client_access_url = settings.SHINE_SITE + '/api/v2/client/access/?format=json'
#             headers = {
#                 "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
#             client_data = {'key': settings.CLIENT_ACCESS_KEY, 'secret': settings.CLIENT_ACCESS_SECRET}
#             client_access_resp = requests.post(client_access_url, data=client_data, headers=headers)
#             client_access_resp_json = client_access_resp.json()
#             if client_access_resp.status_code == 201:
#                 return client_access_resp_json.get('access_token', None)
#         except Exception as e:
#             logging.getLogger('error_log').error(str(e))
#         return None
#
#     def get_access_token(self, email=None, password=None):
#         if email and password:
#             try:
#                 headers = {
#                     "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
#
#                 user_access_url = settings.SHINE_SITE + '/api/v2/user/access/?format=json'
#                 user_data = {"email": email, "password": password}
#                 user_access_resp = requests.post(user_access_url, data=user_data, headers=headers)
#                 user_access_resp_json = user_access_resp.json()
#                 if user_access_resp.status_code == 201:
#                     user_access_resp_json.update({'SUCCESS': True})
#                     return user_access_resp_json
#                 else:
#                     return user_access_resp_json
#             except Exception as e:
#                 logging.getLogger('error_log').error(str(e))
#         return None


# class ShineRequestHeader(object):
#     def get_request_header(self, user_access_token=None, client_token=None):
#         request_header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1'
#                           '; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19'
#                           ' (KHTML, like Gecko) Chrome/18.0.1025.166'
#                           ' Mobile Safari/535.19'}
#         try:
#             if user_access_token:
#                 request_header.update({'User-Access-Token': user_access_token})
#             if client_token:
#                 request_header.update({'Client-Access-Token': client_token})
#         except Exception as e:
#             logging.getLogger('error_log').error(str(e))
#
#         return request_header


class ShineCandidateDetail(SCD):

    # def get_api_headers(self, token: object = None) -> object:
    #     try:
    #         client_token = self.get_client_token()
    #         if client_token and not token:
    #             access_token_json = self.get_access_token(
    #                 email=settings.SHINE_API_USER,
    #                 password=settings.SHINE_API_USER_PWD)
    #             if access_token_json and\
    #                     access_token_json.get('SUCCESS', False):
    #                 access_token = access_token_json.get('access_token', None)
    #                 if access_token:
    #                     headers = {
    #                         "User-Access-Token": access_token,
    #                         "Client-Access-Token": client_token,
    #                         "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
    #                     }
    #                     return headers
    #         elif client_token and token:
    #             headers = {
    #                 "User-Access-Token": token,
    #                 "Client-Access-Token": client_token,
    #                 "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
    #             }
    #             return headers
    #     except Exception as e:
    #         logging.getLogger('error_log').error(str(e))
    #     return None

    def get_api_headers_non_auth(self):
        headers = {
            "Content-Type": 'application/json',
            "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) '
                          'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
        }
        return headers

    # def get_shine_id(self, email=None, headers=None):
    #     try:
    #         if not headers:
    #             headers = self.get_api_headers()
    #         if email and headers:
    #             shine_id_url = settings.SHINE_SITE +\
    #                 "/api/v2/candidate/career-plus/email-detail/?email=" +\
    #                 email + "&format=json"
    #             shine_id_response = requests.get(shine_id_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
    #             if shine_id_response and shine_id_response.status_code==200 and shine_id_response.json():
    #                 shine_id_json = shine_id_response.json()
    #                 if shine_id_json:
    #                     shine_id = shine_id_json[0].get("id", None)
    #                     return shine_id
    #     except Exception as e:
    #         logging.getLogger('error_log').error(str(e))
    #     return None

    # def get_candidate_detail(self, email=None, shine_id=None, token=None):
    #     try:
    #         if shine_id:
    #             headers = self.get_api_headers(token=token)
    #             detail_url = settings.SHINE_SITE +\
    #                     "/api/v2/candidate-profiles/" +\
    #                     shine_id + "/?format=json"
    #             detail_response = requests.get(detail_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
    #             if detail_response.status_code == 200 and detail_response.json():
    #                 return detail_response.json()
    #             logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
    #                 format(email,shine_id))
    #             return {}
    #
    #         elif email:
    #             headers = self.get_api_headers(token=token)
    #             shine_id = self.get_shine_id(email=email, headers=headers)
    #             if shine_id:
    #                 detail_url = settings.SHINE_SITE +\
    #                     "/api/v2/candidate-profiles/" +\
    #                     shine_id + "/?format=json"
    #                 detail_response = requests.get(detail_url, headers=headers)
    #                 if detail_response.status_code == 200 and detail_response.json():
    #                     return detail_response.json()
    #
    #                 logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
    #                 format(email,shine_id))
    #                 return {}
    #
    #             logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
    #                 format(email,shine_id))
    #             return {}
    #
    #         logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
    #                 format(email,shine_id))
    #         return {}
    #     except Exception as e:
    #         logging.getLogger('error_log').error(str(e))
    #
    #     logging.getLogger('error_log').error('unable to get candidate details {} {}'.\
    #                 format(email,shine_id))
    #     return {}

    # def get_status_detail(self, email=None, shine_id=None, token=None):
    #     try:
    #         if shine_id:
    #             headers = self.get_api_headers(token=token)
    #             status_url = "{}/api/v2/candidate/{}/status/?format=json".format(settings.SHINE_SITE, shine_id)
    #             status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
    #             try:
    #                 logging.getLogger('info_log').info(
    #                 'Response Received from shine for shine candidate status: {}'.format(status_response.__dict__))
    #             except Exception as e:
    #                 logging.getLogger('error_log').error(str(e))
    #             if status_response.status_code == 200 and status_response.json():
    #                 return status_response.json()
    #         elif email:
    #             headers = self.get_api_headers(token=None)
    #             shine_id = self.get_shine_id(email=email, headers=headers)
    #             if shine_id:
    #                 status_url = settings.SHINE_SITE +\
    #                     "/api/v2/candidate/" +\
    #                     shine_id + "/status/?format=json"
    #                 status_response = requests.get(status_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
    #                 try:
    #                     logging.getLogger('info_log').info(
    #                         'Response Received from shine for shine candidate status: {}'.format(
    #                             status_response.__dict__))
    #                 except Exception as e:
    #                     logging.getLogger('error_log').error(str(e))
    #                 if status_response.status_code == 200 and status_response.json():
    #                     return status_response.json()
    #     except Exception as e:
    #         logging.getLogger('error_log').error(str(e))
    #     return None

    def get_functional_area(self, email=None):
        try:
            functional_area = 0
            if email:
                shine_id = self.get_shine_id(email)
                headers = self.get_api_headers()
                if shine_id and headers:
                    detail_url = settings.SHINE_SITE +\
                        "/api/v2/candidate-profiles/" +\
                        shine_id + "/?format=json"
                    detail_response = requests.get(detail_url, headers=headers)
                    if detail_response and detail_response.status_code == 200 and detail_response.json():
                        detail_json = detail_response.json()
                        if detail_json and detail_json.get("jobs"):
                            jobs = detail_json.get("jobs")[0]
                            if jobs and jobs.get("sub_field"):
                                functional_area = jobs.get("sub_field")
                        if detail_json and detail_json.get("desired_job") and not functional_area:
                            desired_job = detail_json.get("desired_job")[0]
                            if desired_job and desired_job.get("functional_area"):
                                functional_area = desired_job.get("functional_area")[0]
            return functional_area
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None
