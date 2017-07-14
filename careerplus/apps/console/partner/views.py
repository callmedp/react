import datetime

from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from order.models import OrderItem
from blog.mixins import PaginationMixin
from console.order_form import (
    MessageForm,
    OIFilterForm,
    VendorFileUploadForm,
    OIActionForm,)


class PartnerInboxQueueView(ListView, PaginationMixin):
    context_object_name = 'inbox_list'
    template_name = 'console/partner/partner-inbox.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.updated_on = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.updated_on = request.GET.get('updated_on', '')
        return super(PartnerInboxQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerInboxQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['inbox_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {"updated_on": self.updated_on, "payment_date": self.payment_date}
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "draft_form": VendorFileUploadForm(),
            "action_form": OIActionForm(queue_name="partnerinbox"),
        })
        return context

    def get_queryset(self):
        queryset = super(PartnerInboxQueueView, self).get_queryset()
        queryset = queryset.filter(order__status=1, no_process=False, product__type_flow__in=[2, 6, 10]).exclude(oi_status__in=[4, 10])

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass

        try:
            if self.updated_on:
                date_range = self.updated_on.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    updated_on__range=[start_date, end_date])
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
                    order__payment_date__range=[start_date, end_date])
        except:
            pass

        return queryset.select_related('order', 'product')


class PartnerHoldQueueView(ListView, PaginationMixin):
    context_object_name = 'hold_list'
    template_name = 'console/partner/partner-hold.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.updated_on = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.updated_on = request.GET.get('updated_on', '')
        return super(PartnerHoldQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerHoldQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['hold_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {"updated_on": self.updated_on, "payment_date": self.payment_date}
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "draft_form": FileUploadForm(),
            "action_form": OIActionForm(queue_name="partnerholdqueue"),
        })
        return context

    def get_queryset(self):
        queryset = super(PartnerHoldQueueView, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=10, no_process=False, product__type_flow__in=[2, 6, 10])

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass

        try:
            if self.updated_on:
                date_range = self.updated_on.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    updated_on__range=[start_date, end_date])
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
                    order__payment_date__range=[start_date, end_date])
        except:
            pass

        return queryset.select_related('order', 'product')