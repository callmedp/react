import logging
import json
import requests
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from celery.decorators import task

from core.api_mixin import CrmApiMixin

from .models import AdServerLead, UserQuries


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
        if not usr_query.lead_created:
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
        logging.getLogger('error_log').error("%s" % str(e))


@task()
def addAdServerLead(query_dict):
    email = str(query_dict.get('email', ''))
    mobile = str(query_dict.get('mobile', ''))
    country_code = str(query_dict.get('country_code', '91'))
    timestamp = str(query_dict.get('timestamp', ''))
    url = str(query_dict.get('url', ''))
    utm_parameter = query_dict.get('utm_parameter', '')

    try:
        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_obj = timezone.make_aware(timestamp_obj, timezone.get_current_timezone())
    except:
        timestamp_obj = timezone.now()

    object_list = AdServerLead.objects.filter(
        email=email,
        country_code=country_code, mobile=mobile, created=False,
        timestamp__year=timestamp_obj.year, timestamp__month=timestamp_obj.month,
        timestamp__day=timestamp_obj.day)
    if not object_list.exists():
        AdServerLead.objects.create(
            email=email, country_code=country_code,
            mobile=mobile, url=url, timestamp=timestamp_obj,
            utm_parameter=utm_parameter)


@task(name="create_lead_on_crm")
def create_lead_crm(pk=None):
    try:
        data_dict = {}
        lead = UserQuries.objects.get(pk=pk)

        if lead.lead_source in [4]:
            pass
        else:
            lsource = 0
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
        })
        flag = CrmApiMixin().create_lead_by_api(data_dict=data_dict)
        if flag:
            lead.lead_created = True
            lead.save()
    except Exception as e:
        logging.getLogger('error_log').error("%s" % str(e))
