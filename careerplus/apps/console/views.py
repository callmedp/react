#python imports
import logging,urllib
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
from users.tasks import send_forgot_password_mail_to_user


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

    def get_response_for_forgot_password_flow(self,username):
        user = User.objects.filter(email=username,is_active=True).first()
        if not user:
            messages.add_message(
                self.request,messages.ERROR,'Provided username does not exist or is not active.')
            return HttpResponseRedirect(reverse_lazy('console:login'))

        user.alt = user.generate_alt()
        user.save()
        send_forgot_password_mail_to_user.delay(user.id)
        messages.add_message(
                self.request,messages.INFO,'Please check your mailbox for further instructions.')
        return HttpResponseRedirect(reverse_lazy('console:login')) 


    def post(self, request):
        username = request.POST['username']
        password = request.POST.get('password','')
        forgot_password_flow = request.POST.get('forgot_password_flow')

        if forgot_password_flow:
            return self.get_response_for_forgot_password_flow(username)

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
        
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'));
        
        return HttpResponseRedirect(reverse_lazy('console:login'))


class ConsoleResetPasswordView(TemplateView):
    template_name = "console/reset_password.html"
    success_url = '/console/'

    def get(self,request,*args,**kwargs):
        if not request.GET.get('alt'):
            return HttpResponseRedirect("/console/")

        alt = request.GET.get('alt','')
        alt = alt.replace(" ","+")
        user_obj = User.objects.filter(alt=alt).first()
        
        if not user_obj:
            messages.error(request, 'This link has expired')
            return HttpResponseRedirect("/console/")

        return super(ConsoleResetPasswordView,self).get(request,*args,**kwargs)

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        alt = request.POST.get('alt','')
        alt = alt.replace(" ","+")

        if not alt:
            return HttpResponseRedirect("/console/")

        if password != re_password:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect("/console/reset-password/?alt={}".format(alt))

        user_obj = User.objects.filter(alt=alt).first()
        
        if not user_obj:
            messages.error(request, 'This link has expired')
            return HttpResponseRedirect("/console/")

        user_obj.set_password(password)
        user_obj.alt = ""
        user_obj.save()

        messages.info(request, 'Password has been successfully updated')
        return HttpResponseRedirect("/console/")


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
