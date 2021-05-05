import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from review.models import Review
from core.common import APIResponse
from shop.models import Product
from rest_framework import status
from django.db.models import Avg
from decimal import Decimal


def offset_paginator(page, data, **kwargs):
    custom_size = kwargs.get("size", None)
    if custom_size:
        try:
            size = int(custom_size)
        except ValueError:
            size = settings.PAGINATOR_PAGE_SIZE
    else:
        size = settings.PAGINATOR_PAGE_SIZE

    try:
        page = int(page)
        if page <= 0:
            page = 1
    except ValueError:
        page = 1
    if isinstance(data, list):
        total = len(data)
    else:
        total = data.count()
    count = math.ceil(total / size)
    if count == 0:
        page = 1
    else:
        if page > count:
            page = count
    offset = page * size - size
    return {"data": data[offset : size * page], "total": total,"total_pages":count,"current_page":page}

def get_courses_detail(instance):
    max_draft_limit=settings.DRAFT_MAX_LIMIT

    datalist = []
    options = {}
    oi = instance
    date_created = ''
    current_status={}
    
    if oi.product.type_flow == 1 or  oi.product.type_flow == 12 or oi.product.type_flow == 13:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status==2:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
        elif (oi.oi_status==23 or oi.oi_status==25 or oi.oi_status==26) and oi.draft_counter:
            current_status.update({'status':'Modifications requested'})
        elif oi.oi_status == 24 and oi.draft_counter == 1:
            current_status.update({'status':'Document is ready'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})

        elif oi.oi_status == 24 and oi.draft_counter < max_draft_limit:
            current_status.update({'status':'Revised Document is ready'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})

        elif oi.oi_status == 4 and oi.draft_counter == max_draft_limit:
            current_status.update({'status':'Final Document is ready'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine':True})

        elif oi.oi_status == 4 and oi.draft_counter < max_draft_limit:
            current_status.update({'status':'Service has been processed and Document is finalized'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine':True})

        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.waiting_for_input:
             current_status.update({'status':'Waiting for input'})
        elif oi.order.auto_upload and not oi.is_assigned() and not oi.is_resume_candidate_upload:
            current_status.update({'status':'Service is under progress'})
            current_status.update({'upload_resume':True})
        else:
            current_status.update({'status':'Service is under progress'})

    elif oi.product.type_flow == 8:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 2:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
        elif (oi.oi_status == 45 or oi.oi_status == 47 or oi.oi_status == 48)and oi.draft_counter:
            current_status.update({'status':'Modifications requested'})
        if oi.oi_status == 46 and oi.draft_counter == 1:
            current_status.update({'status':'Document is ready'})
            current_status.update({'download_url':reverse("dashboard-draf-download",kwargs={'order_item':oi.pk})})
        elif oi.oi_status == 46 and oi.draft_counter < max_draft_limit:
            current_status.update({'status':'Revised Document is ready'})
            current_status.update({'download_url':reverse("dashboard-draf-download",kwargs={'order_item':oi.pk})})
        elif oi.oi_status == 4 and oi.draft_counter == max_draft_limit :
            current_status.update({'status':'Final Document is ready'})
            current_status.update({'download_url':reverse("dashboard-draf-download",kwargs={'order_item':oi.pk})})

            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine':True})
        elif oi.oi_status == 4 and oi.draft_counter < max_draft_limit :
            current_status.update({'status':'Service has been processed and Document is finalized'})
            current_status.update({'download_url':reverse("dashboard-draf-download",kwargs={'order_item':oi.pk})})

            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine':True})
        elif oi.waiting_for_input:
            current_status.update({'status':'Waiting for input'})

        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.order.auto_upload and not oi.is_assigned() and not oi.is_resume_candidate_upload:
            current_status.update({'status':'Service is under progress'})
            current_status.update({'upload_resume':True})
        else:
            current_status.update({'status':'Service is under progress'})

    elif oi.product.type_flow == 3:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 2:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
        elif oi.oi_status == 4:
            current_status.update({'status':'Service has been processed and Final document is ready'})
            current_status.update({'download_url': reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine':True})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.order.auto_upload and not oi.is_assigned() and not oi.is_resume_candidate_upload:
            current_status.update({'status':'Service is under progress'})
            current_status.update({'upload_resume':True})
        else:
            current_status.update({'status':'Service is under progress'})

    elif oi.product.type_flow == 2 or  oi.product.type_flow == 14:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 5:
            current_status.update({'status':oi.get_user_oi_status})
            if  oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and not oi.neo_mail_sent and not oi.updated_from_trial_to_regular:
                current_status.update({'BoardOnNeo':True})
            if  oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and oi.neo_mail_sent:
                current_status.update({'neo_mail_sent':True})
            if oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and oi.updated_from_trial_to_regular:
                current_status.update({'updated_from_trial_to_regular':True})
        elif oi.oi_status == 6:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
        elif oi.waiting_for_input:
            current_status.update({'status':'Waiting for input'})
        elif oi.oi_status == 4:
            current_status.update({'status':'Service has been processed'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})

    elif oi.product.type_flow == 4:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 2:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
        # elif oi.oi_status == 6:
        #     current_status.update({'status':oi.get_user_oi_status})
        #     current_status.update({'download_url':reverse("console:profile_credentials",kwargs={'oi':oi.pk})})

        elif oi.oi_status == 4:
            current_status.update({'status':'Service has been processed'})
            # current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
            current_status.update({'download_credentials_url':reverse("console:profile_credentials",kwargs={'oi':oi.pk})})

            if not oi.order.service_resume_upload_shine:
                current_status.update({'UploadResumeToShine': True})
        elif oi.oi_status == 61:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163 or oi.oi_status == 164:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.waiting_for_input:
            datalist.append({'date':date_created,'status':'Waiting for input'})
        elif oi.order.auto_upload and not oi.is_assigned() and not oi.is_resume_candidate_upload:
            current_status.update({'status':'Service is under progress'})
            current_status.update({'upload_resume':True})
        else:
            current_status.update({'status':'Service is under progress'})

    elif oi.product.type_flow == 5:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 2:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
        elif oi.oi_status == 4 or oi.oi_status == 28 or oi.oi_status == 29 or oi.oi_status == 34 or oi.oi_status == 35:
            current_status.update({'status':'Service has been processed'})
        elif oi.oi_status == 61 or oi.oi_status == 36 or oi.oi_status == 37 or oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163 or oi.oi_status == 164 or oi.oi_status==6:
            current_status.update({'status':oi.get_user_oi_status})
        else:
            current_status.update({'status':'Service is under progress'})

    elif oi.product.type_flow == 6:
        date_created =oi.created.strftime("%d %b %y")
        # datalist.append({'date':date_created,'status':oi.get_user_oi_status})
        if oi.oi_status ==81:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
        elif oi.oi_status ==4:
            current_status.update({'status':'Service has been processed'})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
        else:
            current_status.update({'status':oi.get_user_oi_status})

    elif oi.product.type_flow == 7 or oi.product.type_flow == 15:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 2 :
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'upload_resume':True})
            current_status.update({'uploaded_resume_will_be_boosted':True})
        else:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})

    elif oi.product.type_flow == 9:
        op_status = oi.get_roundone_status()
        date_created =oi.created.strftime("%d %b %y")
        if op_status == 141:
            current_status.update({'status':'Your profile to be shared with interviewer is pending'})
            current_status.update({'complete_profile':True})
        elif oi.oi_status == 142:
            current_status.update({'status':'Service is under progress'})
            current_status.update({'edit_your_profile':True})
        elif oi.oi_status == 143:
            current_status.update({'status':'Service has been expired'})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
            datalist.append({'date':date_created,'status':oi.get_user_oi_status})

    elif oi.product.type_flow == 10:
        date_created =oi.created.strftime("%d %b %y")
        # datalist.append({'date':date_created,'status':oi.get_user_oi_status})
        if oi.oi_status == 5:
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.oi_status == 4:
            current_status.update({'status':'Service has been processed'})
            if oi.oi_draft.name:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})
        elif oi.oi_status == 161 or oi.oi_status == 162 or oi.oi_status == 163:
            current_status.update({'status':oi.get_user_oi_status})
        if oi.oi_status == 101:
            current_status.update({'status':oi.get_user_oi_status})
            current_status.update({'take_test':True})
            current_status.update({'auto_login_url': oi.autologin_url})
    
    elif oi.product.type_flow == 16 and oi.product.sub_type_flow == 1602:
        date_created =oi.created.strftime("%d %b %y")
        if oi.oi_status == 5:
            current_status.update({'take_test':True})
            current_status.update({'auto_login_url': oi.autologin_url})
            current_status.update({'status':oi.get_user_oi_status})
        elif oi.oi_status == 4:
            current_status.update({'status':oi.get_user_oi_status})

    elif oi.product.type_flow == 17:
        # resumetemplate option to be shown on frontend if editTemplate option is True
        current_status.update({'edit_template':True})
        date_created =oi.created.strftime("%d %b %y")
        current_status.update({'status':oi.get_user_oi_status})
        if oi.oi_status == 101:
            current_status.update({'take_test':True})
        elif oi.oi_draft and oi.oi_draft.name:
            current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+oi.oi_draft.name})

    if oi.oi_status == 28 or oi.oi_status == 34 or oi.oi_status == 36 or oi.oi_status == 35:
        if oi.days_left_oi_product > 0 and oi.product.is_pause_service:
            if oi.service_pause_status():
                current_status.update({'pause_service':True})
            else:
                current_status.update({'resume_service': True})

    if oi.product.type_flow == 5:
        if oi.oi_status == 28 or oi.oi_status == 34 or oi.oi_status == 35:
            if oi.days_left_oi_product >= 0:
                current_status.update({'day_remaining':oi.days_left_oi_product})
    
    if oi.oi_status == 24 or oi.oi_status==46:
        current_status.update({'accept_reject':True})

    if oi.oi_status == 4 and not oi.user_feedback:
        current_status.update({'your_feedback':True})

    return current_status


