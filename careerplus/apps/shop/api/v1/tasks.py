from celery import task
import subprocess, os
from django.conf import settings


@task(name='delete_products_from_solr')
def delete_from_solr():
    subprocess.call([settings.VENV_PATH,
                     os.paths.join(settings.CODE_PATH, "manage.py"), "index_products",
                     "--noinput", "--settings=careerplus.config.settings_staging"])
