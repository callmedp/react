import logging
import requests
from django.conf import settings


class CpAccessToken(object):
    def get_access_token(self):
        try:
            client_access_url = settings.CP_SITE + '/oauth2/access_token/'
            client_data = {
                'client_id': settings.CP_CLIENT_ID,
                'client_secret': settings.CP_CLIENT_SECRET,
                'username': settings.CP_API_USER,
                'password': settings.CP_API_USER_PASSWORD,
                'grant_type': settings.CP_GRANT_TYPE
            }
            client_access = requests.post(client_access_url, data=client_data)
            client_access_json = client_access.json()
            if client_access.status_code == 200:
                return client_access_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        return None

    def get_request_header(self, access_token=None):
        request_header = {}
        try:
            if access_token:
                request_header.update({'Authorization': 'Bearer ' + access_token})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        return request_header


class CpOrderHistory(CpAccessToken):
    
    def get_order_history(self, email=None):
        try:
            if email:
                access_token = self.get_access_token()
                if access_token:
                    headers = self.get_request_header(access_token=access_token)
                    order_url = settings.CP_SITE + '/crm-api/history/?email=' + email
                    order_response = requests.get(order_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    if order_response.status_code == 200:
                        return order_response.json()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_payment_history(self, txn_id=None, crm_lead_id=None):
        try:
            if txn_id or crm_lead_id:
                access_token = self.get_access_token()
                if access_token:
                    headers = self.get_request_header(access_token=access_token)
                    if txn_id:
                        payment_url = settings.CP_SITE + '/crm-api/?txn_id=' + txn_id
                        order_response = requests.get(payment_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    elif crm_lead_id:
                        payment_url = settings.CP_SITE + '/crm-api/?lead_id=' + crm_lead_id
                        order_response = requests.get(payment_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    if order_response.status_code == 200:
                        return order_response.json()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def payment_confirm(self, order_id=None, sales_id=None, crm_txn=''):
        try:
            if order_id and sales_id:
                access_token = self.get_access_token()
                if access_token:
                    headers = self.get_request_header(access_token=access_token)
                    payment_url = settings.CP_SITE + '/crm-api/'+ order_id+'/edit/'
                    data = {
                        'crm_sales_id':sales_id,
                        'crm_txn': crm_txn,
                        'sale_claimed':True
                    }
                    edit_response = requests.put(payment_url,data=data, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                    if edit_response.status_code == 200:
                        return True
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return False


class PaymentAccessToken(object):
    def get_access_token(self):
        try:
            client_access_url = settings.PAYMENT_SITE + '/o/token/'
            client_data = {
                'client_id': settings.PAYMENT_CLIENT_ID,
                'client_secret': settings.PAYMENT_CLIENT_SECRET,
                'username': settings.PAYMENT_API_USER,
                'password': settings.PAYMENT_USER_PASSWORD,
                'grant_type': settings.PAYMENT_GRANT_TYPE
            }
            client_access = requests.post(client_access_url, data=client_data)
            client_access_json = client_access.json()
            if client_access.status_code == 200:
                return client_access_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        return None

    def get_request_header(self, access_token=None):
        request_header = {}
        try:
            if access_token:
                request_header.update({'Authorization': 'Bearer ' + access_token})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        return request_header


class PaymentShine(PaymentAccessToken):
    
    def payment_link(self, data=None):
        try:
            if data:
                access_token = self.get_access_token()
                if access_token:
                    headers = self.get_request_header(access_token=access_token)
                    payment_url = settings.PAYMENT_SITE + '/api/get-payment-link/'
                    link_response = requests.post(payment_url, data=data, headers=headers, timeout=10)
                    if link_response.status_code == 200 and link_response.json():
                        return link_response.json()
                    else:
                        logging.getLogger('error_log').error(str(link_response))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def expire_payment_link(self, data=None):
        try:
            if data:
                access_token = self.get_access_token()
                if access_token:
                    headers = self.get_request_header(access_token=access_token)
                    payment_url = settings.PAYMENT_SITE + '/api/expire-payment-link/'
                    link_response = requests.post(payment_url, data=data, headers=headers, timeout=10)
                    if link_response.status_code == 200 and link_response.json():
                        return link_response.json()
                    else:
                        logging.getLogger('error_log').error(str(link_response))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

class ShineToken(object):
    def get_client_token(self):
        try:
            client_access_url = settings.SHINE_SITE + '/api/v2/client/access/?format=json'
            client_data = {'key': settings.CLIENT_ACCESS_KEY, 'secret': settings.CLIENT_ACCESS_SECRET}
            client_access_resp = requests.post(client_access_url, data=client_data)
            client_access_resp_json = client_access_resp.json()
            if client_access_resp.status_code == 201:
                return client_access_resp_json.get('access_token', None)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_access_token(self, email=None, password=None):
        if email and password:
            try:
                user_access_url = settings.SHINE_SITE + '/api/v2/user/access/?format=json'
                user_data = {"email": email, "password": password}
                user_access_resp = requests.post(user_access_url, data=user_data)
                user_access_resp_json = user_access_resp.json()
                if user_access_resp.status_code == 201:
                    user_access_resp_json.update({'SUCCESS': True})
                    return user_access_resp_json
                else:
                    return user_access_resp_json
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        return None


class ShineRequestHeader(object):
    def get_request_header(self, user_access_token=None, client_token=None):
        request_header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1'
                          '; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19'
                          ' (KHTML, like Gecko) Chrome/18.0.1025.166'
                          ' Mobile Safari/535.19'}
        try:
            if user_access_token:
                request_header.update({'User-Access-Token': user_access_token})
            if client_token:
                request_header.update({'Client-Access-Token': client_token})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        return request_header


class ShineCandidateDetail(ShineToken):

    def get_api_headers(self):
        try:
            client_token = self.get_client_token()
            if client_token:
                access_token_json = self.get_access_token(
                    email=settings.SHINE_API_USER,
                    password=settings.SHINE_API_USER_PWD)
                if access_token_json and\
                        access_token_json.get('SUCCESS', False):
                    access_token = access_token_json.get('access_token', None)
                    if access_token:
                        headers = {"User-Access-Token": access_token,
                                   "Client-Access-Token": client_token,
                                   "User-Agent": 'Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
                        return headers
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_shine_id(self, email=None, headers=None):
        try:
            if not headers:
                headers = self.get_api_headers()
            if email and headers:
                shine_id_url = settings.SHINE_SITE +\
                    "/api/v2/candidate/career-plus/email-detail/?email=" +\
                    email + "&format=json"
                shine_id_response = requests.get(shine_id_url, headers=headers, timeout=settings.SHINE_API_TIMEOUT)
                if shine_id_response and shine_id_response.status_code==200 and shine_id_response.json():
                    shine_id_json = shine_id_response.json()
                    if shine_id_json:
                        shine_id = shine_id_json[0].get("id", None)
                        return shine_id
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
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
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_status_detail(self, email=None, shine_id=None):
        try:
            if shine_id:
                headers = self.get_api_headers()
                status_url = settings.SHINE_SITE +\
                        "/api/v2/candidate/" +\
                        shine_id + "/status/?format=json"
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
            logging.getLogger('error_log').error(str(e))
        return None

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


