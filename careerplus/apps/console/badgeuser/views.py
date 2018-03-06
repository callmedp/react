import os
import logging
from django.views.generic import FormView, ListView, View
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden,
    HttpResponse)
from django.conf import settings

from blog.mixins import PaginationMixin
from scheduler.models import Scheduler
from .tasks import (
    upload_certificate_task)
from . import forms


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
        context.update({
            'messages': alert})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            file = request.FILES.get('file', None)
            vendor = request.POST.get('user')
            task_type = 2
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

                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                dest = open(full_path + file_name, 'wb')

                for chunk in f_obj.chunks():
                    dest.write(chunk)
                dest.close()
                Task.file_uploaded = path + file_name
                Task.save()
                upload_certificate_task(
                    task=Task.pk, user=request.user.pk, vendor=vendor)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Task Created SuccessFully')
                return HttpResponseRedirect(reverse('console:tasks:tasklist'))
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, "%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                return HttpResponseRedirect(reverse('console:badge:upload-certificate'))
        return self.form_invalid(form)


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
        queryset = queryset.filter(task_type=2)
        return queryset.order_by('-modified')
