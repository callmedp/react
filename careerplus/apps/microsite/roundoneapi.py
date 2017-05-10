from __future__ import absolute_import
import json
import logging
import requests
from collections import OrderedDict
from itertools import islice
from django.conf import settings


class RoundOneAPI(object):

    def get_location_list(self, **kwargs):
        try:
            location_json = settings.REDIS_CON.get('roundone_location')

            if location_json:
                return json.loads(location_json.decode())

            url = settings.ROUNDONE_API_DICT.get("location_url")
            response = requests.get(url, timeout=settings.ROUNDONE_API_TIMEOUT)

            if response.status_code == 200:
                location_list = response.json()
                location_json = json.dumps({"location_list": location_list[1: -1]})
                settings.REDIS_CON.setex('roundone_location', 3600, location_json)
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
            userEmail = '127.0.0.1'#self.get_user_ip(request)
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
                # "location": ["delhi", "Bengaluru"],
                # 'searchKeyword': "java",
                "userEmail": userEmail,
                "start": start,
                "rows": rows,
                "sort": sort_by,
                "affiliateName": settings.ROUNDONE_API_DICT.get("affiliateName", 'CP')
            }
            
            location = request.GET.get('loc', '')
            keyword = kwargs.get('keyword', '')
            company_list = request.GET.get('company', '').split(',')
            
            location  = location if location else kwargs.get('location', '')

            if location and location != "all":
                post_data.update({"location": location.split(",")})
            
            if keyword and keyword != "all":
                searchKeyword = keyword.replace("-", " ")[:45]
                post_data.update({"searchKeyword": searchKeyword})

            if company_list:
                post_data.update({'companyId': company_list})

            headers = {'content-type': 'application/json'}

            response = requests.post(
                post_url, data=json.dumps(post_data),
                headers=headers, timeout=settings.ROUNDONE_API_TIMEOUT,
            )

            if response.status_code == 200:
                response_json = response.json()
                response_json.update({'response': True, 'company_list': company_list})
                sortedCompany = request.session.get('sortedCompany', {})
                companyJobCount = response_json.get('companyJobCount', {})

                if companyJobCount:
                    company_dict = OrderedDict(sorted(companyJobCount.items(), key=lambda k: k[1]['jobCount'], reverse=False))
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
            hmac_value = hmac.new(api_secret_key, data_str, hashlib.sha1).hexdigest()
            data_dict.update({"hash": hmac_value})
            response = requests.get(url, params=data_dict, timeout=settings.ROUNDONE_API_TIMEOUT)

            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('status') == "1":
                    response_json.update({'response': True, 'jobId': job_params[0]})
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
