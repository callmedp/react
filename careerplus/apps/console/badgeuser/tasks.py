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
User = get_user_model()


@task(name="upload_certificate_task")
def upload_certificate_task(task=None, user=None, vendor=None):
    f = False
    try:
        up_task = Scheduler.objects.get(pk=task)
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
            fieldnames = ['name', 'skill']
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
                    if name:
                        obj, created = Certificate.objects.get_or_create(
                        name=name, vendor=vendor)
                        if created:
                            obj.skill = skill
                            obj.save()
                        else:
                            row['error_report'] = "certificate already exist"
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
def upload_candidate_certificate_task(task=None, user=None, vendor=None):
    f = False
    try:
        up_task = Scheduler.objects.get(pk=task)
    except Scheduler.DoesNotExist as e:
        logging.getLogger('error_log').error(
            "%(err)s" % {'err': str(e)})
        return f
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
        fieldnames = ['year', 'candidate_email', 'candidate_mobile', 'certificate_name']
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
                headers = ShineToken().get_api_headers()
                shineid = ShineCandidateDetail().get_shine_id(
                    email=email, headers=headers)
                if not certificate_name:
                    row['certificate_name'] = "certificate not found"
                if shineid and certificate_name:
                    try:
                        certificate = Certificate.objects.get(
                            name__iexact=certificate_name, vendor_provider=vendor)
                    except Certificate.DoesNotExist:
                        row['reason_for_failure'] = "Certificate not found"
                        row['status'] = "Failure"
                        continue
                    else:
                        obj, created = UserCertificate.objects.get_or_create(
                            user=user, certificate=certificate,
                            year=certi_yr_passing,
                            candidate_id=shineid)
                        if created:
                            obj.candidate_mobile = mobile
                            obj.candidate_email = email
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