def get_history(instance):
    max_draft_limit=settings.DRAFT_MAX_LIMIT
    ops=[]

    if instance.product.type_flow in [1, 12, 13]:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163, 164, 181])
    elif instance.product.vendor.slug == 'neo':
        ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 33, 4, 161, 162, 163, 164])
    elif instance.product.type_flow in [2, 14]:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163, 164])
    elif instance.product.type_flow == 3:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163, 164])
    elif instance.product.type_flow == 4:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
    elif instance.product.type_flow == 5:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 36, 37, 61, 161, 162, 163, 164])
    elif instance.product.type_flow == 6:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
    elif instance.product.type_flow in [7, 15]:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163, 164])
    elif instance.product.type_flow == 8:
        oi_status_list = [2, 49, 5, 46, 48, 27, 4, 161, 162, 163, 181, 164]
        ops = instance.orderitemoperation_set.filter(oi_status__in=oi_status_list)
    elif instance.product.type_flow == 10:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163, 164])
    elif instance.product.type_flow == 16:
        ops = instance.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])
    
    datalist = []
    oi = instance
    date_created = ''
    current_status ={}   
    if oi.product.type_flow == 1 or  oi.product.type_flow == 12 or oi.product.type_flow == 13:
        for op in ops:
            current_status ={}
            date_created =op.created.strftime("%d %b %y")
            if op.oi_status == 24 and op.draft_counter == 1:
                current_status = {'date':date_created,'status':op.get_user_oi_status}
            elif op.oi_status == 24 and op.draft_counter < max_draft_limit:
                current_status = {'date':date_created,'status':'Revised Document is ready'}
            elif op.oi_status == 24 and op.draft_counter == max_draft_limit:
                current_status ={'date':date_created,'status':'Final Document is ready'}
            elif op.oi_status == 181:
                current_status ={'date':date_created,'status':'Waiting For Input'}
            else:
                current_status ={'date':date_created,'status':op.get_user_oi_status}
            if oi.oi_status == 2 and op.oi_status == 2:
                current_status.update({'upload_resume':True})
            elif op.oi_status == 24 or op.oi_status == 27:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 8:
        for op in ops:
            current_status ={}
            date_created =op.created.strftime("%d %b %y")
            if op.oi_status == 46 and op.draft_counter == 1:
                current_status = {'date':date_created,'status':op.get_user_oi_status}
            elif op.oi_status == 46 and op.draft_counter < max_draft_limit:
                current_status ={'date':date_created,'status':'Revised Document is ready'}
            elif op.oi_status == 4:
                current_status ={'date':date_created,'status':'Document is finalized'}
            elif op.oi_status == 181:
                current_status ={'date':date_created,'status':'Waiting for input'}
            else:
                current_status = {'date':date_created,'status':op.get_user_oi_status}

            if op.oi_status == 2 and oi.oi_status == 2:
                current_status.update({'upload_resume':True})
            elif op.oi_status == 46 or op.oi_status == 27:
                current_status.update({'download_url':reverse("linkedin-draf-download",kwargs={'order_item':oi.pk,'op_id':op.pk})})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 3:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status = {'date':date_created,'status':op.get_user_oi_status}
            if op.oi_draft:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name})
            elif oi.oi_status == 2 and op.oi_status == 2:
                current_status.update({'upload_resume':True})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 2 or  oi.product.type_flow == 14:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status = {'date':date_created,'status':op.get_user_oi_status}
            if op.oi_status == 6:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 4:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status = {'date':date_created,'status':op.get_user_oi_status}
            if oi.oi_status == 2 and not oi.oi_resume:
                current_status.update({'upload_resume':True})
            elif op.oi_status == 6:
                current_status.update({'download_credentials_url':reverse("console:profile_credentials",kwargs={'oi':oi.pk})})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 5:

        if oi.product.sub_type_flow == 502:
                custom_ops=oi.get_item_operations()
                if custom_ops is not None:
                    current_status={}
                    for op in custom_ops:
                        if op:
                            date_created =op.created.strftime("%d %b %y")
                            if op.oi_status == 31:
                                current_status={'date':date_created,'status':'Service is Under Progress'}
                            else:
                                current_status={'date':date_created,'status':op.get_user_oi_status}
                        if current_status:
                            datalist.append(current_status)
        else:
            for op in ops:
                current_status={}
                date_created =op.created.strftime("%d %b %y")
                current_status={'date':date_created,'status':op.get_user_oi_status}
                if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                    current_status.update({'upload_resume':True})
                if current_status:
                        datalist.append(current_status)

    elif oi.product.type_flow == 6:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status={'date':date_created,'status':op.get_user_oi_status}
            if op.oi_draft:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 7 or oi.product.type_flow == 15:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status={'date':date_created,'status':op.get_user_oi_status}
            if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                current_status.update({'upload_resume':True})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 9:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status={'date':date_created,'status':op.get_user_oi_status}
            if op.oi_status == 141:
                current_status.update({'complete_profile':True})
            elif op.oi_status == 142:
                current_status.update({'edit_profile':True})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 10 or oi.product.type_flow == 17:
        for op in ops:
            current_status={}
            date_created =op.created.strftime("%d %b %y")
            current_status={'date':date_created,'status':op.get_user_oi_status}
            if op.oi_status == 101:
                current_status.update({'take_test':True})
            elif op.oi_draft:
                current_status.update({'download_url':reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name})
            if current_status:
                datalist.append(current_status)

    elif oi.product.type_flow == 16 and oi.product.sub_type_flow == 1602:
        for op in ops:
            current_status = {}
            date_created = op.created.strftime("%d %b %y")
            current_status = {'date': date_created, 'status': op.get_user_oi_status}
            if op.oi_status == 5:
                current_status.update({'take_test': True, 'status': op.get_user_oi_status, 'auto_login_url': oi.autologin_url})
            elif op.oi_status == 4:
                current_status.update({'status': op.get_user_oi_status})
            if current_status:
                datalist.append(current_status)

    return datalist
    
