from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import (HttpResponse,
    HttpResponseRedirect)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView, View
from .forms import UserCreateForm, LoginForm


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


class LogoutView(View):

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