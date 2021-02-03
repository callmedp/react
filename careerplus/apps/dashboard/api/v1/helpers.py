import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse


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
        ops = instance.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
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
    options = {}
    oi = instance
    date_created = ''
    if oi.product.type_flow == 1 or  oi.product.type_flow == 12 or oi.product.type_flow == 13:
        for op in ops:
            date_created =op.created
            if (op.oi_status==23 or op.oi_status==25 or op.oi_status==26) and op.draft_counter:
                datalist.append({'date':date_created,'status':'Modifications requested'})
            if op.oi_status == 24 and op.draft_counter == 1:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif op.oi_status == 24 and op.draft_counter < max_draft_limit:
                datalist.append({'date':date_created,'status':'Revised Document is ready'})
            elif op.oi_status == 4 and op.draft_counter == max_draft_limit:
                datalist.append({'date':date_created,'status':'Final Document is ready'})
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True
            elif op.oi_status == 4 and op.draft_counter < max_draft_limit:
                datalist.append({'date':date_created,'status':'Service has been processed and Document is finalized'})
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True


            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif oi.order.auto_upload and not oi.is_assigned and not oi.is_resume_candidate_upload:
                datalist.append({'date':date_created,'status':'Service is under progress'})
                options['upload_resume']=True
            elif op.oi_status == 181:
                datalist.append({'date':date_created,'status':'Waiting For Input'})
            else:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if oi.oi_status == 2 and op.oi_status == 2:
                options['upload_resume']=True
            elif op.oi_status == 24 or op.oi_status == 27:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url'] = reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name

    elif oi.product.type_flow == 8:
        for op in ops:
            date_created =op.created
            if op.oi_status == 2:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif (op.oi_status == 45 or op.oi_status == 47 or op.oi_status == 48)and op.draft_counter:
                datalist.append({'date':date_created,'status':'Modifications requested'})
            if op.oi_status == 46 and op.draft_counter == 1:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif op.oi_status == 46 and op.draft_counter < max_draft_limit:
                datalist.append({'date':date_created,'status':'Revised Document is ready'})
            elif op.oi_status == 4 and op.draft_counter == max_draft_limit :
                datalist.append({'date':date_created,'status':'Document is finalized'})
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True
            elif op.oi_status == 4 and op.draft_counter < max_draft_limit :
                datalist.append({'date':date_created,'status':'Service has been processed and Document is finalized'})
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True
            elif op.oi_status == 181:
                datalist.append({'date':date_created,'status':'Waiting for input'})

            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif oi.order.auto_upload and not oi.is_assigned and not oi.is_resume_candidate_upload:
                datalist.append({'date':date_created,'status':'Service is under progress'})
                options['upload_resume']=True
            else:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
                datalist.append({'date':date_created,'status':'Service is under progress'})
            # if op.oi_status == 2 and oi.oi_status == 2:
            #     options['upload_resume']=True
            # elif op.oi_status == 46 or op.oi_status == 27:
            #     options['Download']=True
            #     options['oi.pk']=oi.pk
            #     options['op.pk']=op.pk
            #     options['download_url']= reverse("linkedin-draf-download",kwargs={'order_item':oi.pk,'op_id':op.pk})

    elif oi.product.type_flow == 3:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_draft:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name
            elif op.oi_status == 2 and op.oi_status == 2:
                options['upload_resume']=True
            elif op.oi_status == 4:
                datalist.append({'date':date_created,'status':'Service has been processed and Final document is ready'})
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True
            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif oi.order.auto_upload and not oi.is_assigned and not oi.is_resume_candidate_upload:
                datalist.append({'date':date_created,'status':'Service is under progress'})
                options['upload_resume']=True
            else:
                datalist.append({'date':date_created,'status':'Service is under progress'})

    elif oi.product.type_flow == 2 or  oi.product.type_flow == 14:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_status == 5:
                if  oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and not op.neo_mail_sent and not op.updated_from_trial_to_regular:
                    options['BoardOnNeo'] = True
                if  oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and op.neo_mail_sent:
                    options['neo_mail_sent']=True
                if oi.product.type_flow == 2 and oi.product.vendor.slug == 'neo'  and op.updated_from_trial_to_regular:
                    options['updated_from_trial_to_regular'] = True
            elif op.oi_status == 6 or op.oi_status == 4 and op.oi_draft.name:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']=reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name
            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})

    elif oi.product.type_flow == 4:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if oi.oi_status == 2 and not oi.oi_resume:
                options['upload_resume']=True
            elif op.oi_status == 6:
                options['Download_credential']=True
                options['download_url']=reverse("console:profile_credentials",kwargs={'oi':oi.pk})
                options['oi.pk']=oi.pk

            elif op.oi_status == 4:
                options['Download_credential']=True
                if not oi.order.service_resume_upload_shine:
                    options['UploadResumeToShine'] = True
                elif op.oi_status == 61:
                    datalist.append({'date':date_created,'status':op.get_user_oi_status})
                elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                    datalist.append({'date':date_created,'status':op.get_user_oi_status})
                elif oi.order.auto_upload and not oi.is_assigned and not oi.is_resume_candidate_upload:
                    datalist.append({'date':date_created,'status':'Service is under progress'})
                    options['upload_resume']=True

    elif oi.product.type_flow == 5:
        if oi.product.sub_type_flow == 502:
                custom_ops=oi.get_item_operations()
                if custom_ops is not None:
                    for op in custom_ops:
                        if op:
                            date_created =op.created
                            if op.oi_status == 31:
                                datalist.append({'date':date_created,'status':'Service is Under Progress'})
                            else:
                                datalist.append({'date':date_created,'status':op.get_user_oi_status})
        else:
            for op in ops:
                date_created =op.created
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
                if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                    options['upload_resume']=True
                elif op.oi_status == 4 or op.oi_status == 28 or op.oi_status == 29 or op.oi_status == 34 or op.oi_status == 35:
                    datalist.append({'date':date_created,'status':'Service has been processed'})
                elif op.oi_status == 61 or op.oi_status == 36 or op.oi_status == 37 or op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                    datalist.append({'date':date_created,'status':op.get_user_oi_status})
                else:
                    datalist.append({'date':date_created,'status':'Service is under progress'})

    elif oi.product.type_flow == 6:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_draft and op.oi_draft.name:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name
    elif oi.product.type_flow == 7 or oi.product.type_flow == 15:
        for op in ops:
            date_created =op.created
            datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if oi.oi_status == 2 and not oi.oi_resume and op.oi_status == 2:
                options['upload_resume']=True
                options['uploaded_resume_will_be_boosted']=True
            elif op.oi_draft.name:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name

    elif oi.product.type_flow == 9:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_status == 141:
                datalist.append({'date':date_created,'status':'Your profile to be shared with interviewer is pending'})
                options['complete_profile']=True
            elif op.oi_status == 142:
                datalist.append({'date':date_created,'status':'Service is under progress'})
                options['edit_your_profile']=True
            elif op.oi_status == 143:
                datalist.append({'date':date_created,'status':'Service has been expired'})
            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})


    elif oi.product.type_flow == 10:
        for op in ops:
            date_created =op.created
            # datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_status == 5:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            elif op.oi_status == 4:
                datalist.append({'date':date_created,'status':'Service has been processed'})
                if op.oi_draft.name:
                    options['Download']=True
                    options['order_pk']=oi.order.pk
                    options['oi_draftname']=op.oi_draft.name
                    options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name
            elif op.oi_status == 161 or op.oi_status == 162 or op.oi_status == 163:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_status == 101:
                datalist.append({'date':date_created,'status':op.get_user_oi_status})
                options['take_test']=True
                options['auto_login_url'] = oi.autologin_url
            elif op.oi_draft and op.oi_draft.name:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name
    
    elif oi.product.type_flow == 16 and oi.product.sub_type_flow == 1602:
        if oi.oi_status == 5:
            options['take_test']=True
            datalist.append({'date':date_created,'status':op.get_user_oi_status})
        elif op.oi_status == 4:
            datalist.append({'date':date_created,'status':op.get_user_oi_status})
    elif oi.product.type_flow == 17:
        # resumetemplate option to be shown on frontend if editTemplate option is True
        options['edit_template']=True 
        for op in ops:
            date_created =op.created
            datalist.append({'date':date_created,'status':op.get_user_oi_status})
            if op.oi_status == 101:
                options['take_test']=True
            elif op.oi_draft and op.oi_draft.name:
                options['Download']=True
                options['order_pk']=oi.order.pk
                options['oi_draftname']=op.oi_draft.name
                options['download_url']= reverse("dashboard:dashboard-resumedownload",kwargs={'pk':oi.order.pk})+'?path='+op.oi_draft.name

    if oi.oi_status == 28 or oi.oi_status == 34 or oi.oi_status == 35:
        if oi.days_left_oi_product > 0 and oi.product.is_pause_service:
            if oi.service_pause_status:
                options['pause_service'] = True
            else:
                options['resume_service'] = True

    if oi.product.type_flow == 5:
        if oi.oi_status == 28 or oi.oi_status == 34 or oi.oi_status == 35:
            if oi.days_left_oi_product >= 0:
                options['day_remaining']=oi.days_left_oi_product 
    
    if oi.oi_status == 24 or instance.oi_status==46:
        options['accept_reject']=True

    if oi.oi_status == 4 and not instance.user_feedback:
        options['your_feedback']=True

    return {
            'date_created':date_created,
            'datalist':datalist,
            'options':options
            }