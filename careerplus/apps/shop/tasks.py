#python imports
import logging,json

#django imports
from django.conf import settings

#local imports
from shop.models import ProductAuditHistory

#inter app imports

#third party imports
import requests
from celery.decorators import task


@task(name="add_log_in_product_audit_history")
def add_log_in_product_audit_history(**data):
    ProductAuditHistory.objects.create(**data)


@task
def push_updated_product_to_crm(pid):
    from shop.models import Product
    from shop.serializers import CRMProductSerializer

    headers = {'content-type':'application/json',
            'Authorization':'Token ' + settings.SHINECPCRM_DICT.get('token')
            }
    post_url = settings.SHINECPCRM_DICT.get('base_url') + \
        settings.SHINECPCRM_DICT.get('update_products_url')
    product = Product.objects.filter(id=pid).first()
    
    if not product:
        logging.getLogger('error_log').error("No product obj found pid - {}".format(pid))
        return

    data_dict = CRMProductSerializer(product).data
    try:
        response = requests.post(
            post_url,
            data=json.dumps(data_dict),
            headers=headers,
            timeout=settings.SHINECPCRM_DICT.get('timeout'))

    except Exception as e:
        logging.getLogger('error_log').error("{} - pid : {}".format(e,pid))
        return
        
    if response.status_code == 200:
        logging.getLogger('info_log').info("{} Product Updated".format(pid))

    else:
        logging.getLogger('error_log').error(
            "Product Update Failed {} - {}".format(pid,response.content))
        
