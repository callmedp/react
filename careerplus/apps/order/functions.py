import logging
import json
import requests
from django.conf import settings
from emailers.email import SendMail
from dateutil import relativedelta
from emailers.email import SendMail
from emailers.sms import SendSMS
from django.utils import timezone
from api.config import LOCATION_MAPPING, INDUSTRY_MAPPING, SALARY_MAPPING
from shop.models import ProductUserProfile
from shine.core import ShineCandidateDetail 

def update_initiat_orderitem_sataus(order=None):
    if order:
        orderitems = order.orderitems.filter(
            no_process=False).select_related('order', 'product', 'partner')

        # update initial status
        for oi in orderitems:
            if oi.product.type_flow in [1, 3, 12, 13]:
                last_oi_status = oi.oi_status
                oi.oi_status = 2
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow in [2, 14]:
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 4:
                if oi.order.orderitems.filter(product__type_flow=12, no_process=False).exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)
                else:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 2
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 5:
                if oi.order.orderitems.filter(product__type_flow=1, no_process=False).exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)
                else:
                    last_oi_status = oi.oi_status
                    if oi.product.sub_type_flow == 502:
                        oi.oi_status = 31
                    else:
                        oi.oi_status = 2
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 6:
                last_oi_status = oi.oi_status
                oi.oi_status = 82
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow in [7, 15]:
                depending_ois = order.orderitems.filter(
                    product__type_flow=1, no_process=False)

                if depending_ois.exists():
                    last_oi_status = oi.oi_status
                    oi.oi_status = 61
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)
                else:
                    last_oi_status = oi.oi_status
                    oi.oi_status = 2
                    oi.last_oi_status = last_oi_status
                    oi.save()
                    oi.orderitemoperation_set.create(
                        oi_status=oi.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 10:
                last_oi_status = oi.oi_status
                oi.oi_status = 101
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

            elif oi.product.type_flow == 16:
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.wc_cat = 21
                oi.wc_sub_cat = 41
                oi.wc_status = 41
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)

        # for assesment if no orderitems other than assesment present
        # then make welcome call done and update welcome call statuses.
        oi = order.orderitems.exclude(product__type_flow=16)

        if not oi.exists():
            order.wc_cat = 21
            order.wc_sub_cat = 41
            order.wc_status = 41
            order.welcome_call_done = True
            order.save()
            order.welcomecalloperation_set.create(
                wc_cat=order.wc_cat,
                wc_sub_cat=order.wc_sub_cat,
                message='Done automatically, Only Assesment items present',
                wc_status=order.wc_status,
                assigned_to=order.assigned_to
            )




def get_upload_path_order_invoice(instance, filename):
    return "invoice/order/{order_id}/{filename}".format(
        order_id=instance.id, filename=filename)


def create_short_url(login_url={}):
    short_url = {}
    data = {}
    data['url'] = login_url.get('upload_url')
    
    headers = {"Authorization":"Token {}".format(settings.URL_SHORTENER_AUTH_DICT.get('access_token','')),
            "Content-Type":"application/json",
            "Accept":"application/json"}

    response = requests.post(
        url=settings.URL_SHORTENER_AUTH_DICT.get('end_point',''), data=json.dumps(data),headers=headers)

    if response.ok:
        resp = response.json()
        short_url.update({'url': resp.get('uri')})
    
    return short_url

def send_email(to_emails, mail_type, email_dict, status=None, oi=None):
    try:
        SendMail().send(to_emails, mail_type, email_dict)
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.filter(pk=oi)
            for oi_item in obj:
                to_email = to_emails[0] if to_emails else oi_item.order.get_email()
                oi_item.emailorderitemoperation_set.create(
                    email_oi_status=status, to_email=to_email,
                    status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "email sending failed %s - %s - %s" % (str(to_emails), str(e), str(mail_type)))


def send_email_from_base(subject=None, body=None, to=[], headers=None, oi=None, status=None):
    try:
        SendMail().base_send_mail(subject, body, to=[], headers=None, bcc=[settings.DEFAULT_FROM_EMAIL])
        if oi:
            from order.models import OrderItem
            obj = OrderItem.objects.get(pk=oi)
            to = to[0] if to else obj.order.get_email()
            obj.emailorderitemoperation_set.create(
                email_oi_status=status,
                to_email=to, status=1)
    except Exception as e:
        logging.getLogger('error_log').error(
            "%s - %s - %s" % (str(to), str(e)))


