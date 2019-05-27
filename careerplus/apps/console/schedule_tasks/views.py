import logging
import os
import mimetypes
from jsmin import jsmin

from wsgiref.util import FileWrapper

from django.views.generic import FormView, ListView, View, TemplateView
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
    check_group, has_group)
from scheduler.models import Scheduler

from .tasks import (
    gen_auto_login_token_task,
    gen_product_list_task,
    generate_encrypted_urls_for_mailer_task
)
from . import forms

from shop.models import Product
from partner.models import Vendor


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
                if not settings.IS_GCP:
                    full_path = os.path.join(settings.MEDIA_ROOT, path)
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

                if not next_url:
                    next_url = None
                if exp_days:
                    try:
                        exp_days = int(exp_days)
                    except Exception as e:
                        logging.getLogger('error_log').error('unable to get exp_days %s' % str(e))
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
class GenerateEncryptedURLSForMailer(FormView):
    template_name = "console/tasks/encrypted_links_for_mailer.html"
    success_url = "/console/tasks/tasklist/"
    http_method_names = [u'get', u'post']
    form_class = forms.EncryptedURLSGenerateForm

    def get_context_data(self, **kwargs):
        context = super(GenerateEncryptedURLSForMailer, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context

    def form_valid(self,form):
        import time
        f_obj = form.cleaned_data.get('file')
        task_type = 5

        file_name_tuple = os.path.splitext(f_obj.name)
        extension = file_name_tuple[len(file_name_tuple) - 1] if len(
            file_name_tuple) > 1 else ''
        scheduler_obj = Scheduler.objects.create(
            task_type=task_type,
            created_by=self.request.user)
        file_name = str(scheduler_obj.pk) + '_' + 'UPLOAD' + extension
        
        path = 'scheduler/' + time.strftime("%Y_%m_%d") + '/'
        if not settings.IS_GCP:
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            dest = open(full_path + file_name, 'wb')
            for chunk in f_obj.chunks():
                dest.write(chunk)
            dest.close()
        else:
            GCPPrivateMediaStorage().save(path + file_name, f_obj)
        scheduler_obj.file_uploaded = path + file_name
        scheduler_obj.save()

        generate_encrypted_urls_for_mailer_task.delay(
            task_id=scheduler_obj.pk, user=self.request.user.pk)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Task Created SuccessFully, Your file is being generated.')
        return super(GenerateEncryptedURLSForMailer,self).form_valid(form)


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
        queryset = queryset.filter(task_type__in=[1, 4, 5, 6])
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
                    if not settings.IS_GCP:
                        file_path = task.file_uploaded.path
                    else:
                        file_path = task.file_uploaded.name
                    filename_tuple = file_path.split('.')
                    extension = filename_tuple[len(filename_tuple) - 1]
                    file_name = str(task.pk) + '_UPLOAD' + '.' + extension
                else:
                    if not settings.IS_GCP:
                        file_path = task.file_generated.path
                    else:
                        file_path = task.file_generated.name
                    # file_path = task.file_generated.path
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
                except IOError:
                    messages.add_message(request, messages.ERROR, "Sorry, the document is currently unavailable.")
                    response = HttpResponseRedirect(reverse('console:tasks:tasklist'))
                    return response
                response = HttpResponse(fsock, content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
                return response
        except Exception as e:
            logging.getLogger('error_log').error('unable to download document  %s' % str(e))

            messages.add_message(request, messages.ERROR, "Sorry, the document is currently unavailable.")
            response = HttpResponseRedirect(reverse('console:tasks:tasklist'))
            return response


class DownloadProductListView(TemplateView, PaginationMixin):
    model = Product
    template_name = 'console/tasks/download_list_product.html'
    vendor_list = []
    vendor_select = None
    product_class_list = []
    product_class_select = None
    status = None

    def get(self, request, *args, **kwargs):
        self.vendor_list = Vendor.objects.all().values_list('name', flat=True).distinct()
        self.product_class_list = settings.COURSE_SLUG + settings.SERVICE_SLUG
        return super(DownloadProductListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DownloadProductListView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
            'vendor_list': self.vendor_list,
            'vendor_select': self.vendor_select,
            'product_class_list': self.product_class_list,
            'product_class_select': self.product_class_select
        })
        return context

    def post(self, request, *args, **kwargs):
        task_type = 4
        self.status = request.POST.get('is_active', '')
        self.vendor_select = request.POST.get('vendor', '')
        self.product_class_select = request.POST.get('product_class', '')
        Task = Scheduler.objects.create(
            task_type=task_type,
            created_by=request.user,
        )
        gen_product_list_task.delay(
            task=Task.pk,
            user=request.user.pk,
            status=self.status,
            vendor=self.vendor_select,
            product_class=self.product_class_select)
        messages.add_message(
            request, messages.SUCCESS,
            'Task Created SuccessFully, Product List is generating')
        return HttpResponseRedirect(reverse('console:tasks:tasklist'))


class GeneratePixelTracker(FormView):
    template_name = 'console/tasks/generate-pixel-tracker.html'
    form_class = forms.PixelGenerationForm

    def generate_pixel_code(self, pixel_slug, landing_urls, conversion_url, days=90):
        pixel_file = open('pixel_tracker.js')
        content = jsmin(pixel_file.read())
        pixel_url = settings.SITE_DOMAIN + '/pixel/' + pixel_slug
        content = content.replace('pixel_url', "'" + pixel_url + "'")
        content = content.replace('no_of_days', str(days))
        content = content.replace('createcookiurls', ",".join(["'" + url + "'" for url in landing_urls]))
        content = content.replace('readcookieurls', ",".join(["'" + url + "'" for url in conversion_url]))
        return content

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save()
            content = self.generate_pixel_code(
                obj.pixel_slug,
                obj.landing_urls.split(','),
                obj.conversion_urls.split(','),
                obj.days
            )
            context = self.get_context_data()
            context.update({'pixel_tracker': content})
            return self.render_to_response(context) 
        return self.form_invalid(form)

