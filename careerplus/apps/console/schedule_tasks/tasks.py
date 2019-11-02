#python imports
import logging
import os
import csv
import codecs
import time
import sys,gzip
import datetime
import xlwt

#django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

#local imports
#inter app imports
from shop.models import Product
from order.models import OrderItem
from order.functions import date_diff
from scheduler.models import Scheduler
from linkedin.autologin import AutoLogin
from core.mixins import EncodeDecodeUserData
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from order.functions import date_timezone_convert
from core.mixins import EncodeDecodeUserData

#third party imports
from celery.decorators import task
from dateutil.relativedelta import relativedelta

#Global Constants
User = get_user_model()


@task(name="gen_auto_login_token_task")
def gen_auto_login_token_task(task=None, user=None, next_url=None, exp_days=None):
    f = False
    try:
        up_task = Scheduler.objects.get(pk=task)
        if up_task:
            try:
                up_task.status = 3
                up_task.save()
                upload_path = up_task.file_uploaded.name
                total_rows = 0
                try:
                    user = User.objects.get(pk=user)
                    if not settings.IS_GCP:
                        exist_file = os.path.isfile(
                            settings.MEDIA_ROOT + '/' + upload_path)
                    else:
                        exist_file = GCPPrivateMediaStorage().exists(
                            upload_path)
                    if exist_file:
                        f = True

                        if not settings.IS_GCP:
                            with open(
                                settings.MEDIA_ROOT + '/' + upload_path,
                                'r', encoding='utf-8', errors='ignore') as upload:
                                uploader = csv.DictReader(
                                    upload, delimiter=',', quotechar='"')
                                try:
                                    for i, line in enumerate(uploader):
                                        pass
                                    total_rows = i + 1
                                except Exception as e:
                                    total_rows = 2000
                                    logging.getLogger('error_log').error(
                                        "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})
                        else:
                            with GCPPrivateMediaStorage().open(upload_path) as upload:
                                uploader = csv.DictReader(
                                    codecs.iterdecode(upload, 'utf-8'), delimiter=',', quotechar='"')

                                try:
                                    for i, line in enumerate(uploader):
                                        pass
                                    total_rows = i + 1
                                except Exception as e:
                                    total_rows = 2000
                                    logging.getLogger('error_log').error(
                                        "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})

                            # try:
                            #     for i, line in enumerate(uploader):
                            #         pass
                            #     total_rows = i + 1
                            # except Exception as e:
                            #     total_rows = 2000
                            #     logging.getLogger('error_log').error(
                            #         "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})
                        upload.close()
                        gen_dir = os.path.dirname(upload_path)
                        filename_tuple = upload_path.split('.')
                        extension = filename_tuple[len(filename_tuple) - 1]
                        gen_file_name = str(up_task.pk) + '_GENERATED' + '.' + extension
                        generated_path = gen_dir + '/' + gen_file_name

                        if not settings.IS_GCP:
                            generated_file = open(
                                settings.MEDIA_ROOT + '/' + generated_path, 'w')
                        else:
                            generated_file = GCPPrivateMediaStorage().open(
                                generated_path, 'wb')

                        if not settings.IS_GCP:
                            with open(
                                settings.MEDIA_ROOT + '/' + upload_path,
                                'r', encoding='utf-8', errors='ignore') as upload:
                                uploader = csv.DictReader(
                                    upload, delimiter=',', quotechar='"')
                                fieldnames = uploader.fieldnames
                                fieldnames.append('token')
                                fieldnames.append('auto_login_url')
                                fieldnames.append('error_report')
                                csvwriter = csv.DictWriter(
                                    generated_file, delimiter=',', fieldnames=fieldnames)
                                csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                                count = 0
                                for row in uploader:
                                    try:
                                        email = row.get('email_id', '').strip()
                                        candidate_id = row.get('user_id', '').strip()

                                        try:
                                            if email and candidate_id:
                                                token = AutoLogin().encode(
                                                    email,
                                                    candidate_id,
                                                    days=exp_days)
                                                row['token'] = token
                                                if next_url:
                                                    login_url = reverse('autologin', kwargs={'token': token})
                                                    autologin_url = settings.MAIN_DOMAIN_PREFIX + login_url + '?next=' + next_url
                                                    row['auto_login_url'] = autologin_url
                                                csvwriter.writerow(row)

                                            else:
                                                row['error_report'] = 'email or candidate_id not found'
                                                csvwriter.writerow(row)
                                        except Exception as e:
                                            row['error_report'] = str(e)
                                            csvwriter.writerow(row)
                                    except Exception as e:
                                        row['error_report'] = str(e)
                                        csvwriter.writerow(row)
                                    count = count + 1
                                    if count % 20 == 0:
                                        try:
                                            up_task.percent_done = round((count / float(total_rows))*100, 2)
                                            up_task.save()
                                        except:
                                            pass
                                up_task.file_generated = generated_path
                                up_task.percent_done = 100
                                up_task.status = 2
                                up_task.completed_on = timezone.now()
                                up_task.save()
                                upload.close()
                                generated_file.close()

                        else:
                            with GCPPrivateMediaStorage().open(upload_path) as upload:
                                uploader = csv.DictReader(
                                    codecs.iterdecode(upload, 'utf-8'), delimiter=',', quotechar='"')
                                fieldnames = uploader.fieldnames
                                fieldnames.append('token')
                                fieldnames.append('auto_login_url')
                                fieldnames.append('error_report')
                                csvwriter = csv.DictWriter(
                                    generated_file, delimiter=',', fieldnames=fieldnames)
                                csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                                count = 0
                                for row in uploader:
                                    try:
                                        email = row.get('email_id', '').strip()
                                        candidate_id = row.get('user_id', '').strip()

                                        try:
                                            if email and candidate_id:
                                                token = AutoLogin().encode(
                                                    email,
                                                    candidate_id,
                                                    days=exp_days)
                                                row['token'] = token
                                                if next_url:
                                                    login_url = reverse('autologin', kwargs={'token': token})
                                                    autologin_url = settings.MAIN_DOMAIN_PREFIX + login_url + '?next=' + next_url
                                                    row['auto_login_url'] = autologin_url
                                                csvwriter.writerow(row)

                                            else:
                                                row['error_report'] = 'email or candidate_id not found'
                                                csvwriter.writerow(row)
                                        except Exception as e:
                                            row['error_report'] = str(e)
                                            csvwriter.writerow(row)
                                    except Exception as e:
                                        row['error_report'] = str(e)
                                        csvwriter.writerow(row)
                                    count = count + 1
                                    if count % 20 == 0:
                                        try:
                                            up_task.percent_done = round((count / float(total_rows))*100, 2)
                                            up_task.save()
                                        except:
                                            pass
                                up_task.file_generated = generated_path
                                up_task.percent_done = 100
                                up_task.status = 2
                                up_task.completed_on = timezone.now()
                                up_task.save()
                                upload.close()
                                generated_file.close()
                    else:
                        up_task.status = 1
                        up_task.save()
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})
                    up_task.status = 1
                    up_task.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})
                up_task.status = 1
                up_task.save()
        return f
    except Exception as e:
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'generate auto login token task', 'err': str(e)})
    return f

