import logging
import datetime

from django.views.generic import (
    TemplateView, ListView, DetailView, View, UpdateView)
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model


from order.models import Order
from blog.mixins import PaginationMixin
from console.decorators import (
    Decorate,
    stop_browser_cache,
    check_group
)

from console.welcome_form import WelcomeCallActionForm
from console.order_form import (
    OrderFilterForm,
)


@Decorate(stop_browser_cache())
class WelcomeQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/welcome-queue.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 30
        self.query = ''
        self.payment_date, self.created = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        return super(WelcomeQueueView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            order_list = request.POST.getlist('table_records', [])
            action_type = int(request.POST.get('action_type', '0'))
            order_objs = Order.objects.filter(id__in=order_list)
            if action_type == 0:
                messages.add_message(request, messages.ERROR, 'Please select valid action first')
            elif action_type == 1:
                for obj in order_objs:
                    obj.welcome_call_done = True
                    obj.save()
                messages.add_message(request, messages.SUCCESS, str(len(order_objs)) + ' welcome calls are done.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

        return HttpResponseRedirect(reverse('console:queue-welcome'))

    def get_context_data(self, **kwargs):
        context = super(WelcomeQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "created": self.created,
        }
        filter_form = OrderFilterForm(initial)
        context.update({
            "action_form": WelcomeCallActionForm(),
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeQueueView, self).get_queryset()
        queryset = queryset.filter(status=1, welcome_call_done=False)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(number__iexacts=self.query) |
                    Q(email__iexacts=self.query) |
                    Q(mobile__iexacts=self.query) |
                    Q(id__iexacts=self.query))
        except:
            pass

        try:
            if self.payment_date:
                date_range = self.payment_date.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    payment_date__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.order_by('payment_date')