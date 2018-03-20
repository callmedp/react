import logging
import os
import mimetypes

from wsgiref.util import FileWrapper

from django.views.generic import FormView, ListView, View
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden,
    HttpResponse)
from django.conf import settings

from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from blog.mixins import PaginationMixin
from console.decorators import (
    Decorate, stop_browser_cache,
    check_group)
from scheduler.models import Scheduler

from .tasks import (
    gen_auto_login_token_task)
from . import forms


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.MARKETING_GROUP_LIST]))
class GenerateAutoLoginTask(FormView):
    template_name = "console/tasks/auto_login_token_task.html"
    success_url = "/console/tasks/tasklist/"
    http_method_names = [u'get', u'post']
    form_class = forms.LoginTokenGenerateForm

    def get_form_kwargs(self):
        kwargs = super(GenerateAutoLoginTask, self).get_form_kwargs()
        return kwargs

    def get(self, request, *args, **kwargs):
        return super(GenerateAutoLoginTask, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenerateAutoLoginTask, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            file = request.FILES.get('file', None)
            next_url = request.POST.get('next_url', '').strip()
            exp_days = request.POST.get('expiry', 0).strip()
            task_type = 1
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

#                if not os.path.exists(full_path):
#                   os.makedirs(full_path)
#                dest = open(full_path + file_name, 'wb')

#                for chunk in f_obj.chunks():
#                    dest.write(chunk)
#                dest.close()
                GCPPrivateMediaStorage().save(path + file_name, file)
                Task.file_uploaded = path + file_name
                Task.save()

                if not next_url:
                    next_url = None
                if exp_days:
                    try:
                        exp_days = int(exp_days)
                    except:
                        exp_days = None
                else:
                    exp_days = None

                gen_auto_login_token_task.delay(
                    task=Task.pk, user=request.user.pk,
                    next_url=next_url, exp_days=exp_days)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Task Created SuccessFully, Tokens are generating')
                return HttpResponseRedirect(reverse('console:tasks:tasklist'))
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, "%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Error in uploading', 'err': str(e)})
                return HttpResponseRedirect(reverse('console:tasks:generate-autologintoken'))

        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.MARKETING_GROUP_LIST]))
class TaskListView(ListView, PaginationMixin):
    template_name = 'console/tasks/tasklist.html'
    model = Scheduler
    http_method_names = [u'get', ]

    def __init__(self):
        self.page = 1
        self.paginated_by = 20

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        return super(TaskListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['scheduler_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
        })
        return context

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset()
        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.MARKETING_GROUP_LIST]))
class DownloadTaskView(View):

    def get(self, request, *args, **kwargs):
        try:
            task = request.GET.get('task', None)
            download_type = request.GET.get('type', None)
            if task:
                task = Scheduler.objects.get(id=task)
            else:
                return HttpResponseForbidden()
            if task:
                if download_type == 'u':
                    file_path = task.file_uploaded.path
                    filename_tuple = file_path.split('.')
                    extension = filename_tuple[len(filename_tuple) - 1]
                    file_name = str(task.pk) + '_UPLOAD' + '.' + extension
                else:
                    file_path = task.file_generated.path
                    filename_tuple = file_path.split('.')
                    extension = filename_tuple[len(filename_tuple) - 1]
                    file_name = str(task.pk) + '_GENERATED' + '.' + extension
                try:
                    fsock = GCPPrivateMediaStorage().open(file_path)
                except IOError:
                    messages.add_message(request, messages.ERROR, "Sorry, the document is currently unavailable.")
                    response = HttpResponseRedirect(reverse('console:tasks:tasklist'))
                    return response
                response = HttpResponse(fsock, content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
                return response
        except:
            messages.add_message(request, messages.ERROR, "Sorry, the document is currently unavailable.")
            response = HttpResponseRedirect(reverse('console:tasks:tasklist'))
            return response