import logging
import os
import csv
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from celery.decorators import task
from scheduler.models import Scheduler
from partner.models import Certificate, UserCertificate
User = get_user_model()


@task(name="upload_certificate_task")
def upload_certificate_task(task=None, user=None, vendor=None):
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
                    exist_file = os.path.isfile(
                        settings.MEDIA_ROOT + '/' + upload_path)
                    if exist_file:
                        f = True
                        with open(
                            settings.MEDIA_ROOT + '/' + upload_path,
                            'r', encoding='utf-8', errors='ignore') as upload:
                            uploader = csv.DictReader(
                                upload, delimiter=',', quotechar='"')
                            try:
                                for i, line in enumerate(uploader):
                                    line.update({'provider': vendor})
                                    obj, created = Certificate.objects.get_or_create(**line)
                                    if created:
                                        usr_certi_obj = UserCertificate()
                                        usr_certi_obj.user = user
                                        usr_certi_obj.certificate = obj
                                        usr_certi_obj.save()
                                total_rows = i + 1
                            except Exception as e:
                                total_rows = 2000
                                logging.getLogger('error_log').error(
                                    "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
                        upload.close()
                        gen_dir = os.path.dirname(upload_path)
                        filename_tuple = upload_path.split('.')
                        extension = filename_tuple[len(filename_tuple) - 1]
                        gen_file_name = str(up_task.pk) + '_GENERATED' + '.' + extension
                        generated_path = gen_dir + '/' + gen_file_name
                        generated_file = open(
                            settings.MEDIA_ROOT + '/' + generated_path, 'w')
                        with open(
                            settings.MEDIA_ROOT + '/' + upload_path,
                            'r', encoding='utf-8', errors='ignore') as upload:
                            uploader = csv.DictReader(
                                upload, delimiter=',', quotechar='"')
                            count = 0
                            for row in uploader:
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
                        "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
                    up_task.status = 1
                    up_task.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
                up_task.status = 1
                up_task.save()
        return f
    except Exception as e:
        logging.getLogger('error_log').error(
            "%(msg)s : %(err)s" % {'msg': 'upload certificate task', 'err': str(e)})
    return f