@task
def generate_discount_report(sid,start_date,end_date,filter_type):
    from shared.utils import DiscountReportUtil
    from datetime import datetime, timedelta

    scheduler_obj = Scheduler.objects.get(id=sid)
    today_date_str = datetime.now().date().strftime("%Y_%m_%d")
    file_name = "scheduler/{}/{}_discount_report.csv".format(today_date_str,sid)
    start_date = datetime.strptime(start_date,"%Y-%m-%dT%H:%M:%S") if isinstance(start_date,str) else start_date
    end_date = datetime.strptime(end_date,"%Y-%m-%dT%H:%M:%S") if isinstance(end_date,str) else end_date

    logging.getLogger('info_log').info(\
        "Disount Report Task Started for {},{},{}".format(sid,start_date,end_date))
    
    util_obj = DiscountReportUtil(start_date=start_date,\
        end_date=(end_date+timedelta(days=1)).replace(hour=0,minute=0,second=0),\
        file_name=file_name,filter_type=filter_type) 
    util_obj.generate_report()
    
    logging.getLogger('info_log').info(\
        "Disount Report Task Complete for {},{},{}".format(sid,start_date,end_date))

    scheduler_obj.file_generated = file_name
    scheduler_obj.percent_done = 100
    scheduler_obj.status = 2
    scheduler_obj.completed_on = datetime.now()
    scheduler_obj.save()


