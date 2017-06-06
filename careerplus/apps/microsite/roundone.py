from __future__ import absolute_import
import json
import hmac
import base64
import urllib
import hashlib
import logging
import requests
from collections import OrderedDict
from datetime import datetime, timedelta
from itertools import islice

from Crypto.Cipher import XOR

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.template.loader import render_to_string

from .mixins import CommonMethodMixin
from .tasks import post_roundone_order


class RoundOnePassword(object):

    def encode(self, email):
        inp_str = '{email}|{salt}'.format(
            email=email, salt=settings.ROUNDONE_ENCODING_SALT)
        xor_cipher = XOR.new(settings.ROUNDONE_ENCODING_KEY)
        return base64.urlsafe_b64encode(xor_cipher.encrypt(inp_str))

    def decode(self, encoded_str):
        if encoded_str:
            token = base64.urlsafe_b64decode(str(encoded_str))
            xor_cipher = XOR.new(settings.ROUNDONE_ENCODING_KEY)
            inp_str = xor_cipher.decrypt(token)
            inp_list = inp_str.split('|')
            if inp_list and len(inp_list) > 0 and settings.ROUNDONE_ENCODING_SALT in inp_list:
                email = inp_list[0]
                return email if email else None
        return None


class RoundOneAPI(CommonMethodMixin):

    def create_roundone_order(self, order):
        try:
            user = order.candidate
            password = user.pk
            post_roundone_order.delay({
                'user': user,
                'password': password,
                'order': order})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

    def get_access_token(self, email, request=None):
        try:
            if request:
                access_token = request.session.get('roundone_access_token', '')
                token_expiry = request.session.get('roundone_token_expiry')
                if access_token and token_expiry and datetime.now() < token_expiry:
                    return access_token
            try:
                password = User.objects.get(email=email).pk
            except:
                password = settings.ROUNDONE_DEFAULT_PASSWORD

            post_url = settings.ROUNDONE_API_DICT.get("oauth_url")

            post_data = {
                "client_id": settings.ROUNDONE_API_DICT.get("client_id", ''),
                "client_secret": settings.ROUNDONE_API_DICT.get(
                    "client_secret", ''),
                "affiliateName": settings.ROUNDONE_API_DICT.get(
                    "affiliateName", 'CP'),
                "username": email,
                "password": password
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
                        'roundone_token_expiry': datetime.now() +
                        timedelta(seconds=expires_in)})
                return access_token
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return None

    def get_location_list(self, **kwargs):
        try:
            location_json = settings.REDIS_CON.get('roundone_location')

            if location_json:
                return json.loads(location_json)

            url = settings.ROUNDONE_API_DICT.get("location_url")
            response = requests.get(url, timeout=settings.ROUNDONE_API_TIMEOUT)

            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                location_list = response_json[1: -1]
                location_json = json.dumps({"location_list": location_list})
                settings.REDIS_CON.setex(
                    'roundone_location', 3600, location_json)
                return json.loads(location_json)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return {}

    def get_search_response(self, request=None, **kwargs):
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
            except:
                pass
            try:
                page = int(request.GET.get('page', 0))
                if page < 0:
                    page = 0
                start = rows*page
            except:
                page = 0
            post_data = {
                "userEmail": userEmail,
                "start": start,
                "rows": rows,
                "sort": sort_by,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP')
            }
            
            location = request.GET.get('loc', '')
            if location and location != "all":
                post_data.update({"location": location.split(",")})
            if not location:
                location = kwargs.get('location', '')
                if location and location != "all":
                    post_data.update({"location": location.split("-")})

            keyword = kwargs.get('keyword', '')
            if keyword and keyword != "all":
                searchKeyword = keyword.replace("-", " ")[:45]
                post_data.update({"searchKeyword": searchKeyword})

            company_list = request.GET.get('company', '').split(',')
            if company_list and company_list[0]:
                post_data.update({'companyId': company_list})
            
            headers = {'content-type': 'application/json'}
            response = requests.post(post_url,
                                     data=json.dumps(post_data),
                                     headers=headers,
                                     timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                if response_json.get('status') and response_json.get('status') ==  "1":
                    response_json.update({'response': True, 'company_list': company_list})
                    # save_key = keyword + "-jobs-in-" + location
                    sortedCompany = request.session.get('sortedCompany', {})
                    # if save_key not in request.path or not sortedCompany:
                    companyJobCount = response_json.get('companyJobCount', {})
                    if companyJobCount:
                        company_dict = OrderedDict(sorted(companyJobCount.items(), key=lambda k: k[1]['jobCount'], reverse=True))
                        sliced_company_dict = islice(company_dict.iteritems(), 10)
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
            logging.getLogger('error_log').error(str(e))
        return response_json

    def get_job_detail(self, request=None, **kwargs):
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
                "userEmail": userEmail
            }
            data_str = '&'.join('{}={}'.format(key, value) for key, value in data_dict.items())
            hmac_value = hmac.new(api_secret_key, data_str, hashlib.sha1).hexdigest()
            data_dict.update({"hash": hmac_value})
            response = requests.get(url, params=data_dict, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                if response_json.get('status') and response_json.get('status') == "1":
                    response_json.update({'response': True, 'jobId': job_params[0]})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def post_referral_request(self, request, job_params):
        response_json = {"response": False}
        try:
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("referral_request_url")
            data = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("get_profile_url")
            access_token = self.get_access_token(userEmail, request)
            params = {
                "userEmail": userEmail,
                "access_token": access_token
            }
            response = requests.get(
                url, params=params,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
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
                userEmail = request.user.email
                url = settings.ROUNDONE_API_DICT.get("post_profile_url")
                data = {
                    "userEmail": userEmail,
                    "access_token": self.get_access_token(userEmail, request),
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("referral_status_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            requestId = request.GET.get('requestId')
            url = settings.ROUNDONE_API_DICT.get("referral_confirm_url")
            put_data = {
                "userEmail": userEmail,
                "requestId": requestId,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("upcoming_interaction_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("past_interaction_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("saved_history_url")
            params = {
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
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
            userEmail = request.user.email
            url = settings.ROUNDONE_API_DICT.get("delete_job_url")
            data_dict = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP'),
                "access_token": self.get_access_token(userEmail, request)
            }
            headers = {'content-type': 'application/json'}
            response = requests.put(
                url, data=json.dumps(data_dict),
                headers=headers,
                timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json

    def is_premium_user(self, request=None):
        try:
            url = settings.ROUNDONE_API_DICT.get("is_premium_url")

            if request.user.is_authenticated():
                userEmail = request.user.email
            else:
                return False

            access_token = self.get_access_token(userEmail, request)

            if len(access_token) > 0:
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
            userEmail = request.user.email

            post_data = {
                "jobId": job_params[0],
                "jobType": job_params[1],
                "refId": job_params[2],
                "userEmail": userEmail,
                "access_token": self.get_access_token(userEmail, request)
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
                'access_token': self.get_access_token(userEmail, request)
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
                'access_token': self.get_access_token(userEmail, request)
            }
            response = requests.get(url, params=params, timeout=settings.ROUNDONE_API_TIMEOUT)
            if response and response.status_code == 200 and response.json():
                response_json = response.json()
                response_json.update({'response': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return response_json



class RoundOneSEO(object):

    def get_seo_title(self, title_for, **context):
        try:
            if title_for == "home":
                return "Round One : Job Referrals from Top Companies"
            elif title_for == "listing":
                return "{clean_keyword} Jobs in {clean_location} - {clean_keyword} Jobs".format(**context)
            elif title_for == "detail":
                return "{jobTitle} - Careerplus.shine.com".format(**context)
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
                return "Apply to {jobTitle} Jobs Online on Careerplus.shine.com".format(**context)
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
        return {'seo_title': seo_title, 'seo_desc': seo_desc, 'seo_heading': seo_heading}


def get_roundone_context_home(**kwargs):
    # clean location before forming url
    try:
        location_json = RoundOneAPI().get_location_list(**kwargs)
        # location_json.get('location_list')
        return location_json
    except:
        return {}


def get_roundone_context_listing(request=None, **kwargs):
    context = {}
    try:
        search_response = RoundOneAPI().get_search_response(request, **kwargs)
        context.update({'search_result': search_response})
        keyword = kwargs.get('keyword', '')
        location = request.GET.get('loc', '').split(',')
        initial_keyword = ""
        initial_location = []
        if keyword and keyword != "all":
            initial_keyword = keyword.replace("-", " ")
            context.update({"initial_keyword": initial_keyword})
        if location and "" not in location:
            initial_location = [x.encode('UTF-8') for x in location]
            context.update({"initial_location": str(initial_location)})
        clean_keyword = initial_keyword or keyword
        clean_location = ', '.join(initial_location) or kwargs.get('location', '')
        context.update({
            'clean_keyword': clean_keyword,
            'clean_location': clean_location
            })
        seo_data = RoundOneSEO().get_seo_data(data_for="listing", **context)
        context.update(seo_data)
        context.update(get_roundone_context_home(**kwargs))
        context.update(**kwargs)
        if request.user.is_authenticated():
            if RoundOneAPI().is_premium_user(request):
                context.update({'is_roundone_premium': True})
    except:
        pass
    return context

def get_roundone_context_detail(request=None, **kwargs):
    context = {}
    try:
        detail_response = RoundOneAPI().get_job_detail(request, **kwargs)
        data = detail_response.get("data")
        if data:
            jd = data.get("jobDescription")
            data.update({"jobDescription": jd.replace("\\n", "<br>")})
        context.update({'job_detail': detail_response})
        try:
            jobTitle = detail_response.get('data').get('jobTitle')
            breadcrumb_location = slugify(detail_response.get('data').get('location'))
            context.update({'breadcrumb_location': breadcrumb_location})
        except:
            jobTitle = kwargs.get("job_title", "Job Referral")
        context.update({'jobTitle': jobTitle})
        seo_data = RoundOneSEO().get_seo_data(data_for="detail", **context)
        context.update(seo_data)
        context.update(**kwargs)
    except:
        pass
    return context
