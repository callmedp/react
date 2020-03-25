import logging
from celery.decorators import task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.cache import cache


from linkedin.autologin import AutoLogin

from order.functions import (
    create_short_url,
    send_email
)
from emailers.sms import SendSMS
from emailers.email import SendMail
from payment.models import PaymentTxn
from core.mixins import InvoiceGenerate
from coupon.mixins import CouponMixin
from api.config import LOCATION_MAPPING, INDUSTRY_MAPPING, DESIRED_SALARY_MAPPING
from shine.core import ShineCandidateDetail
from crmapi.config import (
    EXPERIENCE_IN_YEARS_MODEL_CHOICES
)
from shop.models import PracticeTestInfo
from core.api_mixin import NeoApiMixin

from shop.models import ProductUserProfile


@task(name="invoice_generation_order")
def invoice_generation_order(order_pk=None):
    from order.models import Order
    try:
        order = Order.objects.get(pk=order_pk)
        InvoiceGenerate().save_order_invoice_pdf(order=order)
    except Exception as e:
        logging.getLogger('error_log').error("invoice generation failed%s" % (str(e)))


@task(name="pending_item_email")
def pending_item_email(pk=None):
    from order.models import Order
    order = Order.objects.get(pk=pk)
    order_items = order.orderitems.filter(no_process=False).select_related(
        'order', 'product', 'partner')

    data = {}
    token = AutoLogin().encode(
            order.email, order.candidate_id, days=None)
    data.update({
            'subject': 'To initiate your services fulfil these details',
            'username': order.first_name,
            'mobile': order.get_mobile(),
            'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token)
    })
    urlshortener = create_short_url(login_url=data)
    data.update({'url': urlshortener.get('url')})

    to_emails = [order.get_email()]
    mail_type = "PENDING_ITEMS"
    product_names = []
    oi_status_mapping = {}

    for oi in order_items:
        email_sets = list(oi.emailorderitemoperation_set.all().values_list(
            'email_oi_status', flat=True).distinct())
        sms_sets = list(oi.smsorderitemoperation_set.all().values_list(
            'sms_oi_status', flat=True).distinct())
        sms_oi_status = None

        if (oi.product.type_flow == 9) and (121 not in email_sets) and (121 not in sms_sets):
            type_flow_9_data = data
            type_flow_9_data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard/roundone/profile/" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
                'type_flow': 9,
                'product_url': oi.product.get_url(),
            })
            send_email(to_emails, mail_type, type_flow_9_data, 121, oi.pk)
            urlshortener = create_short_url(login_url=type_flow_9_data)
            type_flow_9_data.update({'url': urlshortener.get('url')})
            SendSMS().send(sms_type=mail_type, data=type_flow_9_data)
            sms_oi_status = 121

        elif (oi.product.type_flow == 10) and (131 not in email_sets) and (131 not in sms_sets):
            type_flow_10_data = data
            type_flow_10_data.pop('upload_url', None)
            type_flow_10_data.update({
                'test_url': "%s/dashboard" % (settings.SITE_DOMAIN),
                'type_flow': 10,
                'product_url': oi.product.get_url(),
            })
            send_email(to_emails, mail_type, type_flow_10_data, 131, oi.pk)
            urlshortener = create_short_url(login_url=type_flow_10_data)
            type_flow_10_data.update({'url': urlshortener.get('url')})
            SendSMS().send(sms_type=mail_type, data=type_flow_10_data)
            sms_oi_status = 131

        if oi.oi_resume or oi.oi_status == 61:
            continue

        if (oi.product.type_flow == 1) and (21 not in email_sets) and (21 not in sms_sets):
            oi_status_mapping.update({oi.id: 21})
            product_names.append(oi.product.name)
            sms_oi_status = 21

        elif (oi.product.type_flow == 3) and (41 not in email_sets) and (41 not in sms_sets):
            oi_status_mapping.update({oi.id: 41})
            product_names.append(oi.product.name)
            sms_oi_status = 41

        elif (oi.product.type_flow == 4) and (61 not in email_sets or 61 not in sms_sets):
            oi_status_mapping.update({oi.id: 61})
            product_names.append(oi.product.name)
            sms_oi_status = 61

        elif (oi.product.type_flow == 5 and oi.product.sub_type_flow in [501]) \
                and (71 not in email_sets) and (71 not in sms_sets):
            oi_status_mapping.update({oi.id: 71})
            product_names.append(oi.product.name)
            sms_oi_status = 71

        elif (oi.product.type_flow in [7, 15]) and (91 not in email_sets) and (91 not in sms_sets):
            oi_status_mapping.update({oi.id: 91})
            product_names.append(oi.product.name)
            sms_oi_status = 91

        elif (oi.product.type_flow == 12) and (141 not in email_sets or 141 not in sms_sets):
            oi_status_mapping.update({oi.id: 141})
            product_names.append(oi.product.name)
            sms_oi_status = 141

        elif (oi.product.type_flow == 13) and (151 not in email_sets) and (151 not in sms_sets):
            oi_status_mapping.update({oi.id: 151})
            product_names.append(oi.product.name)
            sms_oi_status = 151

        elif (oi.product.type_flow == 8) and (108 not in email_sets) and (108 not in sms_sets):
            oi_status_mapping.update({oi.id: 108})
            product_names.append(oi.product.name)
            sms_oi_status = 108

        if sms_oi_status:
            oi.smsorderitemoperation_set.create(
                sms_oi_status=sms_oi_status,
                to_mobile=data.get('mobile'),
                status=1)

    if oi_status_mapping:
        data.update({
                'product_names': product_names,
                'combined_mail': True  # for type flow type_flow = [1,3,4,5,12,13,7,8,15]
            })
        SendSMS().send(sms_type=mail_type, data=data)
        send_email(
            to_emails=to_emails, mail_type=mail_type,
            email_dict=data, oi_status_mapping=oi_status_mapping
            )


