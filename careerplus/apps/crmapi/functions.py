import json
import logging
import requests
from django.conf import settings


def lead_create_on_crm(cart_obj, data_dict=None):
    headers = dict()
    headers['content-type'] = 'application/json'
    headers['Authorization'] = 'Token ' + settings.SHINECPCRM_DICT.get('token')
    post_url = settings.SHINECPCRM_DICT.get('base_url') + \
               settings.SHINECPCRM_DICT.get('create_lead_url')
    try:
        mobileNo = data_dict.get('mobile')
        if mobileNo:
            rsp = requests.post(
                post_url, data=json.dumps(data_dict),
                headers=headers,
                timeout=settings.SHINECPCRM_DICT.get('timeout'))
            api_rsp = rsp.json()
            if rsp.status_code in [201, 200] and api_rsp.get('status') == 1:
                cart_obj.lead_created = True
                cart_obj.save()
                logging.getLogger('info_log').info('LEAD_CREATE_ON_SPCRM lead created/updated on crm {}'.format(str(data_dict)))
            elif rsp.status_code == 400 and api_rsp.get('status') == 0:
                failed_response = cart_obj.utm_params + json.dumps(rsp.json())
                cart_obj.utm_params = failed_response
                cart_obj.save()
                logging.getLogger('error_log').error(
                    'LEAD_CREATE_ON_SPCRM FAILED TO CREATE LEAD ON CRM __.__ ERROR {}'.format(str(rsp.json())))
        else:
            logging.getLogger("error_log").error("LEAD_CREATE_ON_SPCRM cart have no mobile number")
    except Exception as e:
        logging.getLogger('error_log').error("LEAD_CREATE_ON_SPCRM lead creation from learning is failed%s" % str(e))