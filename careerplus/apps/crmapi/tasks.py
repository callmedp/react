import logging
import json
import requests
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from celery.decorators import task
from geolocation.models import Country
from core.api_mixin import CrmApiMixin

from shine.core import ShineCandidateDetail
from .models import UserQuries
from .models import UNIVERSITY_LEAD_SOURCE
from crmapi.config import (
    EXPERIENCE_IN_YEARS_MODEL_CHOICES, SALARY_IN_LAKH_MODEL_CHOICES
)

@task(name="post_psedu_lead")
def post_psedu_lead(query_dict):
    headers = {}
    lead = {}
    headers['content-type'] = 'application/json'
    headers['Authorization'] = 'Token ' + settings.SHINECPCRM_DICT.get('token')[0]
    post_url = settings.SHINECPCRM_DICT.get('base_url') + \
        settings.SHINECPCRM_DICT.get('create_lead_url')

    lead["name"] = query_dict.get('name', '')
    lead["country_code"] = query_dict.get('country_code', '')
    lead["mobile"] = str(query_dict.get('mobile', ''))
    lead["message"] = str(query_dict.get('message', ''))
    lead["status"] = 0
    lead["source"] = str(query_dict.get('source', ''))
    lead["lsource"] = int(query_dict.get('lead_source', 0))
    lead["product"] = str(query_dict.get('product', ''))
    lead["medium"] = int(query_dict.get('medium', 0))
    try:
        usr_query = UserQuries.objects.get(
            id=query_dict.get('queryid', ''))
        if not usr_query.lead_created and usr_query.lead_source != 21:
            rsp = requests.post(
                post_url, data=json.dumps(lead),
                headers=headers,
                timeout=settings.SHINECPCRM_DICT.get('timeout'))
            if rsp.status_code == 201:
                usr_query.lead_created = True
                usr_query.save()
                logging.getLogger('error_log').error("%s" % str(rsp.json()))
            elif rsp.status_code != 201:
                logging.getLogger('error_log').error("%s" % str(rsp.json()))
    except Exception as e:
        logging.getLogger('error_log').error("unable to lead query%s" % str(e))


# @task()
# def addAdServerLead(query_dict):
#     email = str(query_dict.get('email', ''))
#     mobile = str(query_dict.get('mobile', ''))
#     country_code = str(query_dict.get('country_code', '91'))
#     timestamp = str(query_dict.get('timestamp', ''))
#     url = str(query_dict.get('url', ''))
#     utm_parameter = query_dict.get('utm_parameter', '')

#     try:
#         timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#         timestamp_obj = timezone.make_aware(timestamp_obj, timezone.get_current_timezone())
#     except:
#         timestamp_obj = timezone.now()

#     object_list = AdServerLead.objects.filter(
#         email=email,
#         country_code=country_code, mobile=mobile, created=False,
#         timestamp__year=timestamp_obj.year, timestamp__month=timestamp_obj.month,
#         timestamp__day=timestamp_obj.day)
#     if not object_list.exists():
#         AdServerLead.objects.create(
#             email=email, country_code=country_code,
#             mobile=mobile, url=url, timestamp=timestamp_obj,
#             utm_parameter=utm_parameter)


@task(name="add_server_lead_task")
def add_server_lead_task(query_dict):
    email = str(query_dict.get('email', ''))
    mobile = str(query_dict.get('mobile', ''))
    country_code = str(query_dict.get('country_code', '91'))
    timestamp = str(query_dict.get('timestamp', ''))
    url = str(query_dict.get('url', ''))
    utm_parameter = query_dict.get('utm_parameter', '')
    product_id = query_dict.get('product_id', '')
    product = query_dict.get('product', '')
    campaign_slug = query_dict.get('campaign_slug', '')

    try:
        country_obj = Country.objects.get(phone=country_code)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get country object %s'%str(e))
        country_obj = Country.objects.get(phone='91')

    try:
        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_obj = timezone.make_aware(
            timestamp_obj, timezone.get_current_timezone())
    except Exception as e:
        logging.getLogger('error_log').error(str(e))
        timestamp_obj = timezone.now()

    object_list = UserQuries.objects.filter(
        email=email,
        country=country_obj, phn_number=mobile, lead_created=False,
        lead_source=21, timestamp__year=timestamp_obj.year,
        timestamp__month=timestamp_obj.month,
        timestamp__day=timestamp_obj.day)
    if not object_list.exists():
        UserQuries.objects.create(
            email=email, country=country_obj,
            phn_number=mobile, path=url, timestamp=timestamp_obj,
            product_id=product_id, product=product, lead_source=21,
            utm_parameter=utm_parameter, campaign_slug=campaign_slug)


@task(name="create_lead_crm")
def create_lead_crm(pk=None, validate=False, product_offer = None):
    flag = False
    try:
        data_dict = {}
        lead = UserQuries.objects.get(pk=pk)

        if lead.inactive:
            print('lead is already inactive -{}'.format(lead.id))
            return

        lsource = lead.lead_source
        total_experience = 0
        total_salary = 0
        valid_source_list = [4, 23, 2, 1, UNIVERSITY_LEAD_SOURCE]
        if validate:
            # if lead source not in valid source list , we will check for salary and experience criteria
            if lead.lead_source not in valid_source_list:

                candidate_response = ShineCandidateDetail().get_candidate_detail(email=lead.email)
                if candidate_response:
                    if 'total_experience' in candidate_response and candidate_response['total_experience']:
                        total_experience = candidate_response['total_experience'][0].get('experience_in_years', 0)
                        total_experience = int(dict(EXPERIENCE_IN_YEARS_MODEL_CHOICES).get(total_experience).replace('>','').replace('Yr','').replace('s', ''))

                    if candidate_response['workex']:
                        total_salary = candidate_response['workex'][0].get('salary_in_lakh', 0)
                        total_salary = dict(SALARY_IN_LAKH_MODEL_CHOICES).get(total_salary)
                        if isinstance(total_salary, int):
                            total_salary = total_salary
                        elif isinstance(total_salary, str):
                            total_salary = 55

                    if total_experience < 4 or total_salary < 4:
                        if not product_offer: 
                            return flag
                        else :
                            flag = True
                else:
                    if not product_offer: 
                            return flag
                    else :
                        flag = True

        data_dict.update({
            "name": lead.name,
            "email": lead.email,
            "country_code": lead.country.phone if lead.country else '91',
            "mobile": lead.phn_number,
            "message": lead.message,
            "path": lead.path,
            "product": lead.product,
            "product_id": lead.product_id,
            "lead_source": lsource,
            "campaign_slug": lead.campaign_slug,
            "medium": lead.medium,
            "source": lead.source,
            "utm_parameter": lead.utm_parameter,
            "sub_campaign":lead.sub_campaign_slug
        })
        flag = CrmApiMixin().create_lead_by_api(data_dict=data_dict)
        if flag:
            lead.lead_created = True
            lead.save()
    except Exception as e:
        logging.getLogger('error_log').error("unable to create lead from crm%s" % str(e))

    return flag
