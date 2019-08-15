import datetime

from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
import logging
from order.models import OrderItem
from blog.mixins import PaginationMixin
from console.order_form import (
    MessageForm,
    OIFilterForm,
    VendorFileUploadForm,
    OIActionForm,)


@method_decorator(permission_required('order.can_show_partner_inbox_queue', login_url='/console/login/'), name='dispatch')
class PartnerInboxQueueView(ListView, PaginationMixin):
    context_object_name = 'inbox_list'
    template_name = 'console/partner/partner-inbox.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.modified = '', ''
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.sel_opt = request.GET.get('rad_search', 'number')
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        return super(PartnerInboxQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerInboxQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['inbox_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        var = self.sel_opt
        initial = {"modified": self.modified, "payment_date": self.payment_date}
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "draft_form": VendorFileUploadForm(),
            "action_form": OIActionForm(queue_name="partnerinbox"),
            var: 'checked',
        })
        return context

    def get_queryset(self):
        queryset = super(PartnerInboxQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            product__type_flow__in=[2, 6, 9, 10, 14, 16],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65]).exclude(
            oi_status__in=[4, 10, 81, 161, 162, 163])
        user = self.request.user
        if user.is_superuser:
            pass
        else:
            vendor_employee_list = user.employees.filter(active=True).values_list('vendee', flat=True)  # user's associated vendor ids
            vendor_employee_list = list(vendor_employee_list)
            queryset = queryset.filter(Q(partner__in=vendor_employee_list) |
                Q(product__vendor__in=vendor_employee_list))


        try:
            if self.query:
                if self.sel_opt == 'id':
                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.filter(product__name__icontains=self.query)
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)


        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s'%str(e))
            pass

        try:
            if self.modified:
                date_range = self.modified.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    modified__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset with date range %s'%str(e))
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
        
        except Exception as e:
            logging.getLogger('error_log').error('unable to get order payment queryset with date range %s'%str(e))
            pass

        return queryset.select_related('order', 'product').order_by('-modified')


@method_decorator(permission_required('order.can_show_hold_orderitem_queue', login_url='/console/login/'), name='dispatch')
class PartnerHoldQueueView(ListView, PaginationMixin):
    context_object_name = 'hold_list'
    template_name = 'console/partner/partner-hold.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.modified = '', ''
        self.sel_opt ='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        self.sel_opt = request.GET.get('rad_search','number')
        return super(PartnerHoldQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerHoldQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['hold_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {"modified": self.modified, "payment_date": self.payment_date}
        filter_form = OIFilterForm(initial)
        var = self.sel_opt
        context.update({
            "messages": alert,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(queue_name="partnerholdqueue"),
            var:'checked',
        })
        return context

    def get_queryset(self):
        queryset = super(PartnerHoldQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, oi_status=10,
            no_process=False,
            product__type_flow__in=[2, 6, 9, 10, 14, 16],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        user = self.request.user
        if user.is_superuser:
            pass
        else:
            vendor_employee_list = user.employees.filter(active=True).values_list('vendee', flat=True)  # user's associated vendor ids
            vendor_employee_list = list(vendor_employee_list)
            queryset = queryset.filter(Q(partner__in=vendor_employee_list) |
                Q(product__vendor__in=vendor_employee_list))

        try:
            if self.query:

                if self.sel_opt == 'id':

                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.filter(product__name__icontains=self.query)
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))

            pass

        try:
            if self.modified:
                date_range = self.modified.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    modified__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset with date range%s' % str(e))


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
        except Exception as e:
            logging.getLogger('error_log').error('unable to get order payment queryset with date range %s' % str(e))

            pass

        return queryset.select_related('order', 'product').order_by('-modified')


@method_decorator(permission_required('order.can_show_varification_report_queue', login_url='/console/login/'), name='dispatch')
class PartnerVarificationQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/partner/partner-varification-report.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.modified = '', ''
        self.sel_opt ='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        self.sel_opt=request.GET.get('rad_search','number')
        return super(PartnerVarificationQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerVarificationQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        var=self.sel_opt
        initial = {"modified": self.modified, "payment_date": self.payment_date}
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "draft_form": VendorFileUploadForm(),
            "action_form": OIActionForm(queue_name="partnerinbox"),
             var: 'checked',
        })
        return context

    def get_queryset(self):
        queryset = super(PartnerVarificationQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=81, product__type_flow=6,
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
        user = self.request.user
        if user.is_superuser:
            pass
        else:
            vendor_employee_list = user.employees.filter(active=True).values_list('vendee', flat=True)  # user's associated vendor ids
            queryset = queryset.filter(Q(partner__in=vendor_employee_list) |
                Q(product__vendor__in=vendor_employee_list))


        try:
            if self.query:
                if self.sel_opt == 'number':
                        queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'id':
                        queryset = queryset.filter(id__iexact=self.query)

                elif self.sel_opt == 'mobile':
                        queryset = queryset.filter(order__mobile__iexact=self.query)

                elif self.sel_opt == 'email':
                        queryset = queryset.filter(order__email__iexact=self.query)

                elif self.sel_opt == 'product':
                        queryset = queryset.filter(product__name__icontains=self.query)

        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))


        try:
            if self.modified:
                date_range = self.modified.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    modified__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))

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
        except Exception as e:
            logging.getLogger('error_log').error('unable to get order payment queryset within date range %s' % str(e))

            pass

        return queryset.select_related('order', 'product').order_by('-modified')