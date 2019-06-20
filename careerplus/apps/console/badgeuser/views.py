import os
import mimetypes
import logging
from django.views.generic import FormView, ListView, View
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from wsgiref.util import FileWrapper
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden,
    HttpResponse)
from django.conf import settings

from blog.mixins import PaginationMixin
from scheduler.models import Scheduler
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from .tasks import (
    upload_certificate_task,
    upload_candidate_certificate_task)
from console.decorators import (
    Decorate, stop_browser_cache,
    check_group)
from . import forms


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST]))
class UploadCertificate(FormView):
    template_name = "console/badgeuser/upload_certificate.html"
    http_method_names = [u'get', u'post']
    form_class = forms.UploadCertificateForm

    def get_form_kwargs(self):
        kwargs = super(UploadCertificate, self).get_form_kwargs()
        kwargs.update({'requestuser': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        return super(UploadCertificate, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadCertificate, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        upload_type = self.kwargs.get('upload_type')
        context.update({
            'messages': alert,
            'upload_type': upload_type})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            file = request.FILES.get('file', None)
            vendor = request.POST.get('user')
            upload_type = self.kwargs.get('upload_type')
            vendor_text = request.POST.get('vendor_text')
            task_type = 0
            if upload_type == "upload-certificate":
                task_type = 2
            elif upload_type == "upload-candidate-certificate":
                task_type = 3
            try:
                import time
                timestr = time.strftime("%Y_%m_%d")
                f_obj = file
                file_name_tuple = os.path.splitext(f_obj.name)
                extention = file_name_tuple[len(file_name_tuple) - 1] if len(
                    file_name_tuple) > 1 else ''
                Task = Scheduler.objects.create(
                    task_type=task_type,
                    created_by=request.user)
                file_name = str(Task.pk) + '_' + 'UPLOAD' + extention
                path = 'scheduler/' + timestr + '/'
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                if not settings.IS_GCP:
                    if not os.path.exists(full_path):
                        os.makedirs(full_path)
                    dest = open(full_path + file_name, 'wb')

                    for chunk in f_obj.chunks():
                        dest.write(chunk)
                    dest.close()
                else:
                    GCPPrivateMediaStorage().save(path + file_name, file)
                Task.file_uploaded = path + file_name
                Task.save()
                if upload_type == "upload-certificate":
                    upload_certificate_task.delay(
                        task=Task.pk, user=request.user.pk, vendor=vendor, vendor_text=vendor_text)
                    # upload_certificate_task(
                    #     task=Task.pk, user=request.user.pk, vendor=vendor)
                elif upload_type == "upload-candidate-certificate":
                    upload_candidate_certificate_task.delay(
                        task=Task.pk, user=request.user.pk, vendor=vendor)
                    # upload_candidate_certificate_task(
                    #     task=Task.pk, user=request.user.pk, vendor=vendor)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Task Created SuccessFully')
                return HttpResponseRedirect(reverse('console:badge:upload-tasklist'))
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, "%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                return HttpResponseRedirect(reverse('console:badge:upload-certificate'))
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST]))
class UploadTaskListView(ListView, PaginationMixin):
    template_name = 'console/badgeuser/upload_task_list.html'
    model = Scheduler
    http_method_names = [u'get', ]

    def __init__(self):
        self.page = 1
        self.paginated_by = 20

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        return super(UploadTaskListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadTaskListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['scheduler_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
        })
        return context

    def get_queryset(self):
        queryset = super(UploadTaskListView, self).get_queryset()
        queryset = queryset.filter(task_type__in=[2, 3])
        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST]))
class DownloadBadgeUserView(View):

    def get(self, request, *args, **kwargs):
        try:
            task = request.GET.get('task', None)
            download_type = request.GET.get('type', None)
            file_path = ''
            if task:
                task = Scheduler.objects.get(id=task)
            else:
                return HttpResponseForbidden()
            if task:
                if download_type == 'u':
                    file_path = task.file_uploaded.name
                    filename_tuple = file_path.split('.')
                    extension = filename_tuple[len(filename_tuple) - 1]
                    file_name = str(task.pk) + '_UPLOAD' + '.' + extension
                elif download_type == 'd':
                    file_path = task.file_generated.name
                    filename_tuple = file_path.split('.')
                    extension = filename_tuple[len(filename_tuple) - 1]
                    file_name = str(task.pk) + '_GENERATED' + '.' + extension
                try:
                    if not settings.IS_GCP:
                        if os.path.exists(file_path):
                            path = file_path
                        else:
                            path = settings.MEDIA_ROOT + '/' + file_path
                        fsock = FileWrapper(open(path, 'rb'))
                    else:
                        fsock = GCPPrivateMediaStorage().open(file_path)
                        path = file_path
                except IOError:
                    logging.getLogger("error_log").error(
                        "Sorry, the document is currently unavailable.")
                    messages.add_message(
                        request, messages.ERROR,
                        "Sorry, the document is currently unavailable.")
                    response = HttpResponseRedirect(
                        reverse('console:badge:upload-tasklist'))
                    return response
                response = HttpResponse(
                    fsock, content_type=mimetypes.guess_type(path)[0])
                response['Content-Disposition'] = 'attachment; filename="%s"' % (file_name)
                return response
        except:
            logging.getLogger("error_log").error(
                "Sorry, the document is currently unavailable.")
            messages.add_message(
                request, messages.ERROR,
                "Sorry, the document is currently unavailable.")
            response = HttpResponseRedirect(reverse('console:badge:upload-tasklist'))
            return response
