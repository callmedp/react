import logging
import mimetypes
import json

from django.shortcuts import render
from wsgiref.util import FileWrapper
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,)
from django.contrib import messages
from django.views.generic import FormView, TemplateView, View
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.conf import settings

from shine.core import ShineCandidateDetail
from core.mixins import TokenExpiry
from order.models import OrderItem
from core.api_mixin import ShineCandidateDetail

from .forms import RegistrationForm, LoginApiForm
from .mixins import RegistrationLoginApi
from .dashboard_mixin import DashboardInfo


class DashboardView(TemplateView):
    template_name = "users/dashboard-inbox.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            return super(DashboardView, self).get(request, args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id', None)
        email = self.request.session.get('email')
        # if candidate_id:
        #     if not self.request.session.get('resume_id', None):
        #         res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
        #         resumes = res['resumes']
        #         default_resumes = [resume for resume in resumes if resume['is_default']]
        #         if default_resumes:
        #             self.request.session.update({
        #                 "resume_id": default_resumes[0].get('id', '')
        #             })
        inbox_list = DashboardInfo().get_inbox_list(candidate_id=candidate_id)
        pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id, email=email)
        context.update({
            'inbox_list': inbox_list,
            'pending_resume_items': pending_resume_items,
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            candidate_id = request.session.get('candidate_id')
            resume_type = request.POST.get('resume_type', '0').strip()
            file = request.FILES.get('file', '')
            list_ids = request.POST.getlist('resume_pending', [])
            validation_error = ''

            if resume_type == '0' and file:
                extn = file.name.split('.')[-1]
                if extn in ['doc', 'docx', 'pdf'] and list_ids:
                    data = {
                        "list_ids": list_ids,
                        "candidate_resume": file,
                    }
                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
                elif not list_ids:
                    validation_error = 'Please select atleast one services to upload resume'
                    context = self.get_context_data()
                    context.update({
                        "validation_error": validation_error,
                    })
                    return TemplateResponse(
                        request, ["users/dashboard-inbox.html"], context)
                else:
                    validation_error = 'Only doc, docx and pdf formats are allowed'
                    context = self.get_context_data()
                    context.update({
                        "validation_error": validation_error,
                    })
                    return TemplateResponse(
                        request, ["users/dashboard-inbox.html"], context)
            elif resume_type == 1:
                pass
        return HttpResponseRedirect(reverse('dashboard'))


class DashboardDetailView(TemplateView):
    template_name = 'include/inboxoi-deatil.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and self.candidate_id:
            self.oi_pk = request.GET.get('oi_pk')

            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass
                else:
                    return ''
            except:
                return ''
            return super(DashboardDetailView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            ops = []
            if self.oi.product.type_flow in [1, 12, 13]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 24, 26, 27])
            elif self.oi.product.type_flow == 2:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6])

            elif self.oi.product.type_flow == 3:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 121])
            elif self.oi.product.type_flow == 4:
                pass
            elif self.oi.product.type_flow == 5:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 27])
            elif self.oi.product.type_flow == 6:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82])
            elif self.oi.product.type_flow == 7:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 61, 62])
            elif self.oi.product.type_flow == 8:
                pass
            elif self.oi.product.type_flow == 10:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 101])
            context.update({
                "oi": self.oi,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "ops": list(ops),
            })
        return context


