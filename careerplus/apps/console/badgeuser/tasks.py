import logging
import os
import csv
import json
import requests
import codecs
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from celery.decorators import task
from scheduler.models import Scheduler
from partner.models import Vendor
from partner.models import Certificate, UserCertificate
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from core.api_mixin import ShineCandidateDetail, ShineToken
from order.models import Order

User = get_user_model()


@task(name="upload_certificate_task")
def upload_certificate_task(task=None, user=None, vendor=None, vendor_text=None):
    f = False
    try:
        up_task = Scheduler.objects.get(pk=task)
        if vendor:
            vendor = Vendor.objects.get(pk=vendor)
    except Scheduler.DoesNotExist as e:
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
    except Vendor.DoesNotExist as e:
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
        up_task.status = 1
        up_task.save()
    else:
        up_task.status = 3
        up_task.save()
        upload_path = up_task.file_uploaded.name
        try:
            user = User.objects.get(pk=user)
        except User.DoesNotExist as e:
            logging.getLogger('error_log').error(
                "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
            up_task.status = 1
            up_task.save()
            return f
        if not settings.IS_GCP:
            exist_file = os.path.isfile(
                settings.MEDIA_ROOT + '/' + upload_path)
        else:
            exist_file = GCPPrivateMediaStorage().exists(
                upload_path)
        if exist_file:
            f = True
            fieldnames = ['name', 'skill', 'certificate_file_url', 'vendor_image_url']
            if not settings.IS_GCP:
                upload = open(
                    settings.MEDIA_ROOT + '/' + upload_path,
                    'r', encoding='utf-8', errors='ignore')
                uploader = csv.DictReader(
                    upload, delimiter=',', quotechar='"', fieldnames=fieldnames)
            else:
                upload = GCPPrivateMediaStorage().open(upload_path)
                uploader = csv.DictReader(
                    codecs.iterdecode(upload, 'utf-8'),
                    delimiter=',', quotechar='"', fieldnames=fieldnames)
            try:
                for i, line in enumerate(uploader):
                    pass
                total_rows = i
            except Exception as e:
                total_rows = 2000
                logging.getLogger('error_log').error(
                    "%(msg)s : %(err)s" % {
                        'msg': 'upload certificate task',
                        'err': str(e)})
            gen_dir = os.path.dirname(upload_path)
            filename_tuple = upload_path.split('.')
            extension = filename_tuple[len(filename_tuple) - 1]
            gen_file_name = str(up_task.pk) + '_GENERATED' + '.' + extension
            generated_path = gen_dir + '/' + gen_file_name
            if not settings.IS_GCP:
                generated_file = open(
                    settings.MEDIA_ROOT + '/' + generated_path, 'w')
                upload = open(
                    settings.MEDIA_ROOT + '/' + upload_path,
                    'r', encoding='utf-8', errors='ignore')
                uploader = csv.DictReader(
                    upload, delimiter=',', quotechar='"', fieldnames=fieldnames)
            else:
                generated_file = GCPPrivateMediaStorage().open(
                    generated_path, 'wb')
                upload = GCPPrivateMediaStorage().open(upload_path)
                uploader = csv.DictReader(
                    codecs.iterdecode(upload, 'utf-8'),
                    delimiter=',', quotechar='"', fieldnames=fieldnames)
            fieldnames.append('error_report')
            csvwriter = csv.DictWriter(
                generated_file, delimiter=',',
                fieldnames=fieldnames)
            csvwriter.writerow(
                dict((fn, fn) for fn in fieldnames))
            count = 0
            next(uploader, None)  # skip the headers
            for row in uploader:
                try:
                    name = row.get('name', '')
                    skill = row.get('skill', '')
                    certi_file_url = row.get('certificate_file_url')
                    vendor_image_url = row.get('vendor_image_url')
                    make_entry = False
                    if name:
                        if vendor:
                            existing_certificates = Certificate.objects.filter(
                                name=name, vendor_provider=vendor)
                        elif vendor_text:
                            existing_certificates = Certificate.objects.filter(
                                name=name, vendor_text=vendor_text)

                        if not existing_certificates.exists():
                            make_entry = True
                        else:
                            all_skills = list(existing_certificates.exclude(skill="").values_list('skill', flat=True))
                            processed_all_skills = []
                            for skl in all_skills:
                                skl = sorted(map(lambda s: s.strip(), skl.split(',')))
                                skl = "|".join(skl)
                                processed_all_skills.append(skl)

                            new_skill = list(sorted(map(lambda s: s.strip(), skill.split(','))))
                            new_skill = "|".join(new_skill)

                            if new_skill not in processed_all_skills:
                                make_entry = True

                        if make_entry:
                            if vendor:
                                obj = Certificate.objects.create(
                                    name=name, vendor_provider=vendor)
                            elif vendor_text:
                                obj = Certificate.objects.create(
                                    name=name, vendor_text=vendor_text)
                            if certi_file_url:
                                obj.certificate_file_url = certi_file_url
                            if vendor_image_url:
                                obj.vendor_image_url = vendor_image_url
                            skill = ','.join(sorted(skill.split(',')))
                            obj.skill = skill
                            obj.save()

                        else:
                            row['error_report'] = "certificate already exists"
                    else:

                        row['error_report'] = "certificate name missing"
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
            logging.getLogger('error_log').error(
                "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': "uploaded file not found"})
            up_task.status = 1
            up_task.save()
    return f


@task(name="upload_candidate_certificate_task")
def upload_candidate_certificate_task(task=None, user=None, vendor=None,  vendor_text=None):
    f = False
    try:
        up_task = Scheduler.objects.get(pk=task)
    except Scheduler.DoesNotExist as e:
        logging.getLogger('error_log').error(
            "%(err)s" % {'err': str(e)})
        return f
    if vendor:
        try:
            vendor = Vendor.objects.get(pk=vendor)
        except Vendor.DoesNotExist as e:
            logging.getLogger('error_log').error(
                "%(err)s" % {'err': str(e)})
            up_task.status = 1
            up_task.save()
            return f
    up_task.status = 3
    up_task.save()
    upload_path = up_task.file_uploaded.name
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist as e:
        logging.getLogger('error_log').error(
            "%(err)s" % {'err': str(e)})
        up_task.status = 1
        up_task.save()
        return f
    if not settings.IS_GCP:
        exist_file = os.path.isfile(
            settings.MEDIA_ROOT + '/' + upload_path)
    else:
        exist_file = GCPPrivateMediaStorage().exists(
            upload_path)
    if exist_file:
        f = True
        fieldnames = ['year', 'candidate_email', 'candidate_mobile', 'certificate_name', 'certificate_file_url' , 'order']
        if not settings.IS_GCP:
            with open(
                settings.MEDIA_ROOT + '/' + upload_path,
                    'r', encoding='utf-8', errors='ignore') as upload:
                uploader = csv.DictReader(
                    upload, delimiter=',', quotechar='"', fieldnames=fieldnames)
                try:
                    for i, line in enumerate(uploader):
                        pass
                    total_rows = i
                except Exception as e:
                    total_rows = 2000
                    logging.getLogger('error_log').error(
                        "%(err)s" % {'err': str(e)})
        else:
            with GCPPrivateMediaStorage().open(upload_path) as upload:
                uploader = csv.DictReader(
                    codecs.iterdecode(upload, 'utf-8'),
                    delimiter=',', quotechar='"', fieldnames=fieldnames)
                try:
                    for i, line in enumerate(uploader):
                        pass
                    total_rows = i
                except Exception as e:
                    total_rows = 2000
                    logging.getLogger('error_log').error(
                        "%(err)s" % {'err': str(e)})
        gen_dir = os.path.dirname(upload_path)
        filename_tuple = upload_path.split('.')
        extension = filename_tuple[len(filename_tuple) - 1]
        gen_file_name = str(up_task.pk) + '_GENERATED' + '.' + extension
        generated_path = gen_dir + '/' + gen_file_name
        if not settings.IS_GCP:
            generated_file = open(
                settings.MEDIA_ROOT + '/' + generated_path, 'w')
            upload = open(
                settings.MEDIA_ROOT + '/' + upload_path,
                'r', encoding='utf-8', errors='ignore')
            uploader = csv.DictReader(
                upload, delimiter=',', quotechar='"', fieldnames=fieldnames)
        else:
            generated_file = GCPPrivateMediaStorage().open(
                generated_path, 'wb')
            upload = GCPPrivateMediaStorage().open(
                upload_path)
            uploader = csv.DictReader(
                codecs.iterdecode(upload, 'utf-8'),
                delimiter=',', quotechar='"', fieldnames=fieldnames)
        fieldnames.append('status')
        fieldnames.append('reason_for_failure')
        csvwriter = csv.DictWriter(
            generated_file, delimiter=',', fieldnames=fieldnames)
        csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
        count = 0
        next(uploader, None)  # skip the headers
        for row in uploader:
            try:
                email = row.get('candidate_email', '')
                mobile = row.get('candidate_mobile', '')
                certificate_name = row.get('certificate_name')
                certi_yr_passing = row.get('year')
                certi_file_url = row.get('certificate_file_url')
                order = row.get('order')
                if order:
                    order = Order.objects.filter(id=order).first()
                headers = ShineToken().get_api_headers()
                shineid = ShineCandidateDetail().get_shine_id(
                    email=email, headers=headers)
                if not certificate_name:
                    row['reason_for_failure'] = "Certificate not found"
                    row['status'] = "Failure"
                if shineid and certificate_name:
                    try:
                        if vendor:
                            certificate = Certificate.objects.get(
                                name__iexact=certificate_name,
                                vendor_provider=vendor)
                        elif vendor_text:
                            certificate = Certificate.objects.get(
                                name__iexact=certificate_name,
                                vendor_text=vendor_text)
                    except Certificate.DoesNotExist:
                        logging.getLogger("error_log").error("Certificate not found,{}".format(certificate_name))
                        row['reason_for_failure'] = "Certificate not found"
                        row['status'] = "Failure"
                    else:
                        logging.getLogger("error_log").info("working for,{}".format(certificate_name))
                        obj, created = UserCertificate.objects.get_or_create(
                            user=user, certificate=certificate,
                            year=certi_yr_passing,
                            candidate_id=shineid)
                        if created:
                            obj.candidate_mobile = mobile
                            obj.candidate_email = email
                            if certi_file_url:
                                obj.certificate_file_url = certi_file_url
                            obj.save()
                            post_data = {
                                'certification_name': certificate_name,
                                'certification_year': certi_yr_passing
                            }
                            certification_url = settings.SHINE_API_URL + "/candidate/" +shineid + "/certifications/?format=json"
                            certification_response = requests.post(
                                certification_url, data=post_data,
                                headers=headers)
                            if certification_response.status_code == 201:
                                jsonrsp = certification_response.json()
                                logging.getLogger('info_log').info(
                                    "api response:{}".format(jsonrsp))
                            elif certification_response.status_code != 201:
                                jsonrsp = certification_response.json()
                                logging.getLogger('error_log').error(
                                    "api fail:{}".format(jsonrsp))
                                row['reason_for_failure'] = jsonrsp
                                row['status'] = 'Failure'
                        else:
                            row['reason_for_failure'] = "duplicate entry"
                            row['status'] = "Success"
                else:
                    row['reason_for_failure'] = "user not registered on shine"
                    row['status'] = "Failure"
                csvwriter.writerow(row)
            except Exception as e:
                row['reason_for_failure'] = str(e)
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
        logging.getLogger('error_log').error("Candidate Certificate file not found:{}".format(upload_path))
        up_task.status = 1
        up_task.save()
    return f