@task(name="process_mailer")
def process_mailer(pk=None):
    from order.models import Order
    order = Order.objects.filter(pk=pk).first()

    if (not order) or (not order.status == 1):
        return

    orderitems = order.orderitems.filter(no_process=False).select_related(
        'order', 'product', 'partner')

    for oi in orderitems:
        token = AutoLogin().encode(
            oi.order.email, oi.order.candidate_id, days=None)
        email_sets = list(oi.emailorderitemoperation_set.all().values_list(
            'email_oi_status', flat=True).distinct())
        sms_sets = list(oi.smsorderitemoperation_set.all().values_list(
            'sms_oi_status', flat=True).distinct())
        to_emails = [oi.order.get_email()]
        mail_type = "PROCESS_MAILERS"
        data = {}
        data.update({
            'subject': 'Your service details related to order <' + str(oi.order.id) + '>',
            'username': oi.order.first_name,
            'type_flow': oi.product.type_flow,
            'sub_type_flow': oi.product.sub_type_flow,
            'pk': oi.pk,
            'oi': oi,
            'product_name': oi.product.name,
            'product_url': oi.product.get_url(),
            'vendor_name': oi.product.vendor.name,
            'email': oi.order.get_email(),
            'candidateid': oi.order.email,
            'mobile': oi.order.get_mobile(),
            'parent_name': oi.parent.product.name if oi.parent else None
        })
        email_status, sms_status = None, None

        if oi.product.type_flow in [1, 12, 13] and (25 not in email_sets and 25 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 25
            sms_status = 25

        elif oi.product.type_flow == 3 and (44 not in email_sets and 44 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 44
            sms_status = 44

        elif oi.product.type_flow == 4 and (64 not in email_sets and 64 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 64
            sms_status = 64

        elif oi.product.type_flow == 5 and (74 not in email_sets and 74 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 74
            sms_status = 74

        elif oi.product.type_flow == 12 and (145 not in email_sets and 145 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_DOMAIN, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 145
            sms_status = 145

        elif oi.product.type_flow == 13 and (155 not in email_sets and 155 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 155
            sms_status = 155

        elif oi.product.type_flow in [7, 15] and (94 not in email_sets and 94 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 94
            sms_status = 94

        elif oi.product.type_flow == 2 and (161 not in email_sets and 161 not in sms_sets):
            email_status = 161
            sms_status = 161

        elif oi.product.type_flow == 14 and (191 not in email_sets and 191 not in sms_sets):
            email_status = 191
            sms_status = 191

        elif oi.product.type_flow == 6 and (171 not in email_sets and 171 not in sms_sets):
            email_status = 171
            sms_status = 171

        elif oi.product.type_flow == 8 and (105 not in email_sets and 105 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token),
            })
            email_status = 105
            sms_status = 105

        elif oi.product.type_flow == 9 and (122 not in email_sets and 122 not in sms_sets):
            data.update({
                'upload_url': "%s://%s/autologin/%s/?next=/dashboard/roundone/profile/" % (
                    settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                    token)
            })
            email_status = 122
            sms_status = 122

        if email_status:
            send_email(to_emails, mail_type, data, email_status, oi.pk)

        if sms_status:
            SendSMS().send(sms_type=mail_type, data=data)
            oi.smsorderitemoperation_set.create(
                sms_oi_status=sms_status,
                to_mobile=data.get('mobile'),
                status=1)


@task(name="payment_pending_mailer")
def payment_pending_mailer(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (str(order), str(e)))
    try:
        pymt_objs = PaymentTxn.objects.filter(
            order=order, payment_mode__in=[1, 4])
        if pymt_objs.exists():
            orderitems = order.orderitems.filter(
                no_process=False).select_related('order', 'product', 'partner')

            mail_flag = False
            sms_flag = False

            for oi in orderitems:
                pymt_obj = oi.order.ordertxns.get(order=order)
                email_sets = list(
                    oi.emailorderitemoperation_set.all().values_list(
                        'email_oi_status', flat=True).distinct())
                sms_sets = list(
                    oi.smsorderitemoperation_set.all().values_list(
                        'sms_oi_status', flat=True).distinct())

                data = {}
                data.update({
                    "subject": 'Your Shine Payment Confirmation pending',
                    "username": order.first_name,
                    "txn": pymt_obj.txn,
                    'mobile': oi.order.get_mobile(),
                })
                mail_type = "PAYMENT_PENDING"
                sms_type = 'OFFLINE_PAYMENT'

                to_emails = [order.get_email()]
                if not mail_flag and 1 not in email_sets:
                    send_email(to_emails, mail_type, data, status=1, oi=oi.pk)
                    mail_flag = True
                elif 1 not in email_sets:
                    to_email = to_emails[0] if to_emails else oi.order.get_email()
                    oi.emailorderitemoperation_set.create(
                        email_oi_status=1, to_email=to_email,
                        status=1)

                if not sms_flag and 1 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=1,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))
                elif 1 not in sms_sets:
                    oi.smsorderitemoperation_set.create(
                        sms_oi_status=1,
                        to_mobile=data.get('mobile'),
                        status=1)

                # if 1 not in email_sets and 1 not in sms_sets:
                #     to_emails = [order.email]
                #     mail_type = "PAYMENT_PENDING"
                #     sms_type = 'OFFLINE_PAYMENT'
                #     data = {}
                #     data.update({
                #         "subject": 'Your Shine Payment Confirmation pending',
                #         "username": order.first_name,
                #         "txn": pymt_obj.txn,
                #         'mobile': oi.order.mobile,
                #     })
                #     send_email(to_emails, mail_type, data, status=1, oi=oi.pk)
                #     try:
                #         SendSMS().send(sms_type=sms_type, data=data)
                #         oi.smsorderitemoperation_set.create(
                #             sms_oi_status=1,
                #             to_mobile=data.get('mobile'),
                #             status=1)
                #     except Exception as e:
                #         logging.getLogger('error_log').error(
                #             "%s - %s" % (str(sms_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error("%s - %s" % (str(mail_type), str(e)))


@task(name="payment_realisation_mailer")
def payment_realisation_mailer(pk=None):
    from order.models import Order
    order = None
    mail_type = "SHINE_PAYMENT_CONFIRMATION"
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get order object %s' % str(e))
    try:
        invoice_data = InvoiceGenerate().get_invoice_data(order=order)
        pymt_objs = PaymentTxn.objects.filter(order=order)
        for pymt_obj in pymt_objs:
            if pymt_obj.status == 1:
                to_emails = [order.get_email()]
                # feature coupon
                courses_p = order.orderitems.filter(
                    product__product_class__slug__in=settings.COURSE_SLUG)
                if courses_p.exists():
                    coupon_obj = CouponMixin().create_feature_coupon(
                        users=[order.email])
                else:
                    coupon_obj = None
                if coupon_obj:
                    feature_coupon_code = coupon_obj.code
                else:
                    feature_coupon_code = ''
                invoice_data.update({
                    'subject': 'Your Shine Payment Confirmation',
                    "first_name": order.first_name,
                    "txn": pymt_obj.txn,
                    "order_id": order.id,
                    'feature_coupon_code': feature_coupon_code,
                    'site': 'https://' + settings.SITE_DOMAIN + settings.STATIC_URL,
                })
                try:
                    SendMail().send(to_emails, mail_type, invoice_data)
                    logging.getLogger('info_log').info(
                        "payment realisation mail send to %s - %s" % (
                            str(to_emails), str(mail_type)))
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "payment realisation %s - %s - %s" % (
                            str(to_emails), str(mail_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s - %s" % (str(mail_type), str(e)))


@task(name="service_initiation")
def service_initiation(pk=None):
    from order.models import Order
    order = None
    try:
        order = Order.objects.get(pk=pk)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get order object%s' % str(e))
    try:
        if order:
            orderitems = order.orderitems.filter(
                no_process=False).select_related('order', 'product', 'partner')
            for oi in orderitems:
                data = {}
                token = token = AutoLogin().encode(
                    oi.order.get_email(), oi.order.candidate_id, days=None)
                sms_type = "SERVICE_INITIATION"
                data.update({
                    'mobile': oi.order.get_mobile(),
                    'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                        settings.SITE_PROTOCOL, settings.SITE_DOMAIN,
                        token),
                })
                sms_sets = list(
                    oi.smsorderitemoperation_set.all().values_list(
                        'sms_oi_status', flat=True).distinct())

                urlshortener = create_short_url(login_url=data)
                data.update({'url': urlshortener.get('url')})

                if oi.product.type_flow == 2 and 162 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=162,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))

                elif oi.product.type_flow == 14 and 192 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=192,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))

                elif oi.product.type_flow == 6 and 172 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=172,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error("%s - %s" % (
                            str(sms_type), str(e)))
                elif oi.product.type_flow == 10 and 133 not in sms_sets:
                    try:
                        SendSMS().send(sms_type=sms_type, data=data)
                        oi.smsorderitemoperation_set.create(
                            sms_oi_status=133,
                            to_mobile=data.get('mobile'),
                            status=1)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(sms_type), str(e)))
    except Exception as e:
        logging.getLogger('error_log').error('service initiation failed%s' % str(e))