@task(name="generate_encrypted_urls_for_mailer_task")
def generate_encrypted_urls_for_mailer_task(task_id=None,user=None):
    time.sleep(5) # Wait for DB changes to reflect

    scheduler_obj = Scheduler.objects.get(id=task_id)
    upload_path = scheduler_obj.file_uploaded.name
    gen_dir = os.path.dirname(upload_path)
    filename_tuple = upload_path.split('.')
    extension = filename_tuple[len(filename_tuple) - 1]
    gen_file_name = str(task_id) + '_GENERATED' + '.' + extension
    generated_path = gen_dir + '/' + gen_file_name

    if not settings.IS_GCP:
        generated_file = open(settings.MEDIA_ROOT + '/' + generated_path, 'w')
        upload =  open(settings.MEDIA_ROOT + '/' + upload_path,'r', encoding='utf-8', errors='ignore')
        uploader = csv.DictReader(upload, delimiter=',', quotechar='"')
    else:
        upload = GCPPrivateMediaStorage().open(upload_path)
        generated_file = GCPPrivateMediaStorage().open(generated_path, 'wb')
        uploader = csv.DictReader(codecs.iterdecode(upload, 'utf-8'), delimiter=',', quotechar='"')
                                
    fieldnames = uploader.fieldnames
    fieldnames.append('token')

    csvwriter = csv.DictWriter(generated_file, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
    count = 0

    for row in uploader:
        email = row.get('email','').strip()
        name = row.get('name','').strip()
        contact = row.get('contact','').strip()
        row['token'] = EncodeDecodeUserData().encode(email,name,contact) 
        csvwriter.writerow(row)

        count = count + 1

    scheduler_obj.file_generated = generated_path
    scheduler_obj.percent_done = 100
    scheduler_obj.status = 2
    scheduler_obj.completed_on = timezone.now()
    scheduler_obj.save()
    upload.close()
    generated_file.close()


@task(name="generate_product_list")
def gen_product_list_task(task=None, user=None, status=None, vendor=None, product_class=None):
    f = False
    up_task = None
    try:
        up_task = Scheduler.objects.get(pk=task)
        filter_kwargs = {}
        csvfile = None
        if status:
            filter_kwargs.update({"active": status})

        if vendor:
            filter_kwargs.update({"vendor__name": vendor})
        if product_class:
            filter_kwargs.update({"product_class__slug": product_class})
        products_list = list(Product.objects.filter(
            **filter_kwargs).prefetch_related('variation'))
        if up_task:
            up_task.status = 3
            up_task.save()
            total_rows = len(products_list)
            timestr = time.strftime("%Y_%m_%d")
            header_fields = [
                'ID', 'Name', 'Price', 'Visible_On_Site',
                'Visible_On_CRM', 'Type', 'Product_Class', 'Parent',
                'Vendor',
                'Category', 'Study', 'Duration'
            ]
            count = 0
            path = 'scheduler/' + timestr + '/'
            file_name = str(
                up_task.pk) + '_product_list_' + timestr + ".csv"
            if not settings.IS_GCP:
                upload_path = os.path.join(
                    settings.MEDIA_ROOT + '/' + path)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path = upload_path + file_name
                csvfile = open(upload_path, 'w', newline='')
            else:
                upload_path = path + file_name
                csvfile = GCPPrivateMediaStorage().open(upload_path,
                                                        'wb')
            f = True
            csvwriter = csv.DictWriter(
                csvfile, delimiter=',', fieldnames=header_fields)
            csvwriter.writeheader()
            for product in products_list:
                if status == 'True':
                    if product.get_parent() and product.get_parent().active == False:
                        continue
                product_row = {}
                product_row['Name'] = product.get_name
                product_row['ID'] = product.id
                product_row['Price'] = product.get_price()
                product_row['Visible_On_CRM'] = True if product.active else False
                product_row['Visible_On_Site'] = True if (
                product.is_indexable and product.active) else False
                product_row['Type'] = product.get_type_product_display()
                product_row['Product_Class'] = product.product_class.slug if \
                    product.get_product_class() else None
                product_row['Parent'] = product.get_parent().name if \
                    product.get_parent() else None
                product_row['Vendor'] = product.get_vendor()
                product_row['Category'] = ", ".join(
                    [cat.__str__() for cat in product.categories.all()])
                product_row['Study'] = product.get_studymode_db()
                product_row['Duration'] = product.get_duration_db()
                csvwriter.writerow(product_row)
                count = count + 1
                if count % 20 == 0:
                    up_task.percent_done = round(
                        (count / float(total_rows)) * 100, 2)
                    up_task.save()
            up_task.percent_done = 100
            up_task.status = 2
            up_task.completed_on = timezone.now()
            csvfile.close()
            up_task.file_generated = upload_path
            up_task.save()
    except Exception as e:
        up_task.status = 1
        up_task.save()
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'genrate product list task', 'err': str(e)})
    return f


