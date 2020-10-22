from __future__ import absolute_import
import json
import re
import logging
import hmac
import hashlib
import urllib
import requests
from django.core.cache import cache
from datetime import datetime, timedelta
from collections import OrderedDict
from itertools import islice
import ast

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

from cart.models import Subscription
from .tasks import post_roundone_order


class RoundOneAPI(object):

    def create_roundone_order(self, order):
        try:
            user = order.candidate_id
            post_roundone_order.delay({'user': user, 'order_id': order.id})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def get_roundone_access_token(self, email, request):
        try:
            if request:
                access_token = request.session.get('roundone_access_token', '')
                token_expiry = request.session.get('roundone_token_expiry')
                if access_token and token_expiry and datetime.now() < datetime.strptime(json.loads(token_expiry), "%Y-%m-%dT%H:%M:%S.%f"):
                    return access_token
            try:
                roundone_order = Subscription.objects.get(
                    candidateid=request.session['candidate_id']
                )
                password = ast.literal_eval(roundone_order.remark)
                password = password['pass']
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                password = settings.ROUNDONE_DEFAULT_PASSWORD
            post_url = settings.ROUNDONE_API_DICT.get("oauth_url")
            
            post_data = {
                "client_id": settings.ROUNDONE_API_DICT.get("client_id", ''),
                "client_secret": settings.ROUNDONE_API_DICT.get(
                    "client_secret", ''),
                "affiliateName": settings.ROUNDONE_API_DICT.get(
                    "affiliateName", 'CP'),
                "username": email,
                "password": password.candidateid if hasattr(password, 'candidateid') else password,
            }

            headers = {'content-type': 'application/json'}
            response = requests.post(
                post_url, data=json.dumps(post_data),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)

            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                access_token = response_json.get('access_token', '')
                expires_in = response_json.get('expires_in', 172800)
                if request and access_token:
                    request.session.update({
                        'roundone_access_token': access_token,
                        'roundone_token_expiry': json.dumps(
                            datetime.now() + timedelta(
                                seconds=expires_in), cls=DjangoJSONEncoder)})
                return access_token
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_location_list(self, **kwargs):
        try:
            location_json = cache.get('roundone_location')

            if location_json:
                return json.loads(location_json)

            url = settings.ROUNDONE_API_DICT.get("location_url")
            response = requests.get(url, timeout=settings.ROUNDONE_API_TIMEOUT)

            if response.status_code == 200:
                location_list = response.json()
                location_json = json.dumps({
                    "location_list": location_list[1: -1]})
                cache.set('roundone_location', location_json, 60 * 60)
                return json.loads(location_json)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return {}

    def get_search_response(self, request, **kwargs):
        response_json = {"response": False}
        try:
            page = 0
            start = 0
            sort_by = 0
            rows = 10
            userEmail = self.get_user_ip(request)
            post_url = settings.ROUNDONE_API_DICT.get("job_search_url")

            try:
                sort_by = int(request.GET.get('sort', 0))
                if not sort_by in [0, 1]:
                    sort_by = 0
            except Exception as e:
                logging.getLogger('error_log').error('unable to do sort by:-%s'%str(e))
                pass

            try:
                page = int(request.GET.get('page', 0))
                if page < 0:
                    page = 0
                start = rows * page
            except Exception as e:
                logging.getLogger('error_log').error('unable to get page%s'%str(e))
                page = 0

            post_data = {
                "userEmail": userEmail,
                "start": start,
                "rows": rows,
                "sort": sort_by,
                "affiliateName": settings.ROUNDONE_API_DICT.get(
                    "affiliateName", 'CP')
            }

            location = request.GET.get('loc', '')
            keyword = kwargs.get('keyword', '')
            company_list = request.GET.get('company', '').split(',')

            location = location if location else kwargs.get('location', '')

            if location and location != "all":
                post_data.update({"location": location.split(",")})

            if keyword and keyword != "all":
                searchKeyword = keyword.replace("-", " ")[:45]
                post_data.update({"searchKeyword": searchKeyword})

            if company_list and company_list[0]:
                post_data.update({'companyId': company_list})

            headers = {'content-type': 'application/json'}
            response = requests.post(
                post_url, data=json.dumps(post_data),
                headers=headers, timeout=settings.ROUNDONE_API_TIMEOUT,
            )

            if response.status_code == 200:
                response_json = response.json()
                response_json.update({
                    'response': True,
                    'company_list': company_list})
                sortedCompany = request.session.get('sortedCompany', {})
                companyJobCount = response_json.get('companyJobCount', {})

                if companyJobCount:
                    company_dict = OrderedDict(sorted(companyJobCount.items(), key=lambda k: k[1]['jobCount'], reverse=False))
                    sliced_company_dict = islice(company_dict.items(), 10)
                    sortedCompany = OrderedDict(sliced_company_dict)
                    request.session['sortedCompany'] = sortedCompany
                response_json.update({'sortedCompany': sortedCompany})

                if sort_by:
                    response_json.update({'sort': True})
                if page:
                    response_json.update({'page': page})
                if len(response_json.get('data', [])) < rows:
                    response_json.update({'last_page': True})

        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % (str(response_json.json()), str(e)))
        return response_json

    def get_job_detail(self, request, **kwargs):
        response_json = {"response": False, "msg": "Error Fetching Detail."}
        try:
            userEmail = self.get_user_ip(request)
            url = settings.ROUNDONE_API_DICT.get("job_detail_url")
            api_secret_key = settings.ROUNDONE_API_DICT.get("jobdetail_secret_key")
            job_params = kwargs.get('job_params').split('-')

            data_dict = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
            }

            data_str = '&'.join('{}={}'.format(key, value) for key, value in data_dict.items())
            hmac_value = hmac.new(bytearray(api_secret_key.encode('utf-8')), data_str.encode('utf-8'), hashlib.sha1).hexdigest()
            data_dict.update({"hash": hmac_value})
            response = requests.get(url, params=data_dict, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('status') == "1":
                    response_json.update({'response': True, 'jobId': job_params[0]})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def post_referral_request(self, request, job_params):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("referral_request_url")
            data = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(
                url,
                data=json.dumps(data),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_roundone_profile(self, request):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("get_profile_url")
            access_token = self.get_roundone_access_token(userEmail, request)
            params = {
                "userEmail": userEmail,
                "access_token": access_token
            }

            response = requests.get(
                url, params=params,
                timeout=settings.ROUNDONE_API_TIMEOUT)

            if response.status_code == 200:
                response_json = response.json()
                response_json.update({'response': True, "access_token": access_token})

        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def post_roundone_profile(self, request, roundone_profile):
        response_json = {"response": False}
        try:
            if roundone_profile.get("user"):
                applicantProfile = {"user": roundone_profile.get("user")}
                userEmail = request.session.get('email', '')
                url = settings.ROUNDONE_API_DICT.get("post_profile_url")
                data = {
                    "userEmail": userEmail,
                    "access_token": self.get_roundone_access_token(userEmail, request),
                    "applicantProfile": applicantProfile
                }
                headers = {'content-type': 'application/json'}
                response = requests.put(
                    url, data=json.dumps(data),
                    headers=headers,
                    timeout=settings.ROUNDONE_API_TIMEOUT)
                if response and response.status_code == 200 and response.json():
                    response_json = response.json()
                    response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_referral_status(self, request=None):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("referral_status_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_referral_confirm(self, request):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            requestId = request.GET.get('requestId')
            url = settings.ROUNDONE_API_DICT.get("referral_confirm_url")
            put_data = {
                "userEmail": userEmail,
                "requestId": requestId,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.put(
                url, data=json.dumps(put_data),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_upcoming_status(self, request=None):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("upcoming_interaction_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_past_interaction(self, request=None):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("past_interaction_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_saved_history(self, request=None):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("saved_history_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def delete_saved_job(self, request, job_params):
        response_json = {"response": False}
        try:
            userEmail = request.session.get('email', '')
            url = settings.ROUNDONE_API_DICT.get("delete_job_url")
            data_dict = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.put(
                url, data=json.dumps(data_dict),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def is_premium_user(self, request=None):
        try:
            url = settings.ROUNDONE_API_DICT.get("is_premium_url")
            if 'candidate_id' in request.session:
                userEmail = request.session.get('email', '')
            else:
                return False
            access_token = self.get_roundone_access_token(userEmail, request)
            if access_token:
                params = {
                    "userEmail": userEmail,
                    "access_token": access_token
                }
                response = requests.get(
                    url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
                if response and response.status_code == 200 and\
                   response.json():
                    response_json = response.json()

                    if response_json and response_json.get("status") == "1":
                        return True
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return False

    def save_job(self, request=None, **kwargs):
        response_json = {'response': False}
        try:
            url = settings.ROUNDONE_API_DICT.get("save_job_url")
            job_params = kwargs.get('job_params').split('-')
            userEmail = request.session.get('email')

            post_data = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "access_token": self.get_roundone_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(
                url,
                data=json.dumps(post_data),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)

            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def feedback_submit(self, request, data_dict):
        response_json = {'response': False}
        try:
            url = settings.ROUNDONE_API_DICT.get("feedback_submit_url")
            userEmail = data_dict.get('userEmail')
            orderId = data_dict.get('orderId')
            feedback_dict = {
                'interviewerRating': data_dict.get('interviewerRating'),
                'roundoneRating': data_dict.get('roundoneRating'),
                'comments': data_dict.get('comments')
            }
            feedback_str = '&'.join('{}={}'.format(key, value) for key, value in feedback_dict.items())
            feedbackData = urllib.quote_plus(feedback_str)
            put_data = {
                'userEmail': userEmail,
                'orderId': orderId,
                'feedbackData': feedbackData,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                'access_token': self.get_roundone_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.put(
                url, data=json.dumps(put_data),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def interaction_result(self, request, data_dict):
        response_json = {'response': False}
        try:
            url = settings.ROUNDONE_API_DICT.get("interaction_result_url")
            userEmail = data_dict.get('userEmail')
            orderId = data_dict.get('orderId')
            params = {
                'userEmail': userEmail,
                'orderId': orderId,
                'access_token': self.get_roundone_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_user_ip(self, request):
        user_ip = request.session['email'] if 'email' in request.session else settings.ROUNDONE_DEFAULT_CP_EMAIL
        http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        try:
            if http_x_forwarded_for:
                user_ip = http_x_forwarded_for.split(',')[0]
            else:
                user_ip = request.META.get('REMOTE_ADDR')
        except Exception as e:
            logging.getLogger('error_log').error('unable to get user_ip%s' % str(e))
            pass
        return user_ip

    def remove_html_tags(self, json_dict):
        for json_rsp in json_dict.get('data'):
            jd = json_rsp.get('jobDescription')
            clean = re.compile('<.*?>')
            text = re.sub(clean, '', jd)
            json_rsp.update({'jobDescription': text.replace("\n\n\n", "")})
        return json_dict

    def roundone_message(self, response_json):
        rsp = response_json.get('msg')
        if isinstance(rsp, dict):
            keys = list(rsp.keys())[0]
            msg = rsp[keys][0]
            return msg
        elif isinstance(rsp, str):
            return rsp



class RoundOneSEO(object):

    def get_seo_title(self, title_for, **context):
        try:
            if title_for == "home":
                return "Round One : Job Referrals from Top Companies"
            elif title_for == "listing":
                return "{clean_keyword} Jobs in {clean_location} - {clean_keyword} Jobs".format(**context)
            elif title_for == "detail":
                return "{jobTitle} - learning1.shine.com".format(**context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return "Shine - CV | Resume Format | Curriculum Vitae | Cover Letter | Resume Samples"

    def get_seo_desc(self, desc_for, **context):
        try:
            if desc_for == "home":
                return "Get a Chance to Earn Job Referrals from Top Companies insiders and Get Hired - Higher Your Chances to get Job, Find Jobs in Top 500 Companies"
            elif desc_for == "listing":
                return "Find List of Jobs available in {clean_keyword} - {clean_keyword} Jobs from Top Companies, Explore {clean_keyword} Jobs for Freshers & Experienced, Find New {clean_keyword} Jobs Online".format(**context)
            elif desc_for == "detail":
                return "Apply to {jobTitle} Jobs Online on learning1.shine.com".format(**context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return ""

    def get_seo_heading(self, heading_for, **context):
        try:
            if heading_for == "home":
                return "Job Referrals"
            elif heading_for == "listing":
                return "{clean_keyword} Jobs".format(**context)
            elif heading_for == "detail":
                return "{jobTitle}".format(**context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return ""

    def get_seo_data(self, data_for, **context):
        seo_title = self.get_seo_title(title_for=data_for, **context)
        seo_desc = self.get_seo_desc(desc_for=data_for, **context)
        seo_heading = self.get_seo_heading(heading_for=data_for, **context)
        return {
            'seo_title': seo_title, 'seo_desc': seo_desc,
            'seo_heading': seo_heading
        }