@task(name="process_jobs_on_the_move")
def process_jobs_on_the_move(obj_id=None):
    from order.models import OrderItem
    obj = OrderItem.objects.filter(id=obj_id).first()
    # create jobs on the move profile after welcome call is done.
    if obj:
        if obj.is_combo and obj.parent:
            wc_cat = obj.parent.wc_cat
            wc_sub_cat = obj.parent.wc_sub_cat
        else:
            wc_cat = obj.wc_cat
            wc_sub_cat = obj.wc_sub_cat
        if ((wc_cat == 21 and wc_sub_cat in [41, 42]) or (wc_cat == 22 and wc_sub_cat == 63)) and \
                not getattr(obj, 'whatsapp_profile_orderitem', False):
            other_jobs_on_the_move = OrderItem.objects.filter(
                order__status__in=[1, 3],
                product__type_flow__in=[5],
                oi_status__in=[31, 32],
                product__sub_type_flow=502,
                order__candidate_id=obj.order.candidate_id
            ).exclude(whatsapp_profile_orderitem=None).first()

            desired_industry, desired_location, desired_salary, current_salary, \
                experience, skills = '', '', '', '', '', ''
            latest_education = None

            if other_jobs_on_the_move:
                desired_industry = other_jobs_on_the_move.whatsapp_profile_orderitem.\
                    desired_industry
                desired_location = other_jobs_on_the_move.whatsapp_profile_orderitem.\
                    desired_location
                desired_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_salary
                current_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.current_salary
                experience = other_jobs_on_the_move.whatsapp_profile_orderitem.experience
                skills = other_jobs_on_the_move.whatsapp_profile_orderitem.skills
                latest_education = other_jobs_on_the_move.whatsapp_profile_orderitem.\
                    latest_education
            else:
                resp_status = ShineCandidateDetail().get_candidate_detail(
                    email=obj.order.email, shine_id=None)

                if 'total_experience' in resp_status and resp_status['total_experience']:
                    experience_years = resp_status['total_experience'][0].get('experience_in_years', 0)
                    experience_months = resp_status['total_experience'][0].get('experience_in_months', 0)

                    experience_years = dict(EXPERIENCE_IN_YEARS_MODEL_CHOICES).get(experience_years)
                    if experience_months:
                        experience_months = str(experience_months) + ' months'
                    experience = '{} {}'.format(experience_years, experience_months)

                if 'skills' in resp_status and resp_status['skills']:
                    skills = ','.join([i['value'] for i in resp_status['skills']])[0:99]

                if 'education' in resp_status and resp_status['education']:
                    # extarcting the education level choice from shine api and storing it
                    # in latest education. Then using mapping from choices to get the education.
                    latest_education_dict = ''
                    for education in resp_status['education']:
                        if not latest_education_dict or \
                            latest_education_dict.get('year_of_passout', 0)\
                                < education.get('year_of_passout', 0):
                            latest_education_dict = education

                    latest_education = latest_education_dict.get('education_level')

                if resp_status and 'desired_job' in resp_status:

                    candidate_data = resp_status['desired_job'][0]

                    # Get canidate location
                    candidate_location = candidate_data['candidate_location']
                    desired_location = ','.join(
                        [LOCATION_MAPPING.get(loc, '') for loc in candidate_location]
                        )[0:244]

                    # Get candidate industry
                    candidate_industry = candidate_data['industry']
                    desired_industry = ','.join(
                        [INDUSTRY_MAPPING.get(ind, '') for ind in candidate_industry]
                        )[0:244]

                    # Get desired salary
                    maximum_salary = candidate_data['maximum_salary']
                    expected_min_salary = ','.join(
                        [DESIRED_SALARY_MAPPING.get(l, 'N.A') for l in maximum_salary]
                        )

                    minimum_salary = candidate_data['minimum_salary']
                    expected_max_salary = ','.join(
                        [DESIRED_SALARY_MAPPING.get(l, 'N.A') for l in minimum_salary]
                        )

                    desired_salary = expected_min_salary if expected_min_salary \
                        else expected_max_salary

                    # get current salary
                    salary_in_lakh = resp_status['workex'][0]['salary_in_lakh']
                    salary_in_thousand = resp_status['workex'][0]['salary_in_thousand']
                    current_salary = str(salary_in_lakh) + 'Lakh ' + \
                        str(salary_in_thousand) + 'Thousand'
            #  TODO handle this empty contact number issue in order
            contact_number = obj.order.mobile or "NA"
            ProductUserProfile.objects.create(
                order_item=obj,
                contact_number=contact_number,
                desired_industry=desired_industry,
                desired_location=desired_location,
                desired_salary=desired_salary,
                current_salary=current_salary,
                experience=experience,
                skills=skills,
                latest_education=latest_education,
            )
            obj.update_pending_links_count()