@task(name="generate_compliance_report")
def generate_compliance_report(task_id=None,start_date=None,end_date=None):
    f = False
    up_task = None
    try:
        up_task = Scheduler.objects.get(pk=task_id)
        if not start_date or not end_date:
            up_task.status = 1
            up_task.save()
            return f

        if up_task:
            up_task.status = 3
            up_task.save()
            timestr = time.strftime("%Y_%m_%d")

            oi_list = OrderItem.objects.filter(created__gte=start_date, created__lte=end_date, no_process=False)\
            .exclude(order__status__in=[0, 4, 5])
            total_rows = len(oi_list)

            header_fields = [
                'OrderID', 'CandidateId', 'ItemId', 'ItemCategory',
                'ItemName', 'ItemLevel', 'AllocatedTo', 'ResumeUploadDate',
                'AssignedDate', 'FirstDraftDate', 'TAT', 'WriterBased', 'ClosedDate',\
                'WelcomeCallDate'
            ]
            count = 0
            path = 'scheduler/' + timestr + '/'
            file_name = str(
                up_task.pk) + '_compliance_report_' + timestr + ".csv"
            if not settings.IS_GCP:
                upload_path = os.path.join(
                    settings.MEDIA_ROOT + '/' + path)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path = upload_path + file_name
                csvfile = open(upload_path, 'w', newline='')
            else:
                upload_path = path + file_name
                csvfile = GCPPrivateMediaStorage().open(upload_path,'wb')
            f = True
            csvwriter = csv.DictWriter(
                csvfile, delimiter=',', fieldnames=header_fields)
            csvwriter.writeheader()

            for orderitem in oi_list:
                oi_row = {}
                oi_filter_kwargs = {}
                order_info = orderitem.order
                oi_row['OrderID'] = order_info.id if order_info else 'NA'
                oi_row['CandidateId'] = orderitem.order.candidate_id
                oi_row['ItemId'] = orderitem.id
                orderitem_product = orderitem.product
                if not orderitem_product:
                    continue
                category_list = orderitem_product.categories.all().values_list('name',flat=True)
                category_name = ", ".join(category_list) if category_list else None
                oi_row['ItemCategory'] = category_name if category_name else "N.A"
                oi_row['ItemName'] = orderitem_product.name
                oi_row['ItemLevel'] = orderitem_product.get_exp_db() if orderitem_product.get_exp_db() else "N.A"
                oi_row['AllocatedTo'] = orderitem.assigned_to

                upload_date = orderitem.orderitemoperation_set.filter(oi_status=3,last_oi_status=2).first()
                oi_row['ResumeUploadDate'] = (date_timezone_convert(upload_date.created).strftime('%m/%d/%Y %H:%M:%S')) if\
                    upload_date and upload_date.created else "N.A"

                oi_row['AssignedDate'] = date_timezone_convert(orderitem.assigned_date).strftime('%m/%d/%Y %H:%M:%S') if\
                    orderitem.assigned_date else "N.A"

                if orderitem_product.type_flow == 8:
                    oi_filter_kwargs.update({'oi_status':'44','last_oi_status':'42'})
                else:
                    oi_filter_kwargs.update({'oi_status':'22','last_oi_status':'5'})

                first_draft = orderitem.orderitemoperation_set.filter(**oi_filter_kwargs).first()

                oi_row['FirstDraftDate'] = (date_timezone_convert(first_draft.created).strftime('%m/%d/%Y %H:%M:%S')) if \
                    first_draft and first_draft.created else "N.A"

                oi_row['TAT'] = date_diff(first_draft.created,orderitem.assigned_date) if \
                    first_draft and first_draft.created and orderitem.assigned_date else "N.A"

                oi_row['WriterBased'] = "Yes" if orderitem_product.type_flow in [1,3,8,12,13] else "No"
                orderitem_closed_date = orderitem.orderitemoperation_set.filter(oi_status=4).first()
                oi_row['ClosedDate'] = date_timezone_convert(orderitem_closed_date.created).strftime('%m/%d/%Y %H:%M:%S') if orderitem_closed_date else "Open"
                process_order = order_info.welcomecalloperation_set.filter(wc_cat=21).first()
                oi_row['WelcomeCallDate'] = date_timezone_convert(process_order.created).strftime('%m/%d/%Y %H:%M:%S') if process_order else "N.A"

                csvwriter.writerow(oi_row)
                count = count + 1
                if count % 20 == 0:
                    up_task.percent_done = round(
                        (count / float(total_rows)) * 100, 2)
                    up_task.save()
            up_task.percent_done = 100
            up_task.status = 2
            up_task.completed_on = timezone.now()
            csvfile.close()
            up_task.file_generated = upload_path
            up_task.save()
    except Exception as e:
        up_task.status = 1
        up_task.save()
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'generate compliance list task', 'err': str(e)})
    return f

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

