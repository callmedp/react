import requests
import logging
from celery import task
import subprocess, os
from django.conf import settings
from shop.models import PracticeTestInfo
from core.api_mixin import NeoApiMixin
from review.models import Review
from django.contrib.contenttypes.models import ContentType

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
        if json_rep and json_rep.get('status', None) == 200:
            json_rep = json_rep.get('data', {})
            setattr(test_info, 'test_data', str(json_rep))
            test_info.save()
            if email:
                return eval(getattr(test_info, 'test_data'))
        if json_rep and json_rep.get('status', None) == 400:
            return {'status': 400}


@task(name='create_neo_lead')
def create_neo_lead(email=None):
    from crmapi.models import UserQuries, DEFAULT_SLUG_SOURCE
    from crmapi.tasks import create_lead_crm
    if not email:
        return False
    test_info = PracticeTestInfo.objects.filter(
        email=email, order_item=None
    ).first()
    if test_info:
        msg = ''
        from geolocation.models import Country
        country = Country.objects.get(
            phone='91', name='India')
        scores = ['pt_level', 'certificate_level', 'ielts', 'toeic', 'toefl', 'dyned']
        skills = ['listening', 'vocabulary', 'social_interaction', 'reading', 'grammar']

        results = eval(test_info.test_data).get('result', '')
        msg = ', '.join([str(k) + ':-' + str(results.get(k, '')) for k in scores ])
        skills = ', '.join([k + ':-' + str(results.get('skills', {}).get(k)) for k in skills ])
        msg = msg + ', ' + skills
        lead_source = 2
        campaign_slug = 'neo'
        medium = 0
        Country.objects.get_or_create(
            phone='91', name='India')
        lead = UserQuries.objects.create(
            name=test_info.name,
            email=test_info.email,
            country=country,
            phn_number=test_info.mobile_no.replace('+91',''),
            message=msg,
            lead_source=lead_source,
            product='Neo Product',
            product_id=999999,
            medium=medium,
            campaign_slug=campaign_slug,
        )
        flag = create_lead_crm(pk=lead.pk)
        if flag:
            lead.lead_created = True
            lead.save()


@task(name='create_product_review_task')
def create_product_review_task(product_id, name, email, candidate_id, review, rating, title):
    try:
        content_type = ContentType.objects.get(
            app_label="shop", model="product")
        review_obj_created = Review.objects.create(
            content_type=content_type,
            object_id=product_id,
            user_name=name,
            user_email=email,
            user_id=candidate_id,
            content=review,
            average_rating=rating,
            title=title
        )
        extra_content_obj = ContentType.objects.get(
            app_label="shop", model="product")
        review_obj_created.extra_content_type = extra_content_obj
        review_obj_created.extra_object_id = product_id
        review_obj_created.save()
    except Exception as e:
        logging.getLogger('error_info').error('error is task log: {}'.format(str(e)))