@task
def generate_resume_for_order(order_id):
    from resumebuilder.models import Candidate
    from order.models import Order
    from shop.models import Product
    from resumebuilder.utils import ResumeGenerator
    order_obj = Order.objects.get(id=order_id)
    candidate_id = order_obj.candidate_id

    for item in order_obj.orderitems.all():
        if item.product and item.product.type_flow == 17 and item.product.type_product == 0:
            product_id = item.product.id
            break
    product = Product.objects.filter(id=product_id).first()
    if product.sub_type_flow == 1701:
        is_combo = True
    else:
        is_combo = True if product.attr.get_value_by_attribute(
            product.attr.get_attribute_by_name('template_type')
            ).value == 'multiple' else False

    candidate_obj = Candidate.objects.filter(candidate_id=candidate_id).first()
    # if not candidate_obj create it by yourself.
    if not candidate_obj:
        selected_template = 1
    else:
        selected_template = candidate_obj.selected_template or 1
    # selected_template
    builder_obj = ResumeGenerator()
    builder_obj.save_order_resume_pdf(order=order_obj, is_combo=is_combo, index=selected_template)


@task
def send_resume_in_mail_resume_builder(attachment, data):
    to_email = [data.get('email')]
    mail_type = "SEND_RESUME_IN_MAIL_RESUME_BUILDER"
    try:
        SendMail().send(to_email, mail_type, data, attachment=attachment)
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s" % (str(e)))