@task(name="generate_pixel_report")
def generate_pixel_report(task=None, url_slug=None, days=None):
    up_task = Scheduler.objects.get(pk=task)
    count = 0
    today = datetime.datetime.now()
    ccount = 0
    days = int(days)
    yesterday = (datetime.datetime.now() - relativedelta(days=days))
    encode_decode_obj = EncodeDecodeUserData()
    output = []
    uniques_dict = {}
    if up_task:
        up_task.status = 3
        up_task.save()
        timestr = time.strftime("%Y_%m_%d")
    header_fields = ['Email', 'Name', 'Contact','Date']
    while yesterday.date() < today.date():
        yesterday_as_str = yesterday.strftime('%Y%m%d')
        file_name = ''
        bucket_name = ''

        if settings.DEBUG:
            file_name = 'uploads/celery-learningcrm/worker.log-' + yesterday_as_str + '.gz'
            bucket_name = 'learningcrm-misc-staging-189607'
        else:
            file_name = 'nginx-access-learning/access.log-' + yesterday_as_str + '.gz'
            bucket_name = 'shine-logs'
        print("Fetching records from {}".format(file_name))
        try:
            if settings.DEBUG:
                content = gzip.open(open(file_name, 'rb')).read()
            else:
                content = gzip.open(GCPPrivateMediaStorage(bucket_name=bucket_name).open(file_name, 'rb')).read()
        except IOError:
            content = b''
            print()
            logging.getLogger('error_log').error('File' + file_name + 'Does not Exist')

        for line in content.decode('utf-8').split('\n'):
            count += 1
            if 'pixel/{}?udata'.format(url_slug) not in line:
                continue
            udata = find_between(line, 'udata=', ' ')
            decrypted_data = encode_decode_obj.decode(udata)
            if decrypted_data and decrypted_data[0]:
                output.append(decrypted_data)
                uniques_dict[decrypted_data[0]] = (decrypted_data[1], decrypted_data[2],yesterday.date())
            ccount += 1

        yesterday = yesterday + datetime.timedelta(days=1)

    path = 'scheduler/' + timestr + '/'
    file_name = str(up_task.pk) + '_pixel_report_' + timestr + ".csv"
    if not settings.IS_GCP:
        upload_path = os.path.join(
            settings.MEDIA_ROOT + '/' + path)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        upload_path = upload_path + file_name
        csvfile = open(upload_path, 'w', newline='')
    else:
        upload_path = path + file_name
        csvfile = GCPPrivateMediaStorage().open(upload_path,'wb')
    csvwriter = csv.DictWriter(
        csvfile, delimiter=',', fieldnames=header_fields)
    csvwriter.writeheader()

    for key, value in uniques_dict.items():
        row = {}
        row['Email'] = key
        row['Name'] = value[0]
        row['Contact'] = value[1]
        row['Date'] = value[2]
        csvwriter.writerow(row)
        
    up_task.percent_done = 100
    up_task.status = 2
    up_task.completed_on = timezone.now()
    csvfile.close()
    up_task.file_generated = upload_path
    up_task.save()

def get_file_obj(file_name):
    if settings.IS_GCP:
        generated_file_obj = GCPPrivateMediaStorage().open(file_name, 'wb')
    else:
        generated_file_obj = open(settings.MEDIA_ROOT + '/' + file_name, 'w')
    return generated_file_obj

def write_row(sheet,data, row=0, start_col=0):
    try:
        for column, value in enumerate(data, start_col):
            sheet.write(row, column, value,)
    except Exception as e:
        logging.getLogger('error_log').error("Failed to write row {}".format(e))
    

