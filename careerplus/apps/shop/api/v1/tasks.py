import requests

from celery import task
import subprocess, os
from django.conf import settings
from shop.models import PracticeTestInfo
from core.api_mixin import NeoApiMixin

@task(name='delete_products_from_solr')
def delete_from_solr():
    subprocess.call([settings.VENV_PATH,
                     os.path.join(settings.CODE_PATH, "manage.py"), "index_products",
                     "--noinput", "--settings=careerplus.config.settings_staging"])



@task(name='update_practice_test_info')
def update_practice_test_info(email=None, with_orderitem=False):
    if not email:
        return False
    test_info = PracticeTestInfo.objects.filter(
        email=email, order_item=None
    ).first()
    if test_info:
        email = test_info.email
        json_rep = NeoApiMixin().get_pt_result(email=email)
        print(json_rep)
        if json_rep and json_rep.get('status', None) == 200:
            json_rep = json_rep.get('data', {})
            setattr(test_info, 'test_data', str(json_rep))
            test_info.save()
            if email:
                return eval(getattr(test_info, 'test_data'))
        if json_rep and json_rep.get('status', None) == 400:
            return {'status': 400}