@task(name='board_user_on_neo')
def board_user_on_neo(neo_ids):
    '''
    Take Neo Order Items
    - Board User on Trial Basis Or Regular Basis.
    - While Boarding User On Regular Basis Check.
        - If on Trial, then update SSO Profile.
        - else hit for Boarding assuming either
        already Regular user O New user.
    '''
    from datetime import datetime, timedelta
    from order.models import OrderItem
    neo_items = OrderItem.objects.filter(id__in=neo_ids)
    boarding_type = 'regular'
    for item in neo_items:
        email = item.order.email
        data_dict = {}
        coursetype = item.product.get_coursetype()
        duration = item.product.get_duration_in_day()
        if coursetype == 'TR':
            boarding_type = 'trail'
            data_dict['account_type'] = 'trial'
            if duration:
                start_date = datetime.now().strftime('%Y-%m-%d')
                end_date = (datetime.now() + timedelta(days=duration)).strftime('%Y-%m-%d')
                data_dict.update({
                    'start_date': start_date,
                    'end_date': end_date,
                })
        account_type = NeoApiMixin().get_student_account_type(email)
        if account_type and account_type == 'trial':
            boarding_type = 'already_trial'
            data = {
                'account_type': 'regular',
            }
            flag = NeoApiMixin().update_student_sso_profile(data=data, email=email)
            if flag:
                cache.set(
                    'updated_from_trial_to_regular_{}'.format(str(item.id)), 1, 3600 * 24 * 2
                    )
                logging.getLogger('error_log').error(
                    'Account update to Regular from Trial for email {}'.format(email)
                    )
            else:
                logging.getLogger('error_log').error(
                    'Unable to Update SSO profile for email{}'.format(email)
                    )

        else:
            flag = NeoApiMixin().board_user_on_neo(email=email, data_dict=data_dict)
            if flag:
                cache.set('neo_mail_sent_{}'.format(str(item.id)), 1, 3600 * 24 * 2)
        return boarding_type


