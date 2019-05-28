#python imports
import logging
from datetime import datetime

#django imports
from django.views.generic import View, TemplateView, FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout

#local imports
from .forms import PasswordResetRequestForm, SetConfirmPasswordForm

#inter app imports

#third party imports
from core.mixins import TokenGeneration
from users.models import User


class ConsoleDashboardView(TemplateView):
    template_name = 'console/dashboard.html'
    success_url = reverse_lazy('ConsoleDashboardView')

    def get_context_data(self, **kwargs):
        if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
            kwargs['is_vendee'] = True
            kwargs['vendor_id'] = self.request.user.vendor_set.all()[0].id
        if self.request.user and self.request.user.is_staff:
            kwargs['is_admin'] = True
        context = super(ConsoleDashboardView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(ConsoleDashboardView, self).get(
                request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('console:login'))


class ConsoleLoginView(TemplateView):
    template_name = 'console/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('console:dashboard'))
        return super(ConsoleLoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsoleLoginView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session.set_expiry(settings.CONSOLE_SESSION_TIMEOUT)
            login(request, user)
            user.last_login = datetime.now()
            user.save()
            logging.getLogger('info_log').info("Console Login Record - {}, {}, {}".\
                format(user.email,user.name,user.last_login))
            return HttpResponseRedirect(reverse_lazy('console:dashboard'))
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Username or Password does not match.')
            return HttpResponseRedirect(reverse_lazy('console:login'))


class ConsoleLogoutView(View):
    template_name = 'console/login.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('console:login'))


class ConsoleForgotPasswordView(FormView):
    template_name = "console/forget_password.html"
    form_class = PasswordResetRequestForm
    success_url = '/console/forgot-password/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(email=data)
                email_dict = {
                'subject': "User Reset Password",
                'from': settings.DEFAULT_FROM_EMAIL,
                'to': [user.email],
                'email_type': 6,
                'email': user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'Careerplus Sales CRM',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'username': user.email,
                'token': default_token_generator.make_token(user),
                'protocol': 'http://',
                }
                send_email_change_user_password.delay(email_dict)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
                return result
            except Exception as e:
                logging.getLogger('error_log').error('unable to send forgotpassword email %s' % str(e))
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
        return self.form_invalid(form)


class ConsolePasswordResetView(FormView):
    template_name = "console/reset_password.html"
    success_url = '/console/'
    form_class = SetConfirmPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


class ConsoleAutoLoginView(View):

    def get(self, request, *args, **kwargs):
        valid = False
        email = None
        try:
            email, enc_type, valid = TokenGeneration().decode(
                request.GET.get("token")
            )
        except Exception as e:
            pass
        user = User.objects.filter(email=email).first()

        if valid and user and enc_type == 2:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('console:dashboard'))
        else:
            messages.add_message(
                self.request, messages.ERROR,
                "Token has been expired. Login with Username/Password "
            )
        return HttpResponseRedirect(reverse_lazy('console:login'))
