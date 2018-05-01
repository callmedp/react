import logging
import mimetypes
import json
import urllib.parse

from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,)
from django.contrib import messages
from django.views.generic import FormView, TemplateView, View
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from geolocation.models import Country
from shine.core import ShineCandidateDetail
from core.mixins import TokenExpiry, TokenGeneration
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage, GCPInvoiceStorage
from order.models import OrderItem
from users.mixins import WriterInvoiceMixin

from emailers.tasks import send_email_task

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
        post_data = {}
        post_data.update({
            "email": request.POST.get('email'),
            "raw_password": request.POST.get('raw_password'),
            "cell_phone": request.POST.get('cell_phone'),
            "country_code": request.POST.get('country_code'),
            "vendor_id": settings.CP_VENDOR_ID,
            "is_job_seeker": request.POST.get('is_job_seeker') == 'on'
        })
        resp = RegistrationLoginApi.user_registration(post_data)

        if resp['response'] == 'new_user' and resp['id']:
            mail_type = "REGISTRATION"
            email_dict = {}
            email_dict.update({
                'email': resp['email'],
                'password': request.POST.get('raw_password'),
            })
            # task for email
            send_email_task.delay(
                [resp['email']], mail_type, email_dict, status=None, oi=None)
            resp_status = ShineCandidateDetail().get_status_detail(
                shine_id=resp['id'], token=resp['access_token'])
            request.session.update(resp_status)
            return HttpResponseRedirect(self.success_url)

        elif resp['response'] == 'exist_user':
            messages.add_message(
                self.request, messages.ERROR,
                "This user already exists", 'danger')
            return HttpResponseRedirect(reverse('login'))

        elif not resp['response']:
            messages.add_message(
                self.request, messages.ERROR,
                "Something went wrong", 'danger')
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
        linkedin = self.request.GET.get('linkedin', '')
        linkedin_mobile = self.request.GET.get('linkedin_mobile', '')
        if linkedin == 'true':
            context.update({
                "linkedin": True,
            })
        if linkedin_mobile == 'true':
            country_objs = Country.objects.exclude(
                Q(phone__isnull=True) | Q(phone__exact=''))
            context.update({
                "country_objs": country_objs,
                "linkedin_mobile": True
            })

        context.update({
            'messages': alert,
            'form': form,
            "reset_form": PasswordResetRequestForm()
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
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
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None,
                        shine_id=login_resp.get('candidate_id', ''))
                    if resp_status:
                        self.request.session.update(resp_status)

                    if remember_me:
                        self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                    return HttpResponseRedirect(self.success_url)

                elif login_resp['response'] == 'error_pass':
                    messages.add_message(
                        self.request, messages.ERROR,
                        login_resp["non_field_errors"][0], 'danger')
                elif not login_resp['response']:
                    messages.add_message(
                        self.request, messages.ERROR,
                        "Something went wrong", 'danger')
                return render(
                    self.request, self.template_name,
                    {'form': form, 'reset_form': context['reset_form']})

            elif not user_exist.get('response', ''):
                messages.add_message(
                    self.request, messages.ERROR,
                    "Something went wrong", 'danger')
                return render(
                    self.request, self.template_name,
                    {'form': form, 'reset_form': context['reset_form']})

            elif not user_exist.get('exists', ''):
                messages.add_message(
                    self.request, messages.ERROR,
                    "You do not have an account. Please register first.",
                    'danger')
                return render(
                    self.request, self.template_name,
                    {'form': form, 'reset_form': context['reset_form']})

        except Exception as e:
            logging.getLogger(
                'error_log').error(
                "Exception while logging in a user with email: %s. "
                "Exception: %s " % (user_email, str(e))
            )
            messages.add_message(
                self.request, messages.ERROR,
                "Something went wrong", 'danger')
            return render(
                self.request, self.template_name,
                {'form': form, 'reset_form': context['reset_form']})

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
        response = HttpResponseRedirect(reverse('homepage'))
        response.delete_cookie('_em_', domain='.shine.com')
        return response


class DownloadBoosterResume(View):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token', '')
            email, oi_pk, valid = TokenExpiry().decode(token)
            if valid:
                oi = OrderItem.objects.get(pk=oi_pk)
                if oi.oi_draft:
                    resume = oi.oi_draft
                elif oi.oi_resume:
                    resume = oi.oi_resume

                if resume:
                    resume_name = resume.name
                    if resume_name.startswith('/'):
                        resume_name = resume_name[1:]
                    file_path = settings.RESUME_DIR + resume_name
                    filename = resume.name
                    extn = filename.split('.')[-1]
                    newfilename = 'resume_' + oi.order.first_name + '.' + extn

                    path = file_path
                    try:
                        if not settings.IS_GCP:
                            fsock = FileWrapper(open(path, 'rb'))
                        else:
                            fsock = GCPPrivateMediaStorage().open(file_path)
                    except IOError:
                        raise Exception("Resume not found.")

                    response = HttpResponse(
                        fsock, content_type=mimetypes.guess_type(path)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (newfilename)
                    return response
                else:
                    logging.getLogger(
                        'error_log').error("candidate booster resume not found")
                    raise Exception("Resume not found.")
        except:
            messages.add_message(
                request, messages.ERROR,
                "Sorry, the document is currently unavailable.")
            logging.getLogger(
                'error_log').error("candidate booster resume not found")
            response = HttpResponseRedirect(
                request.META.get('HTTP_REFERER', '/'))
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
        email, type, valid = TokenGeneration().decode(
            request.POST.get("token"))
        form = self.form_class(request.POST)
        if valid:
            if form.is_valid():
                data = request.POST
                email_exist = RegistrationLoginApi.check_email_exist(
                    data.get('email'))
                if email_exist['exists']:
                    pass_resp = RegistrationLoginApi.reset_update(data)
                    if pass_resp['response']:
                        messages.success(request, 'Password has been reset.')
                        return self.form_valid(form)
                    elif pass_resp['status_code'] == 400:
                        messages.success(
                            request, 'Client Authentication Failed')
                        return self.form_valid(form)
                elif not email_exist['exists']:
                    messages.success(request, 'email does not exist')
                    return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


class ForgotHtmlView(TemplateView):
    template_name = "mobile/users/forgot_password.html"

    def get_context_data(self, **kwargs):
        context = super(ForgotHtmlView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        next_url = self.request.META.get('HTTP_REFERER', None)
        if next_url:
            next_url = next_url + '?email=' + self.request.GET.get('email', '')
        context.update({
            'next_url': next_url,
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
            email_dict = {}
            email_dict.update({
                'email': email,
                'site': 'http://' + settings.SITE_DOMAIN + settings.STATIC_URL
            })
            next1 = request.POST.get('next', '')
            if user_exist.get('exists', ''):
                # task call for email
                send_email_task.delay(to_emails, mail_type, email_dict, status=None, oi=None)
                return HttpResponse(json.dumps({'exist': True, 'next': next1}), content_type="application/json")

            elif not user_exist.get('exists', ''):
                return HttpResponse(json.dumps({'notexist': True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'noresponse': True}), content_type="application/json")


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
                elif fb_user.get('response') == 400:
                    return HttpResponseRedirect('/login/')
            elif request.GET.get('key') == 'gplus':
                gplus_user = RegistrationLoginApi.social_login(request.GET)
                if gplus_user.get('response'):
                    candidateid = gplus_user['user_details']['candidate_id']
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=candidateid)
                    request.session.update(resp_status)
                    return HttpResponseRedirect(self.success_url)
                elif gplus_user.get('response') == 400:
                    return HttpResponseRedirect('/login/')
        except Exception as e:
            logging.getLogger('error_log').error('unable to do social login%s'%str(e))
            return HttpResponseRedirect('/login/')


class LinkedinLoginView(View):

    def get(self, request, *args, **kwargs):
        try:
            print(request.GET)
            credential = request.GET.get('credential', '')
            if credential == '1':
                client_id = settings.LINKEDIN_DICT.get('CLIENT_ID', '')
                request.session['linkedin_client_id'] = client_id
            else:
                client_id = settings.CLIENT_ID
            logging.getLogger('info_log').error('unable to do linked login%s' % str(e))
            request.session['next_url'] = request.GET.get('next', '')
            request.session['mobile_code'] = request.GET.get('country_code', '91')
            request.session['mobile'] = request.GET.get('mobile', '')

            params = {
                'client_id': client_id,
                'redirect_uri': settings.REDIRECT_URI,
                'response_type': 'code',
                'scope': settings.SCOPE,
                'state': settings.STATE,
            }
            url = settings.OAUTH_URL + urllib.parse.urlencode(params)
            return HttpResponseRedirect(url)
        except Exception as e:
            logging.getLogger('error_log').error('unable to do linked login%s'%str(e))

            raise e


class LinkedinCallbackView(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):

        linkedin_client_id = request.session.get('linkedin_client_id', '')

        if linkedin_client_id and linkedin_client_id == settings.LINKEDIN_DICT.get('CLIENT_ID'):
            client_id = settings.LINKEDIN_DICT.get('CLIENT_ID', '')
            client_secret = settings.LINKEDIN_DICT.get('CLIENT_SECRET', '')
        else:
            client_id = settings.CLIENT_ID
            client_secret = settings.CLIENT_SECRET

        self.success_url = request.session.get('next_url') if request.session.get('next_url') else '/'
        country_code = request.session.get('mobile_code', '91')
        mobile = request.session.get('mobile')
        if request.session.get('next_url'):
            del request.session['next_url']

        if request.session.get('mobile_code'):
            del request.session['mobile_code']

        if request.session.get('mobile'):
            del request.session['mobile']

        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code') if 'code' in request.GET else '',
            'redirect_uri': settings.REDIRECT_URI,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        if not params['code']:
            return HttpResponseRedirect('/login/')
        params = urllib.parse.urlencode(params)
        try:
            info = urllib.request.urlopen(
                settings.TOKEN_URL, params.encode("utf-8"))
            read_data = info.read()
            # convert byte object into string
            str_data = str(read_data, 'utf-8')
            data_dict = json.loads(str_data)
            data_dict.update({'key': 'linkedin'})
            linkedin_user = RegistrationLoginApi.social_login(data_dict)
            logging.getLogger('info_log').error('Response Received from shine for linkedin login: {}'.format(linkedin_user))
            if linkedin_user.get('response'):
                logging.getLogger('info_log').info(linkedin_user)
                if linkedin_user.get('user_details'):
                    candidateid = linkedin_user['user_details']['candidate_id']
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=candidateid)
                    request.session.update(resp_status)
                    return HttpResponseRedirect(self.success_url)
                elif linkedin_client_id == settings.LINKEDIN_DICT.get('CLIENT_ID') and not mobile:
                    url = '/login/' + '?next=' + self.success_url + '&linkedin=true' + '&linkedin_mobile=true'
                    return HttpResponseRedirect(url)
                elif linkedin_client_id == settings.LINKEDIN_DICT.get('CLIENT_ID') and mobile and linkedin_user.get('prefill_details'):
                    prefill_details = linkedin_user.get('prefill_details', {})
                    email = prefill_details.get('email')
                    if email:
                        register_data = {
                            'email': email,
                            'cell_phone': mobile,
                            'country_code': country_code,
                            'sms_alert_flag': 0,
                            'is_job_seeker': False,  # flag set false for Career Plus Registration (won't receive shine mails)
                            'user_type': 14,
                            'vendor_id': settings.CP_VENDOR_ID
                        }
                        reg_res = RegistrationLoginApi.auto_registration(register_data)
                        if reg_res and reg_res.get('id'):
                            candidateid = reg_res.get('id')
                            resp_status = ShineCandidateDetail().get_status_detail(
                                email=None, shine_id=candidateid)
                            if resp_status:
                                request.session.update(resp_status)
                            else:
                                logging.getLogger('error_log').error('Did not receive correct response from shine.com '
                                                                     'for candidate status api')
                            return HttpResponseRedirect(self.success_url)

            elif linkedin_user['status_code'] == 400:
                return HttpResponseRedirect('/login/')

        except Exception as e:
            logging.getLogger('error_log').error('unable to do linked in callback view %s'%str(e))

            return HttpResponseRedirect('/login/')


# HTTP Error 404
def page_not_found(request):
    response = render(request, 'error_pages/404.html', {})
    response.status_code = 404
    return response


# HTTP Error 500
def server_error(request):
    response = render(request, 'error_pages/500.html', {})
    response.status_code = 500
    return response


class GenerateWriterInvoiceView(View):

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated():
                data = WriterInvoiceMixin().save_writer_invoice_pdf(
                    user=user)
                if data.get('error'):
                    messages.add_message(
                        request, messages.ERROR,
                        data.get('error'))
                else:
                    messages.add_message(
                        request, messages.SUCCESS,
                        'Your invoice has generated, please download.')
        except Exception as e:
            logging.getLogger(
                'error_log').error(
                'writer invoice generation error - ' + str(e))
        return HttpResponseRedirect(reverse('console:dashboard'))


class DownloadWriterInvoiceView(View):
    def get(self, request, *args, **kwargs):
        try:
            import os
            user = request.user
            invoice = None
            if user.is_authenticated() and user.userprofile and user.userprofile.user_invoice:
                invoice = user.userprofile.user_invoice
            if invoice:
                file_path = invoice.name
                if not settings.IS_GCP:
                    file_path = os.path.join(settings.MEDIA_ROOT, invoice.name)
                    fsock = FileWrapper(open(file_path, 'rb'))
                else:
                    fsock = GCPInvoiceStorage().open(file_path)
                filename = invoice.name.split('/')[-1]
                response = HttpResponse(
                    fsock,
                    content_type=mimetypes.guess_type(filename)[0])
                response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                return response
        except Exception as e:
            logging.getLogger(
                'error_log').error(
                'writer invoice download error - ' + str(e))
        return HttpResponseRedirect(reverse('console:dashboard'))
