from __future__ import absolute_import
import urllib
import hmac
import hashlib
import requests
import logging
import csv
import StringIO

from django.conf import settings
from django.utils import timezone
from datetime import datetime
from celery.decorators import task
from shinecp.cart.models import RoundOneOrder
from core.common import ShineCandidateDetail

from shinecp.apps.resume_builder.config import REGISTER_INDUSTRY_CHOICES_K2V, CITY_K2V,FUNCTIONAL_AREA_CHOICES_K2V

@task()
def post_roundone_order(data_dict):
    try:
        user = data_dict.get('user')
        password = data_dict.get('password')
        order = data_dict.get('order')
        if order and user:
            roundone_order, created = RoundOneOrder.objects.get_or_create(
                user=user, order=order)
            if roundone_order.status != 1:
                roundone_api_dict = settings.ROUNDONE_API_DICT
                data_str = ''
                api_secret_key = roundone_api_dict.get('order_secret_key')
                user_mobile = user.userprofile.mobile if (
                    user.userprofile and user.userprofile.mobile) else ''
                order_save_url = roundone_api_dict.get('order_save_url')
                try:
                    billingDate = order.payment_date.date().strftime("%Y-%m-%d")
                except:
                    billingDate = datetime.now().strftime("%Y-%m-%d")
                data_dict = {
                    'emailId': user.email,
                    'name': user.first_name,
                    'mobile': order.order_mobile if order.order_mobile else user_mobile,
                    'amount': roundone_api_dict.get('amount', 1999),
                    'orderId': order.id,
                    'transactionId': order.transaction_id,
                    'billingDate': billingDate,
                    'isBundled': int(order.is_combo_included()),
                    'organisationId': roundone_api_dict.get(
                        'organisationId', 11),
                    'password': password
                }
                data_str = '&'.join('{}={}'.format(key, value) for key, value in data_dict.items())
                data_encoded = urllib.quote_plus(data_str)
                hmac_value = hmac.new(api_secret_key, data_str, hashlib.sha1).hexdigest()
                post_data = {'data': data_encoded, 'hash': hmac_value}
                resp = requests.post(order_save_url, data=post_data)
                try:
                    if resp and resp.status_code == 200:
                        resp_json = resp.json()
                        if resp_json:
                            status = resp_json.get('status')
                            roundone_order.status = status
                            if status == 1 or status == "1":
                                roundone_order.remark = resp_json.get('data', resp_json)
                                roundone_order.completed_on = datetime.now()
                            else:
                                roundone_order.remark = resp_json.get('error', resp_json)
                except Exception as e:
                    roundone_order.remark = str(e)
                roundone_order.save()
    except Exception as e:
        logging.getLogger('error_log').error(str(e))

@task()
def roundone_query_save(data_dict):
    try:
        shine_id = data_dict.get('appId')
        job_id = data_dict.get('jobId')
        ref_id = data_dict.get('refId')
        if shine_id:
            shine_profile = ShineCandidateDetail().get_candidate_detail(shine_id=shine_id)
            if shine_profile:

                personal_detail = shine_profile.get('personal_detail', '')
                candidate_id = shine_profile.get('candidate_id',  '')
                desired_job = shine_profile.get('desired_job', '')
                workex = shine_profile.get('workex', '')
                total_experience = shine_profile.get('total_experience', '')
                email , first_name, last_name, mobile, candidate_location = '', '' , '', '', ''
                country_code, industry , fa, experience = '', '', '', '' 
                salary = ''
                if personal_detail:
                    personal_detail = personal_detail[0]
                    email = personal_detail.get('email', '')
                    first_name = personal_detail.get('first_name', '')
                    last_name = personal_detail.get('last_name', '')
                    mobile = personal_detail.get('cell_phone', '')
                    country_code = personal_detail.get('country_code', '')
                    candidate_location_id = personal_detail.get('candidate_location','')
                    
                    if candidate_location_id:
                        candidate_location = CITY_K2V.get(candidate_location_id,'')
                if desired_job:
                    desired_job = desired_job[0]
                    industry_id = desired_job.get('industry','')
                    if industry_id:
                        industry = REGISTER_INDUSTRY_CHOICES_K2V.get(industry_id[0],'')
                    fa_id = desired_job.get('functional_area', '')
                    if fa_id:
                        fa = FUNCTIONAL_AREA_CHOICES_K2V.get(fa_id[0],'')
                if total_experience:
                    total_experience = total_experience[0]
                    exp_year = total_experience.get('experience_in_years', 0)
                    exp_month = total_experience.get('experience_in_months', 0)
                    if not exp_year:
                        exp_year = 0
                    if not exp_month:
                        exp_month = 0
                    experience = ' '.join([str(exp_year), 'Year', str(exp_month), 'months'])
                
                if workex:
                    workex = workex[0]
                    salary_lakh = workex.get('salary_in_lakh',0)
                    salary_thousand = workex.get('salary_in_thousands',0)
                    if not salary_lakh:
                        salary_lakh = 0
                    if not salary_thousand:
                        salary_thousand = 0

                    salary = ' '.join([str(salary_lakh), 'lakhs', str(salary_thousand), 'thousands'])

                
                import os
                writepath = settings.SHINE_ROUNDONE_CLICK + '/roundone_click' +datetime.now().strftime("%Y-%m-%d") +'.csv'

                if os.path.exists(writepath):
                    with open(writepath, 'a') as csvfile:
                        fieldnames = ['jobId','refId', 'userId', 'email','first_name', 'last_name',
                            'country_code','mobile','candidate_location','industry','fa','total_experience','salary']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'jobId': job_id, 'refId': ref_id, 'userId': shine_id,
                            'email': email, 'first_name': first_name, 'last_name': last_name,
                            'country_code': country_code, 'mobile':mobile, 
                            'candidate_location':candidate_location, 'industry': industry, 'fa':fa, 
                            'total_experience':experience, 'salary':salary})
                      
                else:
                    with open(writepath, 'w') as csvfile:
                        fieldnames = ['jobId','refId', 'userId', 'email','first_name', 'last_name',
                            'country_code','mobile','candidate_location','industry','fa','total_experience', 'salary']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({'jobId': job_id, 'refId': ref_id, 'userId': shine_id,
                            'email': email, 'first_name': first_name, 'last_name': last_name,
                            'country_code': country_code, 'mobile':mobile, 
                            'candidate_location':candidate_location, 'industry': industry, 'fa':fa, 
                            'total_experience':experience, 'salary': salary})
                
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        pass