@task(name="generate_feedback_report")
def generate_feedback_report(sid,start_date,end_date):
    from order.models import OrderItemFeedbackOperation,OrderItemFeedback
    from datetime import datetime

    logging.getLogger('info_log').info(\
        "Feedback Report Task Started for {},{},{}".format(sid,start_date,end_date))

    scheduler_obj = Scheduler.objects.get(id=sid)
    today_date_str = datetime.now().date().strftime("%Y_%m_%d")
    file_name = "scheduler/{}/{}_discount_report.xls".format(today_date_str,sid)
    file_obj = get_file_obj(file_name)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet 1",cell_overwrite_ok=True) 
    heading = ['Feedback Call Assigned Date Time','CustomerID','Status','Agent Name','LTV','Follow Up Date Time','Item Name',\
                'Feedaback Call Attempted Date Time', 'Satisfaction Status', 'Resolution', 'Payment Date Time']
    write_row(sheet,heading,)
    oi_feedbacks = OrderItemFeedback.objects.filter(created__gte=start_date,created__lte=end_date)
    logging.getLogger('info_log').info(\
        "Total Order Item Feedback Found {}".format(oi_feedbacks.count()))
    
    merged_row_data = {'merge_fields':['assigned_date','candidate_id','status','agent_name','ltv','follow_up']}
    row = 1
    merge_row_start_pos = None
    current_feedback_id = None

    for oi_feedback in oi_feedbacks:
        logging.getLogger('info_log').info(\
            "Adding a row for OI Feedback {}".format(oi_feedback.id))

        if current_feedback_id != oi_feedback.customer_feedback.id:
            if merge_row_start_pos:
                logging.getLogger('info_log').info(\
                    "Merging rows of a column ")
                for index,field in  enumerate(merged_row_data.get('merge_fields',[])):
                    sheet.write_merge(merge_row_start_pos, row - 1, index, index, merged_row_data.get(field,''))

            assigned_date = None
            assigned_date_list = OrderItemFeedbackOperation.objects.filter(customer_feedback=current_feedback_id,\
                                oi_type__in=[3,4]).values_list('added_on',flat=True)
            
            for date in assigned_date_list:
                assigned_date += date.strftime('%d/%m/%Y, %H:%M:%S') + '|'

            assigned_to = oi_feedback.customer_feedback.assigned_to.name if oi_feedback.customer_feedback and \
                        oi_feedback.customer_feedback.assigned_to else ''
            ltv = oi_feedback.customer_feedback.ltv

            follow_up = None
            follow_up_list = OrderItemFeedbackOperation.objects.filter(customer_feedback=current_feedback_id,oi_type=5)\
                        .values_list('added_on',flat=True)
            for date in follow_up_list:
                follow_up += date.strftime('%d/%m/%Y, %H:%M:%S') + '|'

            merged_row_data.update({
                'assigned_date': assigned_date,
                'candidate_id': oi_feedback.customer_feedback.candidate_id, 
                'status': oi_feedback.customer_feedback.status_text,
                'agent_name':assigned_to,
                'ltv':ltv,
                'follow_up':follow_up
            })
            current_feedback_id =  oi_feedback.customer_feedback.id

            merge_row_start_pos = row

        feedback_attempted_date_time = OrderItemFeedbackOperation.objects.filter(customer_feedback=current_feedback_id,\
                                        order_item = oi_feedback.order_item, oi_type=1).first()

        feedback_attempted_date_time = feedback_attempted_date_time.added_on.strftime('%d/%m/%Y, %H:%M:%S') if \
                                        feedback_attempted_date_time else ''
 
        payment_date = oi_feedback.order_item.order.payment_date.strftime('%d/%m/%Y, %H:%M:%S') if oi_feedback.order_item\
                     and oi_feedback.order_item.order and oi_feedback.order_item.order.payment_date else ''
       
        product_name = oi_feedback.order_item.product.name if oi_feedback.order_item and oi_feedback.order_item.product else ''
        excel_row = [
                        None, None, None,None,None, None, product_name, feedback_attempted_date_time\
                        , oi_feedback.category_text,oi_feedback.resolution_text, payment_date
                    ]
        write_row(sheet,excel_row,row)
        row += 1

    if merge_row_start_pos and merge_row_start_pos != row:
        for index,field in  enumerate(merged_row_data.get('merge_fields',[])):
            sheet.write_merge(merge_row_start_pos, row - 1, index, index, merged_row_data.get(field,''))

    if settings.IS_GCP:
        workbook.save(file_obj)
        logging.getLogger('info_log').info("Saved Data to GCP")
    else:
        workbook.save(file_obj.name)
    file_obj.close()
    
    logging.getLogger('info_log').info(\
        "Feedback Report Task Complete for {},{},{}".format(sid,start_date,end_date))

    scheduler_obj.file_generated = file_name
    scheduler_obj.percent_done = 100
    scheduler_obj.status = 2
    scheduler_obj.completed_on = datetime.now()
    scheduler_obj.save()