@task
def bypass_resume_midout(order_id):
    import os
    import pytz
    from order.models import OrderItem, Order
    from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
    from datetime import timedelta, datetime
    from django.utils import timezone
    from random import random

    utc = pytz.UTC

    order = Order.objects.filter(id=order_id).first()

    if not order:
        return

    update_resume_oi_ids = []

    # update order item id to upload previous resume
    order_items = order.orderitems.all().exclude(no_process=True)
    for order_item in order_items:
        if order_item.oi_status == 2 and order_item.product.type_flow in [1, 12, 13, 8, 3, 4]:
            update_resume_oi_ids.append(order_item.id)

    if not update_resume_oi_ids:
        logging.getLogger('error_log').error("No orderitem Id found to update resume")
        return

    logging.getLogger('info_log').info(
        "Order item to update resume : {} ".format(' '.join(map(str, update_resume_oi_ids)))
        )

    old_resume = None
    oi_resume_creation_date = None
    start_date = timezone.now() - timedelta(days=180)
    end_date = timezone.now()
    # order items to get previous resume in previous 180 days
    order_items = OrderItem.objects.filter(
        order__candidate_id=order.candidate_id, created__range=[start_date, end_date]
        ).order_by('-id')

    for order_item in order_items:
        if order_item.oi_resume:
            old_resume = order_item.oi_resume
            oi_operation = order_item.orderitemoperation_set.filter(oi_status=3).last()
            oi_resume_creation_date = oi_operation.created if oi_operation else None
            break

    try:
        shine_resume_details = None
        response = ShineCandidateDetail().get_candidate_detail(shine_id=order.candidate_id)
        resumes = response.get('resumes', None)

        if len(resumes) > 0:
            shine_resume_details = resumes[0]
            logging.getLogger('info_log').info(
                "shine resume exist with id {}".format(shine_resume_details.get('id'))
                )

        shine_resume_creation_date = datetime.strptime(
            shine_resume_details.get('creation_date'), '%Y-%m-%dT%H:%M:%S'
            ) if shine_resume_details else None

        if oi_resume_creation_date and shine_resume_creation_date:
            oi_resume_creation_date = oi_resume_creation_date.replace(tzinfo=utc)
            shine_resume_creation_date = shine_resume_creation_date.replace(tzinfo=utc)

        if ((oi_resume_creation_date and shine_resume_creation_date) and
                (oi_resume_creation_date < shine_resume_creation_date)) or \
                (shine_resume_creation_date and not oi_resume_creation_date):
            response = ShineCandidateDetail().get_shine_candidate_resume(
                candidate_id=order.candidate_id,
                resume_id=shine_resume_details.get('id')
                )
            if response.status_code == 200:
                content_disposition_header = response.headers.get('Content-Disposition')
                file_name_pos = content_disposition_header.find('filename=')
                file_name = content_disposition_header[file_name_pos + 9:] if file_name_pos != -1\
                    else 'file'
                extention = file_name.split('.')[-1] if file_name else ''

                shine_resume = open(file_name, 'wb+')
                shine_resume.write(response.content)
                shine_resume.seek(0)

                file_name = 'resumeupload_' + str(order_id) + '_' + str(int(random() * 9999)) \
                            + '_' + timezone.now().strftime('%Y%m%d') + '.' + extention

                full_path = '%s/' % str(order.pk)
                if not settings.IS_GCP:
                    if not os.path.exists(settings.RESUME_DIR + full_path):
                        os.makedirs(settings.RESUME_DIR + full_path)
                    dest = open(
                        settings.RESUME_DIR + full_path + file_name, 'wb')
                    for chunk in shine_resume.chunks():
                        dest.write(chunk)
                    dest.close()
                else:
                    GCPPrivateMediaStorage().save(
                        settings.RESUME_DIR + full_path + file_name, shine_resume
                        )
                shine_resume.close()
                old_resume = full_path + file_name

    except Exception as e:
        logging.getLogger('error_log').error('get resume failed from shine  %s' % str(e))

    if not old_resume:
        logging.getLogger('info_log').info("Old Resume Not Found")
        return

    # order items to update old resume in new order ->(order items)
    order_items = OrderItem.objects.filter(id__in=update_resume_oi_ids)

    for oi in order_items:
        oi.oi_resume = old_resume
        last_oi_status = oi.oi_status
        oi.oi_status = 5
        oi.last_oi_status = 3
        oi.save()
        oi.orderitemoperation_set.create(
            oi_status=3,
            oi_resume=oi.oi_resume,
            last_oi_status=last_oi_status,
            assigned_to=oi.assigned_to)
        oi.orderitemoperation_set.create(
            oi_status=oi.oi_status,
            last_oi_status=oi.last_oi_status,
            assigned_to=oi.assigned_to)

    order.auto_upload = True
    order.save()


@task
def upload_Resume_shine(order_item_id):
    from order.models import OrderItem
    from core.api_mixin import ShineCandidateDetail
    import logging
    if not order_item_id:
        return

    order_item = OrderItem.objects.filter(id=order_item_id).first()
    if not order_item:
        return
    candidate_id = order_item.order.candidate_id
    data = {
        'candidate_id': candidate_id,
        'upload_medium': 'direct',
        'upload_source': 'web',
        'resume_source': 7,
        'resume_medium': 7,
        'resume_trigger': 7
    }
    file_path = settings.RESUME_DIR + order_item.oi_draft.name
    response = ShineCandidateDetail().upload_resume_shine(data=data, file_path=file_path)
    if response:
        logging.getLogger('info_log').info("Uploaded to shine")
        order = order_item.order
        order.service_resume_upload_shine = True
        order.save()
        return
    logging.getLogger('error_log').info("Upload to shine failed ")