class DashboardCommentView(TemplateView):
    template_name = 'include/user-inbox-comment.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi_pk')
        if self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass
                else:
                    return ''
            except:
                return ''
            return super(DashboardCommentView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardCommentView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            comments = self.oi.message_set.filter(is_internal=False).order_by('added_on')
            context.update({
                "oi": self.oi,
                "comments": comments
            })
        return context

    def post(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and self.candidate_id:
            self.oi_pk = request.POST.get('oi_pk')
            comment = request.POST.get('comment', '').strip()
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and comment:
                    self.oi.message_set.create(
                        message=comment,
                        candidate_id=self.candidate_id,
                    )
            except:
                pass
            redirect_url = reverse('users:dashboard-comment') + '?oi_pk=%s' % (self.oi_pk)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseForbidden()


class DashboardRejectService(View):
    def get(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        oi_pk = request.GET.get('oi_pk', None)
        if request.is_ajax() and self.candidate_id and oi_pk:

            try:
                oi = OrderItem.objects.get(pk=self.oi_pk)
                if oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    if oi.product.type_flow in [1, 12, 13] and oi.oi_status == 24:
                        pass
            except:
                pass
            return super(DashboardDetailView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()


class RegistrationApiView(FormView):
    template_name = 'users/register.html'
    http_method_names = [u'get', u'post']
    success_url = '/'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super(RegistrationApiView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        form = self.get_form()
        context.update({
            'messages': alert,
            'form': form
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(RegistrationApiView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        login_dict, post_data = {}, {}
        post_data.update({
            "email": request.POST.get('email'),
            "raw_password": request.POST.get('raw_password'),
            "cell_phone": request.POST.get('cell_phone'),
            "country_code": request.POST.get('country_code'),
            "vendor_id": request.POST.get('vendor_id'),
            "is_job_seeker": request.POST.get('is_job_seeker') == 'on'
        })
        user_resp = RegistrationLoginApi.user_registration(post_data)

        if user_resp['response'] == 'new_user':
            login_dict.update({
                "email": request.POST.get('email'),
                "password": request.POST.get('password') if request.POST.get('password')
                            else request.POST.get('raw_password'),
            })
            resp = RegistrationLoginApi.user_login(login_dict)
            
            if resp['response'] == 'login_user':
                resp_status = ShineCandidateDetail().get_status_detail(shine_id=resp['candidate_id'])
                request.session.update(resp_status)
                return HttpResponseRedirect(self.success_url)

        elif user_resp['response'] == 'exist_user':
            messages.add_message(self.request, messages.ERROR, "This user already exists", 'danger')
            return HttpResponseRedirect(reverse('login'))

        elif not user_resp['response']:
            messages.add_message(self.request, messages.ERROR, "Something went wrong", 'danger')
        return render(self.request, self.template_name, {'form': form})

    def get_form_kwargs(self):
        kwargs = super(RegistrationApiView, self).get_form_kwargs()
        kwargs['flavour'] = self.request.flavour
        return kwargs


class LoginApiView(FormView):
    form_class = LoginApiForm
    template_name = "users/login.html"
    success_url = "/"

    def form_valid(self, form):
        login_dict = {}
        remember_me = self.request.POST.get('remember_me', None)
        user_email = self.request.POST.get('email')
        login_dict.update({
            "email": user_email,
            "password": self.request.POST.get('password')
        })
        try:
            user_exist = RegistrationLoginApi.check_email_exist(login_dict['email'])
            if user_exist.get('exists', ''):
                login_resp = RegistrationLoginApi.user_login(login_dict) # TODO: Do we need this check here
                                                                        # TODO: if we have that check on frontend?
                if login_resp['response'] == 'login_user':
                    resp_status = ShineCandidateDetail().get_status_detail(email=None,
                        shine_id=login_resp.get('candidate_id', ''))
                    if resp_status:
                        self.request.session.update(resp_status)

                    if remember_me:
                        self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                    return HttpResponseRedirect(self.success_url)

                elif login_resp['response'] == 'error_pass':
                    messages.add_message(self.request, messages.ERROR, login_resp["non_field_errors"][0], 'danger')
                elif not login_resp['response']:
                    messages.add_message(self.request, messages.ERROR, "Something went wrong", 'danger')
                return render(self.request, self.template_name, {'form': form})

            elif not user_exist.get('response', ''):
                messages.add_message(self.request, messages.ERROR, "Something went wrong", 'danger')
                return render(self.request, self.template_name, {'form': form})

            elif not user_exist.get('exists', ''):
                messages.add_message(self.request, messages.ERROR, "You do not have an account. Please register first.", 'danger')
                return render(self.request, self.template_name, {'form': form})

        except Exception as e:
            logging.getLogger('error_log').error("Exception while logging in a user with email: %s. "
                                                 "Exception: %s " % (user_email, str(e)))

    def dispatch(self, request, *args, **kwargs):

        if request.session.get('candidate_id'):
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET.get(
                    'next', self.success_url))
            return HttpResponseRedirect(self.success_url)
        else:
            return super(LoginApiView, self).dispatch(request, *args, **kwargs)


class LogoutApiView(TemplateView):

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect(reverse('homepage'))


class DownloadBoosterResume(View):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token', '')
            email, oi_pk, valid = TokenExpiry().decode(token)
            if valid:
                oi = OrderItem.objects.get(pk=oi_pk)

                if oi.oi_draft:
                    resume = oi.oi_draft
                    file_path = resume.path
                    filename = resume.name
                    extn = filename.split('.')[-1]
                    newfilename = 'resume_' + oi.order.first_name + '.' + extn

                    path = file_path
                    try:
                        fsock = FileWrapper(open(path, 'rb'))
                    except IOError:
                        raise Exception("Resume not found.")

                    response = HttpResponse(fsock, content_type=mimetypes.guess_type(path)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (newfilename)
                    return response
                else:
                    raise Exception("Resume not found.")
        except:
            messages.add_message(request, messages.ERROR, "Sorry, the document is currently unavailable.")
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return response