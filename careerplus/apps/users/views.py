import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse
from shine.core import ShineCandidateDetail

from .forms import RegistrationForm, LoginApiForm
from .mixins import RegistrationLoginApi


class DashboardView(TemplateView):
    template_name = "users/loginsuccess.html"

    def get_context(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return super(DashboardView, self).get(request, args, **kwargs)


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
