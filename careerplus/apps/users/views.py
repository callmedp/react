import json
import requests

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import (HttpResponse,
    HttpResponseRedirect)
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse
from shine.core import ShineToken, ShineCandidateDetail

from .forms import UserCreateForm, LoginForm, RegistrationForm, LoginApiForm
from .mixins import RegistrationLoginApi


class CreateUserView(FormView):
    template_name = 'users/register.html'
    http_method_names = [u'get', u'post']
    success_url = '/'
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert,
            'form': self.get_form()
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_obj = form.save(request, commit=True)
            messages.add_message(request, messages.SUCCESS, 'User registered successfully.')
            return HttpResponseRedirect(self.get_success_url())
        form = self.get_form()
        return render(request, self.template_name, {'form': form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = "/dashboard/"

    def get_context(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_error(self, user):
        error_message = None
        if user is None:
            error_message = "Username and Password do not match"
        elif not user.is_active:
            error_message = "Your account is not active"
        return error_message

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = self.request.POST.get('remember_me', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                if remember_me:
                    self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                return HttpResponseRedirect(self.success_url)
        error_msg = self.form_error(user)
        if error_msg is not None:
            messages.add_message(self.request, messages.SUCCESS, error_msg)
            return render(self.request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET.get(
                    'next', self.success_url))
            return HttpResponseRedirect(self.success_url)
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

       
class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class DashboardView(TemplateView):
    template_name = "users/loginsuccess.html"

    def get_context(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, args, **kwargs)


class RegistrationApiView(FormView):
    template_name = 'users/register.html'
    http_method_names = [u'get', u'post']
    success_url = '/'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        form = self.get_form()
        context.update({
            'messages': alert,
            'form': form
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        login_dict, post_data = {}, {}

        post_data.update({
            "email": request.POST.get('email'),
            "raw_password": request.POST.get('raw_password'),
            "cell_phone": request.POST.get('cell_phone'),
            "country_code": request.POST.get('country_code'),
            "vendor_id": request.POST.get('vendor_id'),
        })
        user_resp = RegistrationLoginApi().user_registration(post_data)

        if user_resp['response'] == 'new_user':
            login_dict.update({
                "email": request.POST.get('email'),
                "password": request.POST.get('password') if request.POST.get('password') else request.POST.get('raw_password'),
            })
            resp = RegistrationLoginApi().user_login(login_dict)
            
            if resp['response'] == 'login_user':
                resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=resp['candidate_id'])
                request.session.update(resp_status)
                return HttpResponseRedirect(reverse('dashboard'))

        elif user_resp['response'] == 'exist_user':
            messages.add_message(self.request, messages.SUCCESS, user_resp["non_field_errors"][0])
            return HttpResponseRedirect(reverse('login'))

        elif user_resp['response'] == 'form_error':
            return render(self.request, self.template_name, {'form': form})


class LoginApiView(FormView):
    form_class = LoginApiForm
    template_name = "users/login.html"
    success_url = "/dashboard/"

    def get_context(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        login_dict = {}
        remember_me = self.request.POST.get('remember_me', None)

        login_dict.update({
                "email": self.request.POST.get('email'),
                "password": self.request.POST.get('password')
            })

        user_exist = RegistrationLoginApi().check_email_exist(login_dict['email'])
        import ipdb; ipdb.set_trace()
        if user_exist['exists'] == True:
            login_resp = RegistrationLoginApi().user_login(login_dict)

            if login_resp['response'] == 'login_user':
                resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=login_resp['candidate_id'])
                self.request.session.update(resp_status)

                if remember_me:
                    self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year
                return HttpResponseRedirect(self.success_url)
            elif login_resp['response'] == 'error_pass':
                messages.add_message(self.request, messages.SUCCESS, login_resp["non_field_errors"][0])
                return render(self.request, self.template_name, {'form': form})

        elif user_exist['exists'] == False:
            messages.add_message(self.request, messages.SUCCESS, "User have No Account")
            return render(self.request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET.get(
                    'next', self.success_url))
            return HttpResponseRedirect(self.success_url)
        else:
            return super(LoginApiView, self).dispatch(request, *args, **kwargs)


class LogoutApiView(TemplateView):

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect(reverse('register'))

