#python imports
import logging
import os
import csv
import codecs
import time

#django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

#local imports

#inter app imports
from shop.models import Product
from scheduler.models import Scheduler
from linkedin.autologin import AutoLogin
from core.mixins import EncodeDecodeUserData
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage

#third party imports
from celery.decorators import task

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


@task(name="generate_encrypted_urls_for_mailer_task")
def generate_encrypted_urls_for_mailer_task(task_id=None,user=None):
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
    try:
        up_task = Scheduler.objects.get(pk=task)
        csvfile = None
        products_list = Product.objects.all()
        if vendor:
            products_list = products_list.filter(vendor__name=vendor)
        if status:
            variation_parent_products = products_list.filter(type_product=1).exclude(active=status)
            products_to_exclude = [product.id for product in variation_parent_products]
            products_to_exclude = products_to_exclude + [
                product.id for pr in variation_parent_products for product in pr.variation.all()
            ]
            products_list = products_list.filter(active=status).exclude(id__in=products_to_exclude)
        if product_class:
            products_list = products_list.filter(product_class__slug=product_class)
        if up_task:
            try:
                up_task.status = 3
                up_task.save()
                total_rows = products_list.count()
                try:
                    user = User.objects.get(pk=user)
                    timestr = time.strftime("%Y_%m_%d")
                    header_fields = [
                        'ID', 'Name', 'Price', 'Visible_On_Site',
                        'Visible_On_CRM', 'Type', 'Product_Class', 'Parent', 'Vendor',
                        'Category', 'Study', 'Duration'
                    ]
                    count = 0
                    path = 'scheduler/' + timestr + '/'
                    file_name = str(up_task.pk) + '_product_list_' + timestr + ".csv"
                    if not settings.IS_GCP:
                        upload_path = os.path.join(settings.MEDIA_ROOT + '/' +path)
                        if not os.path.exists(upload_path):
                            os.makedirs(upload_path)
                        upload_path = upload_path + file_name
                        csvfile = open(upload_path, 'w', newline='')
                    else:
                        upload_path = path + file_name
                        csvfile = GCPPrivateMediaStorage().open(upload_path, 'wb')
                    f = True
                    csvwriter = csv.DictWriter(
                        csvfile, delimiter=',', fieldnames=header_fields)
                    csvwriter.writeheader()
                    for product in products_list:
                        product_row = {}
                        product_row['Name'] = product.get_name
                        product_row['ID'] = product.id
                        product_row['Price'] = product.get_price()
                        product_row['Visible_On_CRM'] = True if product.active else False
                        product_row['Visible_On_Site'] = True if (product.is_indexable and product.active) else False
                        product_row['Type'] = product.get_type_product_display()
                        product_row['Product_Class'] = product.product_class.slug if product.get_product_class() else None
                        product_row['Parent'] = product.get_parent().name if product.get_parent() else None
                        product_row['Vendor'] = product.get_vendor()
                        product_row['Category'] = ", ".join([cat.__str__() for cat in product.categories.all()])
                        product_row['Study'] = product.get_studymode_db()
                        product_row['Duration'] = product.get_duration_db()
                        csvwriter.writerow(product_row)
                        count = count + 1
                        if count % 20 == 0:
                            up_task.percent_done = round((count / float(total_rows))*100, 2)
                            up_task.save()

                    up_task.percent_done = 100
                    up_task.status = 2
                    up_task.completed_on = timezone.now()
                    csvfile.close()
                    up_task.file_generated = upload_path
                    up_task.save()

                except Exception as e:
                    logging.getLogger('error_log').error(
                        "%(msg)s : %(err)s" % {'msg': 'genrate product list task', 'err': str(e)}
                    )
                    up_task.status = 1
                    up_task.save()
            except Exception as e:
                    logging.getLogger('error_log').error(
                        "%(msg)s : %(err)s" % {'msg': 'genrate product list task', 'err': str(e)}
                    )
                    up_task.status = 1
                    up_task.save()

    except Exception as e:
        up_task.status = 1
        up_task.save()
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'genrate product list task', 'err': str(e)})
    return f