def date_timezone_convert(date=None):
    from pytz import timezone
    if not date:
        return 'N.A'
    return date.astimezone(timezone(settings.TIME_ZONE))



def date_diff(date1,date2):
    datediff = relativedelta.relativedelta(date1, date2)
    # return str(datediff.days) + '-days-' + str(datediff.hours)+'-hours-'\
    #        +str(datediff.minutes)+'-minutes'
    #only returning days difference
    return str(datediff.days)


def close_resume_booster_ois(ois_to_update):
    from order.models import OrderItem
    for oi in OrderItem.objects.filter(id__in=ois_to_update):
        last_oi_status = oi.oi_status
        oi.oi_status = 4
        oi.last_oi_status = 6
        oi.closed_on = timezone.now()
        oi.save()
        # status as tuple (status, last_status)
        # if order is in service under progress create three operation
        # resume boosted, service progress and order closed.
        # else create single operation resume boosted.
        if last_oi_status == 5:
            oi_statuses = ((62, last_oi_status), (6, 62), (4, 6))
        else:
            oi_statuses = ((62, last_oi_status),)

        for status, last_status in oi_statuses:
            oi.orderitemoperation_set.create(
                oi_status=status,
                last_oi_status=last_status,
                assigned_to=oi.assigned_to,
            )
        oi.emailorderitemoperation_set.create(email_oi_status=92)

def process_jobs_on_the_move(obj):
    # create jobs on the move profile after welcome call is done.
    if ((obj.wc_cat == 21 and obj.wc_sub_cat in [41, 42]) or (obj.wc_cat == 22 and obj.wc_cat == 63)) and \
            not getattr(obj, 'whatsapp_profile_orderitem', False):
        from order.models import OrderItem
        other_jobs_on_the_move = OrderItem.objects.filter(
            order__status__in=[1, 3],
            product__type_flow__in=[5],
            oi_status__in=[31, 32],
            product__sub_type_flow=502,
        ).exclude(whatsapp_profile_orderitem=None).first()

        desired_industry, desired_location, desired_salary, current_salary = '', '' ,'', ''

        if other_jobs_on_the_move:
            desired_industry = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_industry
            desired_location = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_location
            desired_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.desired_salary
            current_salary = other_jobs_on_the_move.whatsapp_profile_orderitem.current_salary
        else:
            resp_status = ShineCandidateDetail().get_candidate_detail(email=obj.order.email, shine_id=None)

            if resp_status and 'desired_job' in resp_status:
                candidate_data = resp_status['desired_job'][0]

                # Get canidate location
                candidate_location = candidate_data['candidate_location']
                desired_location = ','.join([LOCATION_MAPPING.get(loc, '') for loc in candidate_location])

                # Get candidate industry
                candidate_industry = candidate_data['industry']
                desired_industry = ','.join([INDUSTRY_MAPPING.get(ind, '') for ind in candidate_industry])

                # Get desired salary
                maximum_salary = candidate_data['maximum_salary']
                expected_min_salary = ','.join([SALARY_MAPPING.get(l, 'N.A') for l in maximum_salary])

                minimum_salary = candidate_data['minimum_salary']
                expected_max_salary = ','.join([SALARY_MAPPING.get(l, 'N.A') for l in minimum_salary])

                desired_salary = expected_min_salary + ' - ' + expected_max_salary

                # get current salary
                salary_in_lakh = resp_status['workex'][0]['salary_in_lakh']
                salary_in_thousand = resp_status['workex'][0]['salary_in_thousand']
                current_salary = str(salary_in_lakh) + 'Lakh ' + str(salary_in_thousand) + 'Thousand'

        ProductUserProfile.objects.create(
            order_item=obj,
            contact_number=obj.order.mobile,
            desired_industry=desired_industry,
            desired_location=desired_location,
            desired_salary=desired_salary,
            current_salary=current_salary
        )
