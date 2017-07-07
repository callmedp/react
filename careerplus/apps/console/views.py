from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout


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
            login(request, user)
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
