import logging
import mimetypes
import json

from django.shortcuts import render
from wsgiref.util import FileWrapper
from django.http import (
    HttpResponse,
    HttpResponseRedirect,)
from django.contrib import messages
from django.views.generic import FormView, TemplateView, View
from django.core.urlresolvers import reverse

from shine.core import ShineCandidateDetail
from core.mixins import TokenExpiry, TokenGeneration
from order.models import OrderItem
from emailers.email import SendMail

from .forms import (
    RegistrationForm,
    LoginApiForm,
    SetConfirmPasswordForm,
    PasswordResetRequestForm)
from .mixins import RegistrationLoginApi


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

            elif resp['response'] == False:
                return render(self.request, self.template_name, {'form': form})    


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

    def get_context_data(self, **kwargs):
        context = super(LoginApiView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        form = self.get_form()
        context.update({
            'messages': alert,
            'form': form,
            "reset_form": PasswordResetRequestForm()
        })
        return context

    def form_valid(self, form):
        login_dict = {}
        remember_me = self.request.POST.get('remember_me', None)
        user_email = self.request.POST.get('email')
        login_dict.update({
            "email": user_email,
            "password": self.request.POST.get('password')
        })
        if 'next' in self.request.GET:
            self.success_url = self.request.GET.get('next')
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
                return render(
                    self.request, self.template_name,
                    {'form': form})

            elif not user_exist.get('response', ''):
                messages.add_message(self.request, messages.ERROR, "Something went wrong", 'danger')
                return render(
                    self.request, self.template_name,
                    {'form': form,})

            elif not user_exist.get('exists', ''):
                messages.add_message(self.request, messages.ERROR, "You do not have an account. Please register first.", 'danger')
                return render(
                    self.request, self.template_name,
                    {'form': form,})

        except Exception as e:
            logging.getLogger('error_log').error("Exception while logging in a user with email: %s. "
                                                 "Exception: %s " % (user_email, str(e)))
            messages.add_message(self.request, messages.ERROR, "Something went wrong", 'danger')
            return render(
                self.request, self.template_name,
                {'form': form})

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


class ForgotPasswordResetView(ShineCandidateDetail, FormView):
    template_name = "users/reset_password.html"
    form_class = SetConfirmPasswordForm
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        return super(ForgotPasswordResetView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForgotPasswordResetView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        token = self.request.GET.get('token')
        email, type, valid = TokenGeneration().decode(token)
        context.update({
            'messages': alert,
            'email': email,
            'token': token,
        })
        return context

    def post(self, request, *arg, **kwargs):
        email, type, valid = TokenGeneration().decode(request.POST.get("token"))
        form = self.form_class(request.POST)
        if valid:
            if form.is_valid():
                data = request.POST
                email_exist = RegistrationLoginApi.check_email_exist(data.get('email'))
                if email_exist['exists']:
                    pass_resp = RegistrationLoginApi.reset_update(data)
                    if pass_resp['response']:
                        messages.success(request, 'Password has been reset.')
                        return self.form_valid(form)
                    elif pass_resp['status_code'] == 400:
                        messages.success(request, 'Client Authentication Failed')
                        return self.form_valid(form)
                elif not email_exist['exists']:
                    messages.success(request, 'email does not exist')
                    return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


class ForgotHtmlView(TemplateView):
    template_name = "mobile/users/forgot_password.html"

    def get_context_data(self, **kwargs):
        context = super(ForgotHtmlView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert,
            "reset_form": PasswordResetRequestForm()
        })
        return context


class ForgotPasswordEmailView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            email = request.POST.get('email')
            user_exist = RegistrationLoginApi.check_email_exist(email)
            mail_type = 'FORGOT_PASSWORD'
            to_emails = [email]
            email_dict = {"email": email}

            if user_exist.get('exists', ''):
                try:
                    SendMail().send(to_emails, mail_type, email_dict)
                except Exception as e:
                    logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))
                return HttpResponse(json.dumps({'exist':True}), content_type="application/json")

            elif not user_exist.get('exists', ''):
                return HttpResponse(json.dumps({'notexist':True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'noresponse':True}), content_type="application/json")


class SocialLoginView(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('key') == 'fb':
                fb_user = RegistrationLoginApi.social_login(request.GET)
                candidateid = fb_user['user_details']['candidate_id']
                if fb_user.get('response'):
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None,
                        shine_id=candidateid)
                    request.session.update(resp_status)
                    return HttpResponseRedirect(self.success_url)
            elif request.GET.get('key') == 'gplus':
                gplus_user = RegistrationLoginApi.social_login(request.GET)
                if gplus_user.get('response'):
                    # candidateid = gplus_user['user_details']['candidate_id']
                    # resp_status = ShineCandidateDetail().get_status_detail(
                    #         email=None,
                    #         shine_id=fb_user['user_details']['candidate_id'])
                    # request.session.update(resp_status)
                    return HttpResponseRedirect(self.success_url)
        except Exception as e:
            raise e