def get_review_details(product, candidate_id):
    product_type = ContentType.objects.get(
        app_label='shop', model='product')
    prd_list = []
    if product.type_product in [0, 2, 4, 5]:
        prd_list = [product.pk]
    elif product.type_product == 1:
        prd_id = product.variation.filter(
            siblingproduct__active=True,
            active=True).values_list('id', flat=True)
        prd_list = list(prd_id)
        prd_list.append(product.pk)
    elif product.type_product == 3:
        prd_id = product.childs.filter(
            childrenproduct__active=True,
            active=True).values_list('id', flat=True)
        prd_list = list(prd_id)
        prd_list.append(product.pk)
    review_list = Review.objects.filter(
        content_type__id=product_type.id,status=1,
        object_id__in=prd_list, user_id=candidate_id)
    avg_rating = review_list.aggregate(Avg('average_rating'))['average_rating__avg'] if len(review_list)>0 else 0
    return {'review_list':review_list,'avg_rating':avg_rating}

def get_ratings(avg_rating):
        pure_rating = int(avg_rating)
        decimal_part = avg_rating - pure_rating
        final_score = ['*' for i in range(pure_rating)]
        rest_part = int(Decimal(5.0) - Decimal(avg_rating))
        res_decimal_part = Decimal(5.0) - Decimal(avg_rating) - Decimal(rest_part)
        if decimal_part >= 0.75:
            final_score.append("*")
        elif decimal_part >= 0.25:
            final_score.append("+")
        if res_decimal_part >= 0.75:
            final_score.append('-')
        for i in range(rest_part):
            final_score.append('-')
        return final_score
