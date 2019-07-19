import json
import csv
import datetime
import math
import logging
import mimetypes
import textwrap

from io import StringIO
from dateutil import relativedelta
from wsgiref.util import FileWrapper
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    TemplateView, ListView, DetailView, View, UpdateView)
from django.core.paginator import Paginator
from django.db.models import Q, Count, Case, When, IntegerField, Value
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.forms import modelformset_factory
from django.template.response import TemplateResponse

from geolocation.models import Country
from order.models import Order, OrderItem, InternationalProfileCredential, OrderItemOperation
from shop.models import DeliveryService, Product, JobsLinks
from blog.mixins import PaginationMixin
from emailers.email import SendMail
from emailers.tasks import send_email_task, send_booster_recruiter_mail_task
from emailers.sms import SendSMS
from core.mixins import TokenExpiry
from payment.models import PaymentTxn
from linkedin.autologin import AutoLogin
from order.functions import send_email, date_timezone_convert, create_short_url
from .schedule_tasks.tasks import generate_compliance_report
from scheduler.models import Scheduler

from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from review.models import Review
from partner.models import BoosterRecruiter
from shop.choices import S_ATTR_DICT, A_ATTR_DICT
from partner.models import BoosterRecruiter,VendorHierarchy

from .decorators import (
    Decorate,
    stop_browser_cache,
    check_group
)
from .welcome_form import WelcomeCallActionForm
from .order_form import (
    ResumeUploadForm,
    InboxActionForm,
    FileUploadForm,
    MessageForm,
    OrderFilterForm,
    OIFilterForm,
    OIActionForm,
    AssignmentActionForm,
    ReviewActionForm,
    ReviewFilterForm,
    ReviewUpdateForm,
    emailupdateform,
    mobileupdateform,
    ProductUserProfileForm,
    JobLinkForm)
from .mixins import ActionUserMixin
from users.mixins import UserPermissionMixin

@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_order_queue', login_url='/console/login/'), name='dispatch')
class OrderListView(ListView, PaginationMixin):
    context_object_name = 'order_list'
    template_name = 'console/order/order-list.html'
    model = Order
    http_method_names = [u'get', ]

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.payment_date, self.created = '', ''
        self.status = -1
        self.sel_opt = 'id'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        self.status = request.GET.get('status', -1)
        self.sel_opt = self.request.GET.get("rad_search",'id')
        return super(OrderListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['order_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {"payment_date": self.payment_date, "created": self.created, "status": self.status}
        filter_form = OrderFilterForm(initial)
        email_form=emailupdateform()
        mobil_form=mobileupdateform()
        context.update({
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
            var: "checked",
            'email_form': email_form,
            'mobil_form': mobil_form,

        })
        return context

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        user = self.request.user
        # excl_txns = PaymentTxn.objects.filter(status__in=[0, 2, 3, 4, 5], payment_mode__in=[6, 7])
        # excl_order_list = excl_txns.all().values_list('order__pk', flat=True)
        # queryset = queryset.exclude(id__in=excl_order_list)
        if user.has_perm('order.can_show_all_order'):
            queryset = queryset
        elif user.has_perm('order.can_show_paid_order'):
            queryset = queryset.filter(status=1)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                txns = PaymentTxn.objects.filter(txn__iexact=self.query)
                if txns.exists():
                    order_ids = list(txns.values_list('order__id', flat=True))
                    queryset = queryset.filter(id__in=order_ids)
                else:
                    if self.sel_opt == 'id':
                        if (self.query.strip())[:2] == 'cp' or (self.query.strip())[:2] == 'CP':
                            result = self.query.strip()[2:]
                            try:
                                queryset = queryset.filter(id__iexact=result)
                            except Exception as e:
                                queryset = queryset.none()
                                logging.getLogger('error_log').error(str(e))

                        else:
                            result = self.query.strip()
                            try:
                                queryset = queryset.filter(id__iexact=result)
                            except Exception as e:
                                queryset = queryset.none()
                                logging.getLogger('error_log').error(str(e))

                    elif self.sel_opt == 'mobile':
                        queryset = queryset.filter(mobile__iexact=self.query)

                    elif self.sel_opt == 'email':
                        result = self.query.strip()
                        queryset = queryset.filter(email__iexact=result)

        except Exception as e:
            queryset = queryset.none()
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if int(self.status) != -1:
                queryset = queryset.filter(status=self.status)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
        if queryset.exists():
            return queryset.order_by('-modified')
        else:
            return queryset.none()

# @Decorate(stop_browser_cache())
# @method_decorator(permission_required('order.can_show_welcome_queue', login_url='/console/login/'), name='dispatch')
#updated one is currently being used
# class WelcomeCallVeiw(ListView, PaginationMixin):
#     context_object_name = 'welcome_list'
#     template_name = 'console/order/welcome-list.html'
#     model = Order
#     http_method_names = [u'get', u'post']
#
#     def __init__(self):
#         self.page = 1
#         self.paginated_by = 50
#         self.query = ''
#         self.payment_date, self.created = '', ''
#
#     def get(self, request, *args, **kwargs):
#         self.page = request.GET.get('page', 1)
#         self.query = request.GET.get('query', '')
#         self.payment_date = request.GET.get('payment_date', '')
#         self.created = request.GET.get('created', '')
#         return super(WelcomeCallVeiw, self).get(request, args, **kwargs)
#
#     def post(self, request, *args, **kw
# args):
#         try:
#             order_list = request.POST.getlist('table_records', [])
#             action_type = int(request.POST.get('action_type', '0'))
#             order_objs = Order.objects.filter(id__in=order_list)
#             if action_type == 0:
#                 messages.add_message(request, messages.ERROR, 'Please select valid action first')
#             elif action_type == 1:
#                 for obj in order_objs:
#                     obj.welcome_call_done = True
#                     obj.save()
#                 messages.add_message(request, messages.SUCCESS, str(len(order_objs)) + ' welcome calls are done.')
#         except Exception as e:
#             messages.add_message(request, messages.ERROR, str(e))
#
#         return HttpResponseRedirect(reverse('console:queue-welcome'))
#
#     def get_context_data(self, **kwargs):
#         context = super(WelcomeCallVeiw, self).get_context_data(**kwargs)
#         paginator = Paginator(context['welcome_list'], self.paginated_by)
#         context.update(self.pagination(paginator, self.page))
#         alert = messages.get_messages(self.request)
#         initial = {
#             "payment_date": self.payment_date,
#             "created": self.created,
#         }
#         filter_form = OrderFilterForm(initial)
#         context.update({
#             "action_form": WelcomeCallActionForm(),
#             "messages": alert,
#             "filter_form": filter_form,
#             "query": self.query,
#         })
#
#         return context
#
#     def get_queryset(self):
#         queryset = super(WelcomeCallVeiw, self).get_queryset()
#         queryset = queryset.filter(status=1, welcome_call_done=False)
#
#         try:
#             if self.query:
#                 queryset = queryset.filter(
#                     Q(number__icontains=self.query) |
#                     Q(email__iexact=self.query) |
#                     Q(mobile__iexact=self.query) |
#                     Q(id__iexact=self.query))
#         except Exception as e:
#             logging.getLogger('error_log').error("%s " % str(e))
#             pass
#
#         try:
#             if self.payment_date:
#                 date_range = self.payment_date.split('-')
#                 start_date = date_range[0].strip()
#                 start_date = datetime.datetime.strptime(
#                     start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
#                 end_date = date_range[1].strip()
#                 end_date = datetime.datetime.strptime(
#                     end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
#                 queryset = queryset.filter(
#                     payment_date__range=[start_date, end_date])
#         except Exception as e:
#             logging.getLogger('error_log').error("%s " % str(e))
#             pass
#
#         try:
#             if self.created:
#                 date_range = self.created.split('-')
#                 start_date = date_range[0].strip()
#                 start_date = datetime.datetime.strptime(
#                     start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
#                 end_date = date_range[1].strip()
#                 end_date = datetime.datetime.strptime(
#                     end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
#                 queryset = queryset.filter(
#                     created__range=[start_date, end_date])
#         except Exception as e:
#             logging.getLogger('error_log').error("%s " % str(e))
#             pass
#
#         return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_midout_queue', login_url='/console/login/'), name='dispatch')
class MidOutQueueView(TemplateView, PaginationMixin):
    # context_object_name = 'midout_list'
    template_name = 'console/order/midout-list.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query, self.payment_date = '', ''
        self.sel_opt='id'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.sel_opt = request.GET.get('rad_search','id')
        self.payment_date = request.GET.get('payment_date', '')
        return super(MidOutQueueView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ResumeUploadForm(request.POST, request.FILES)
        obj_pk = request.POST.get('oi_pk', None)
        if form.is_valid():
            try:
                order = Order.objects.get(pk=obj_pk)
                orderitems = order.orderitems.filter(oi_status=2)  # filter(product__type_flow__in=[1])
                for oi in orderitems:
                    if not oi.oi_resume:
                        data = {
                            "candidate_resume": request.FILES.get('oi_resume', ''),
                        }

                        ActionUserMixin().upload_candidate_resume(
                            oi=oi, data=data, user=request.user)
                messages.add_message(request, messages.SUCCESS, 'resume uploaded Successfully')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            error_message = form.errors.get('oi_resume')
            if error_message:
                messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse("console:queue-midout"))

    def get_context_data(self, **kwargs):
        context = super(MidOutQueueView, self).get_context_data(**kwargs)
        midout_list = self.get_queryset()
        var = self.sel_opt
        paginator = Paginator(midout_list, self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
        }
        # has_permission = self.request.user.user_permissions.filter(codename='can_do_exotel_call')
        # show_btn = True if has_permission else False
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "form": ResumeUploadForm(),
            "query": self.query,
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name='midout'),
            var: "checked",
            # "show_btn":show_btn,
        })
        return context

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            'orderitems').filter(
            status=1, orderitems__oi_status=2,
            orderitems__no_process=False).distinct()
        # queryset = OrderItem.objects.all().select_related('order', 'product')
        # queryset = queryset.filter(
        #     order__status=1, no_process=False, oi_status=2)

        try:
            if self.query:
                if self.sel_opt == 'id':
                    if self.query[:2]=='cp' or self.query[:2]=='CP':
                        queryset=queryset.filter(number__iexact=self.query)
                    else:
                        queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                        queryset = queryset.filter(mobile__iexact=self.query)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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

        return queryset.order_by('-payment_date')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_inbox_queue', login_url='/console/login/'), name='dispatch')
class InboxQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'inbox_list'
    template_name = 'console/order/inbox-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.writer, self.created = '', ''
        self.delivery_type = ''
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.writer = request.GET.get('writer', '')
        self.created = request.GET.get('created', '')
        self.delivery_type = request.GET.get('delivery_type', '')
        self.sel_opt = request.GET.get('rad_search','number')
        return super(InboxQueueVeiw, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            data = {"display_message": ''}
            try:
                orderitem_list = request.POST.getlist('selected_id[]', [])
                writer_pk = int(request.POST.get('action_type', '0'))
                orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list).select_related('order')
                if writer_pk == 0:
                    data['display_message'] = 'Please select valid action first.'
                else:
                    User = get_user_model()
                    try:
                        writer = User.objects.get(pk=writer_pk)
                        ActionUserMixin().assign_orderitem(
                            orderitem_list=orderitem_list,
                            assigned_to=writer,
                            user=request.user,
                            data={})

                        data['display_message'] = str(len(orderitem_objs)) + ' orderitems are Assigned.'
                    except Exception as e:
                        data['display_message'] = str(e)
            except Exception as e:
                data['display_message'] = str(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(InboxQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['inbox_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created, "writer": self.writer,
            "delivery_type": self.delivery_type}
        filter_form = OIFilterForm(initial)

        context.update({
            "action_form": InboxActionForm(),
            "messages": alert,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            var: "checked",
        })
        return context

    def get_queryset(self):
        queryset = super(InboxQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            product__type_flow__in=[1, 3, 12, 13],
            oi_status__in=[5, 3],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        user = self.request.user
        if user.is_superuser:
            pass
        elif user.has_perm('order.writer_inbox_assigner'):
            queryset = queryset.filter(assigned_to__isnull=True)
        elif user.has_perm('order.writer_inbox_assignee'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()
        try:
            if self.query:
                if self.sel_opt == 'id':
                        queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt =='number':
                        queryset=queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt =='product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query)|
                                               Q(parent__isnull=False , parent__product__name__icontains=self.query))
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

        try:
            if self.writer:
                queryset = queryset.filter(assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related('order').order_by('-modified')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InboxQueueVeiw, self).dispatch(request, *args, **kwargs)


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_view_order_item_detail', login_url='/console/login/'), name='dispatch')
class OrderItemDetailVeiw(DetailView):
    model = OrderItem
    template_name = "console/order/order-item-detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(OrderItemDetailVeiw, self).get(request, *args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                last_status = obj.oi_status
                obj.oi_draft = request.FILES.get('file', '')
                if obj.oi_status == 26:
                    obj.draft_counter += 1
                elif not obj.draft_counter:
                        obj.draft_counter += 1
                obj.oi_status = 23  # pending Approval
                obj.last_oi_status = last_status
                obj.draft_added_on = timezone.now()
                obj.save()
                messages.add_message(request, messages.SUCCESS, 'draft uploaded Successfully')
                obj.orderitemoperation_set.create(
                    oi_draft=obj.oi_draft,
                    draft_counter=obj.draft_counter,
                    oi_status=22,
                    last_oi_status=last_status,
                    assigned_to=obj.assigned_to,
                    added_by=request.user)
                obj.orderitemoperation_set.create(
                    oi_status=obj.oi_status,
                    last_oi_status=22,
                    assigned_to=obj.assigned_to,
                    added_by=request.user)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            error_message = form.errors.get('file')
            if error_message:
                messages.add_message(request, messages.ERROR, error_message)

        return HttpResponseRedirect(reverse("console:order-item-detail", kwargs={'pk': obj.pk}))

    def get_context_data(self, **kwargs):
        context = super(OrderItemDetailVeiw, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        obj = self.get_object()
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        order = obj.order
        communications = obj.message_set.all().select_related('added_by')
        operations = obj.orderitemoperation_set.all().select_related('added_by', 'assigned_to')
        drafts = operations.filter(draft_counter__range=[1, max_limit_draft])
        context.update({
            "order": order,
            "max_limit_draft": max_limit_draft,
            "drafts": drafts,
            "draft_form": FileUploadForm(),
            "messages": alert,
            "message_form": MessageForm(),
            "communications": communications,
            "operations": operations,
        })
        return context


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_search_order_from_console', login_url='/console/login/'), name='dispatch')
class SearchOrderView(ListView, PaginationMixin):
    context_object_name = 'order_list'
    template_name = "console/order/order-search.html"
    model = Order
    http_method_names = [u'get', ]

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.payment_date, self.created = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        return super(SearchOrderView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchOrderView, self).get_context_data(**kwargs)
        paginator = Paginator(context['order_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
            "query": self.query,
        })
        return context

    def get_queryset(self):
        queryset = super(SearchOrderView, self).get_queryset()
        excl_txns = PaymentTxn.objects.filter(status__in=[0, 2, 3, 4, 5], payment_mode__in=[6, 7])
        excl_order_list = list(excl_txns.all().values_list('order__pk', flat=True))
        queryset = queryset.exclude(id__in=excl_order_list)
        queryset = queryset.filter(status=1)

        try:
            if self.query:
                q1 = queryset.filter(
                    Q(number=self.query) |
                    Q(email=self.query) |
                    Q(mobile=self.query))

                pay_txns = PaymentTxn.objects.filter(txn=self.query)
                order_pks = list(pay_txns.all().values_list('order__pk', flat=True))
                q2 = queryset.filter(id__in=order_pks)

                queryset = q1 | q2
                queryset = queryset.distinct()
            else:
                queryset = queryset.none()
                messages.add_message(self.request, messages.ERROR, 'Search not found any order.')
        except:
            queryset = queryset.none()
            messages.add_message(self.request, messages.ERROR, 'Search not found any order.')

        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_view_order_detail', login_url='/console/login/'), name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = "console/order/order-detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super(OrderDetailView, self).get(request, *args, **kwargs)

        #Redirect user if none of the items are visible
        if not self.context.get('orderitems'):
            logging.getLogger('info_log').info("Invalid data access {},{},{}".format(\
                request.user.id,request.user.get_full_name(),self.object.id))
            messages.add_message(self.request,messages.ERROR,'You are not authorised to view this order.')
            return HttpResponseRedirect("/console/")
        
        return response

    def _get_visible_order_items_for_order(self,order):
        order_items = order.orderitems.all().select_related('product', 'partner').order_by('id')
        
        #Handle vendor users
        vendor_ids = [x.vendee.id for x in VendorHierarchy.objects.filter(\
            employee=self.request.user,active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                    Q(product__vendor_id__in=vendor_ids))

        #Handle Writers
        if self.request.user.is_writer:
            order_items = order_items.filter(assigned_to=self.request.user)

        return order_items

    def get_context_data(self, **kwargs):
        last_status = ""
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = self.get_object()
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        last_status_object = order.welcomecalloperation_set.exclude(wc_status__in=[0, 1, 2])\
            .order_by('id').last()

        # has_permission = self.request.user.user_permissions.filter(codename='can_do_exotel_call')
        # show_btn = True if has_permission else False
        email_form = emailupdateform()
        mobil_form = mobileupdateform()
        
        if not last_status_object:
            last_status = "Not Done"
        else:
            timestamp = '\n' + date_timezone_convert(last_status_object.created).strftime('%b. %d, %Y, %I:%M %P ')
            last_status = last_status_object.get_wc_status()
            last_status += timestamp
        
        context.update({
            "order": order,
            "order_wc_status": last_status,
            'orderitems': list(self._get_visible_order_items_for_order(order)),
            "max_limit_draft": max_limit_draft,
            "messages": alert,
            "message_form": MessageForm(),
            "draft_form": FileUploadForm(),
            # "show_btn": show_btn,
            'email_form': email_form,
            'mobil_form': mobil_form,

        })
        self.context = context
        return context


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_approval_queue', login_url='/console/login/'), name='dispatch')
class ApprovalQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'approval_list'
    template_name = 'console/order/approval-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.modified, self.draft_level = '', -1
        self.writer, self.delivery_type = '', ''
        self.sel_opt= 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
        self.sel_opt=request.GET.get('rad_search','number')
        try:
            self.draft_level = int(request.GET.get('draft_level', -1))
        except:
            self.draft_level = -1
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(ApprovalQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApprovalQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['approval_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var=self.sel_opt
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT

        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = OIFilterForm(initial)

        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(),
             var: "checked",
        })
        return context

    def get_queryset(self):
        queryset = super(ApprovalQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=23,
            product__type_flow__in=[1, 3, 12, 13],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
        user = self.request.user
       
        if user.has_perm('order.can_view_all_approval_list'):
            pass
        elif user.has_perm('order.can_view_only_assigned_approval_list'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()
        try:
            if self.query:
                if self.sel_opt=='id':
                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt=='number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt== 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt== 'mobile':
                    queryset=queryset.filter(order__mobile__iexact=self.query)
                elif self.sel_opt=='email':
                    queryset=queryset.filter(order__email__iexact=self.query)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related(
            'order', 'product', 'assigned_by',
            'assigned_to', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_approved_queue', login_url='/console/login/'), name='dispatch')
class ApprovedQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'approved_list'
    template_name = 'console/order/approved-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.modified, self.draft_level = '', -1
        self.writer, self.delivery_type = '', ''
        self.sel_opt='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
        self.sel_opt=request.GET.get('rad_search','number')
        try:
            self.draft_level = int(request.GET.get('draft_level', -1))
        except:
            self.draft_level = -1
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(ApprovedQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApprovedQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['approved_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        var = self.sel_opt
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "query": self.query,
            "filter_form": filter_form,
             var: "checked",
        })
        return context

    def get_queryset(self):
        queryset = super(ApprovedQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=24, product__type_flow__in=[1, 3, 5, 12, 13],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
        user = self.request.user

        if user.has_perm('order.can_view_all_approved_list'):
            pass
        elif user.has_perm('order.can_view_only_assigned_approved_list'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        try:
            if self.query:

                if self.sel_opt== 'id':
                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt== 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt== 'number':
                    queryset=queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset=queryset.filter(order__mobile__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset=queryset.filter(order__email__iexact=self.query)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related(
            'order', 'product', 'assigned_by',
            'assigned_to', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_rejectedbyadmin_queue', login_url='/console/login/'), name='dispatch')
class RejectedByAdminQueue(ListView, PaginationMixin):
    context_object_name = 'rejectedbyadmin_list'
    template_name = 'console/order/rejectedbyadmin-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.modified, self.draft_level = '', -1
        self.writer, self.delivery_type = '', ''
        self.sel_opt ='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
        self.sel_opt =request.GET.get('rad_search','number')
        try:
            self.draft_level = int(request.GET.get('draft_level', -1))
        except:
            self.draft_level = -1
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(RejectedByAdminQueue, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RejectedByAdminQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbyadmin_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        var = self.sel_opt
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(),
            var:'checked',
        })
        return context

    def get_queryset(self):
        queryset = super(RejectedByAdminQueue, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=25, product__type_flow__in=[1, 3, 12, 13],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        user = self.request.user

        if user.has_perm('order.can_view_all_rejectedbyadmin_list'):
            pass
        elif user.has_perm('order.can_view_only_assigned_rejectedbyadmin_list'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                if self.sel_opt=='id':
                    queryset=queryset.filter(id__iexact=self.query)
                elif self.sel_opt=='product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt=='number':
                    queryset=queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt=='email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt== 'mobile':
                    queryset=queryset.filter(order__mobile=self.query)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        return queryset.select_related(
            'order', 'product', 'assigned_by',
            'assigned_to', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_rejectedbycandidate_queue', login_url='/console/login/'), name='dispatch')
class RejectedByCandidateQueue(ListView, PaginationMixin):
    context_object_name = 'rejectedbycandidate_list'
    template_name = 'console/order/rejectedbycandidate-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.modified, self.draft_level = '', -1
        self.writer, self.delivery_type = '', ''
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
        self.sel_opt = request.GET.get('rad_search','number')
        try:
            self.draft_level = int(request.GET.get('draft_level', -1))
        except:
            self.draft_level = -1
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(RejectedByCandidateQueue, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RejectedByCandidateQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbycandidate_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        var = self.sel_opt
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(),
            var:'checked',
        })
        return context

    def get_queryset(self):
        queryset = super(RejectedByCandidateQueue, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=26, product__type_flow__in=[1, 3, 12, 13],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        user = self.request.user

        if user.has_perm('order.can_view_all_rejectedbycandidate_list'):
            pass
        elif user.has_perm('order.can_view_only_assigned_rejectedbycandidate_list'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        try:

            if self.query:

                if self.sel_opt == 'id':
                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related(
            'order', 'product', 'assigned_by',
            'assigned_to', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_allocated_queue', login_url='/console/login/'), name='dispatch')
class AllocatedQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'allocated_list'
    template_name = 'console/order/allocated-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.writer, self.created, self.delivery_type = '', '', ''
        self.oi_status = -1
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.sel_opt=request.GET.get('rad_search','number')
        self.writer = request.GET.get('writer', '')
        self.created = request.GET.get('created', '')
        self.oi_status = request.GET.get('oi_status', '')
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(AllocatedQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AllocatedQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['allocated_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "writer": self.writer,
            "oi_status": self.oi_status,
            "delivery_type": self.delivery_type}
        filter_form = OIFilterForm(initial)
        context.update({
            "assignment_form": AssignmentActionForm(queue_name='allocatedqueue'),
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
            var: 'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(AllocatedQueueVeiw, self).get_queryset()

        queryset = queryset.filter(
            order__status__in=[1, 3],
            no_process=False,
            product__type_flow__in=[1, 12, 13, 8, 3],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65]).exclude(
            oi_status=4)
        # user = self.request.user

        # if user.has_perm('order.can_view_all_allocated_list'):
        #     pass
        # elif user.has_perm('order.can_view_only_assigned_allocated_list'):
        #     queryset = queryset.filter(assigned_to=user)
        # else:
        #     queryset = queryset.none()

        try:
            if self.query:
                if self.sel_opt == 'id':
                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)
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

        try:
            if self.writer:
                queryset = queryset.filter(assigned_to=self.writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if int(self.oi_status) != -1:
                queryset = queryset.filter(oi_status=self.oi_status)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related(
            'order', 'product', 'assigned_to',
            'assigned_by', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_closed_oi_queue', login_url='/console/login/'), name='dispatch')
class ClosedOrderItemQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'closed_oi_list'
    template_name = 'console/order/closed-oi-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.payment_date, self.created = '', ''
        self.sel_opt ='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        self.sel_opt=request.GET.get('rad_search','number')
        return super(ClosedOrderItemQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClosedOrderItemQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['closed_oi_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var =self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "payment_date": self.payment_date, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
            var:'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(ClosedOrderItemQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3], oi_status=4,
            no_process=False)
        user = self.request.user
        vendor_employee_list = list(user.employees.filter(active=True).values_list('vendee', flat=True))  # user's associated vendor ids

        if user.has_perm('order.can_view_all_closed_oi_list'):
            pass
        elif user.has_perm('order.can_view_only_assigned_closed_oi_list'):
            queryset = queryset.filter(assigned_to=user)
        elif vendor_employee_list:
            queryset = queryset.filter(Q(partner__in=vendor_employee_list) |
                Q(product__vendor__in=vendor_employee_list))
        else:
            queryset = queryset.none()

        try:
            if self.query:

                if self.sel_opt == 'id':

                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related(
            'order', 'product', 'assigned_to',
            'assigned_by', 'delivery_service').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_domestic_profile_update_queue', login_url='/console/login/'), name='dispatch')
class DomesticProfileUpdateQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/domestic-profile-update-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.payment_date, self.modified = '', ''
        self.sel_opt='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.sel_opt=request.GET.get('rad_search','number')
        self.modified = request.GET.get('modified', '')
        return super(DomesticProfileUpdateQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomesticProfileUpdateQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var=self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "modified": self.modified, }
        filter_form = OIFilterForm(initial)
        context.update({
            "assignment_form": AssignmentActionForm(),
            "messages": alert,
            "query": self.query,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name="domesticprofileupdate"),
            var:'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(DomesticProfileUpdateQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3],
            product__type_flow=5, no_process=False,
            oi_status__in=[5, 25, 61],
            product__sub_type_flow__in=[501, 503],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
        # queryset = queryset.exclude(oi_resume__isnull=True).exclude(oi_resume__exact='')
        user = self.request.user

        q1 = queryset.filter(oi_status=61)
        exclude_list = []
        for oi in q1:
            closed_ois = oi.order.orderitems.filter(product__type_flow=1, oi_status=4, no_process=False)
            if closed_ois.exists():
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.last_oi_status = last_oi_status
                oi.oi_draft = closed_ois[0].oi_draft
                oi.draft_counter += 1
                oi.draft_added_on = timezone.now()
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    oi_draft=oi.oi_draft,
                    draft_counter=oi.draft_counter,
                    assigned_to=oi.assigned_to)
            else:
                exclude_list.append(oi.pk)

        queryset = queryset.exclude(id__in=exclude_list)
        if user.is_superuser:
            pass
        elif user.has_perm('order.domestic_profile_update_assigner'):
            queryset = queryset.filter(assigned_to=None)
        elif user.has_perm('order.domestic_profile_update_assignee'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                if self.sel_opt == 'number':
                    if self.query[:2] == 'cp' or self.query[:2] == 'CP':
                        queryset = queryset.filter(order__number__iexact=self.query)
                    else:
                        queryset=queryset.none()
                elif self.sel_opt == 'id':
                        queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')

@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_domestic_profile_initiated_queue', login_url='/console/login/'), name='dispatch')
class DomesticProfileInitiatedQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/domestic-profile-initiated-list.html'
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
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.sel_opt = request.GET.get('rad_search','number')
        self.modified = request.GET.get('modified', '')
        self.status = request.GET.get('status', '')
        return super(DomesticProfileInitiatedQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomesticProfileInitiatedQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "modified": self.modified, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
            var: 'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(DomesticProfileInitiatedQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3],
            product__type_flow=5, no_process=False,
            oi_status__in=[28, 4],
            product__sub_type_flow__in=[501, 503],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
        # queryset = queryset.exclude(oi_resume__isnull=True).exclude(oi_resume__exact='')
        user = self.request.user

        q1 = queryset.filter(oi_status=61)
        exclude_list = []
        for oi in q1:
            closed_ois = oi.order.orderitems.filter(product__type_flow=1, oi_status=4, no_process=False)
            if closed_ois.exists():
                last_oi_status = oi.oi_status
                oi.oi_status = 5
                oi.last_oi_status = last_oi_status
                oi.oi_draft = closed_ois[0].oi_draft
                oi.draft_counter += 1
                oi.draft_added_on = timezone.now()
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    oi_draft=oi.oi_draft,
                    draft_counter=oi.draft_counter,
                    assigned_to=oi.assigned_to)
            else:
                exclude_list.append(oi.pk)

        queryset = queryset.exclude(id__in=exclude_list)

        if not user.is_superuser:
            queryset = queryset.filter(assigned_to=user)

        try:
            if self.query:
                if self.sel_opt == 'number':
                    if self.query[:2] == 'cp' or self.query[:2] == 'CP':
                        queryset = queryset.filter(order__number__iexact=self.query)
                    else:
                        queryset = queryset.none()
                elif self.sel_opt == 'id':
                        queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        try:
            if self.status:
                queryset = queryset.filter(
                    oi_status=int(self.status))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_domestic_profile_approval_queue', login_url='/console/login/'), name='dispatch')
class DomesticProfileApprovalQueue(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/domestic-profile-approval-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.payment_date, self.modified = '', ''
        self.sel_opt='number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        self.sel_opt = request.GET.get('rad_search','number')
        return super(DomesticProfileApprovalQueue, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomesticProfileApprovalQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var =self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "modified": self.modified, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name="domesticprofileapproval"),
             var:'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(DomesticProfileApprovalQueue, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, product__type_flow=5,
            product__sub_type_flow__in=[501,503],
            oi_status=23, no_process=False,
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        try:
            if self.query:

                if self.sel_opt == 'id':

                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile__iexact=self.query)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_booster_queue', login_url='/console/login/'), name='dispatch')
class BoosterQueueVeiw(ListView, PaginationMixin):
    context_object_name = 'booster_list'
    template_name = 'console/order/booster-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.sel_opt = 'number'
        self.payment_date = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.sel_opt = request.GET.get('rad_search','number')
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        return super(BoosterQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoosterQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['booster_list'], self.paginated_by)
        var = self.sel_opt
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date, }
        filter_form = OIFilterForm(initial)

        context.update({
            "action_form": OIActionForm(queue_name='booster'),
            "messages": alert,
            "query": self.query,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "form": ResumeUploadForm(),
            var: 'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(BoosterQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3], product__type_flow__in=[7, 15],
            no_process=False, oi_status__in=[5, 61, 62, 4],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65]
        ).annotate(
            booster_counter=Count(Case(
                When(emailorderitemoperation__email_oi_status=92, then=1),
                output_field=IntegerField()
            ))
        ).filter(
            booster_counter__lte=2
        )
        queryset = queryset.select_related('order', 'product', 'assigned_to', 'assigned_by')
        q1 = queryset.filter(oi_status=61)
        exclude_list = []
        for obj in q1:
            closed_ois = obj.order.orderitems.filter(oi_status=4, product__type_flow=1, no_process=False)
            if closed_ois.exists():
                last_oi_status = obj.oi_status
                obj.oi_status = 5
                obj.oi_draft = closed_ois[0].oi_draft
                obj.draft_counter += 1
                obj.last_oi_status = last_oi_status
                obj.draft_added_on = timezone.now()
                obj.save()

                obj.orderitemoperation_set.create(
                    oi_draft=obj.oi_draft,
                    draft_counter=obj.draft_counter,
                    oi_status=obj.oi_status,
                    last_oi_status=obj.last_oi_status,
                    assigned_to=obj.assigned_to,
                )
            else:
                exclude_list.append(obj.pk)

        queryset = queryset.exclude(id__in=exclude_list)
        # queryset = queryset.exclude(Q(oi_draft__isnull=True) | Q(oi_draft__exact=''))

        try:
            if self.query:

                if self.sel_opt == 'id':

                    queryset = queryset.filter(id__iexact=self.query)
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                               Q(parent__isnull=False, parent__product__name__icontains=self.query))
                elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(order__email__iexact=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(order__mobile=self.query)

        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
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
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.order_by('-modified')

    def post(self, request, *args, **kwargs):
        form = ResumeUploadForm(request.POST, request.FILES)
        obj_pk = request.POST.get('oi_pk', None)
        if form.is_valid():
            try:
                orderitem = OrderItem.objects.get(pk=obj_pk, oi_status__in=[5, 62,4])
                data = {
                    "oi_draft": request.FILES.get('oi_resume', ''),
                }
                ActionUserMixin().upload_draft_orderitem(
                    oi=orderitem, data=data, user=request.user
                )
                messages.add_message(request, messages.SUCCESS, 'Draft uploaded Successfully')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            error_message = form.errors.get('oi_resume')
            if error_message:
                messages.add_message(request, messages.ERROR, error_message[0])
        return HttpResponseRedirect(reverse("console:queue-booster"))


class ActionOrderItemView(View):
    def post(self, request, *args, **kwargs):
        try:
            action = int(request.POST.get('action', '0'))
        except:
            action = 0

        selected = request.POST.get('selected_id', '')
        selected_id = json.loads(selected)
        queue_name = request.POST.get('queue_name', '')

        if action == -1 and queue_name == 'approval':
            try:
                csvfile = StringIO()
                csv_writer = csv.writer(
                    csvfile, delimiter=',', quotechar="'",
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([
                    'Orderitem Id', 'Order Number', 'Name',
                    'Email', 'Country Code', 'Mobile', 'Product Name', 'Partner', 'Flow Status',
                    'Expert Name', 'modified', 'Draft Level',
                    'Draft Submited On', 'Payment Date'])
                orderitems = OrderItem.objects.filter(
                    id__in=selected_id).select_related('order', 'product', 'partner')
                if orderitems:
                    for oi in orderitems:
                        try:
                            if oi.assigned_to:
                                writer = oi.assigned_to.name or oi.assigned_to.email
                            else:
                                writer = ''
                            name = ''
                            if oi.order.first_name:
                                name = oi.order.first_name
                            if oi.order.last_name:
                                name = name + ' ' + oi.order.last_name

                            partner_name = ''
                            if oi.partner:
                                partner_name = oi.partner.name

                            csv_writer.writerow([
                                str(oi.pk),
                                str(oi.order.number),
                                str(name),
                                str(oi.order.email),
                                str(oi.order.country_code),
                                str(oi.order.mobile),
                                str(oi.product.get_name),
                                str(partner_name),
                                str(oi.get_oi_status),
                                str(writer),
                                str(oi.modified),
                                str(oi.get_draft_level()),
                                str(oi.draft_added_on),
                                str(oi.order.payment_date)])
                        except Exception as e:
                            logging.getLogger('error_log').error("%s " % str(e))
                            continue
                    response = HttpResponse(csvfile.getvalue())
                    file_name = queue_name + timezone.now().date().strftime("%Y-%m-%d")
                    response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
                return response

            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-approval'))

        elif action == -1 and queue_name == 'rejectedbycandidate':
            try:
                csvfile = StringIO()
                csv_writer = csv.writer(
                    csvfile, delimiter=',', quotechar="'",
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([
                    'Orderitem Id', 'Order Number', 'Name',
                    'Email', 'Country Code', 'Mobile', 'Product Name', 'Partner', 'Flow Status',
                    'Expert Name', 'modified', 'Draft Level',
                    'Draft Submited On', 'Payment Date'])

                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                if orderitems:
                    for oi in orderitems:
                        try:
                            if oi.assigned_to:
                                writer = oi.assigned_to.name or oi.assigned_to.email
                            else:
                                writer = ''

                            name = ''
                            if oi.order.first_name:
                                name = oi.order.first_name
                            if oi.order.last_name:
                                name = name + ' ' + oi.order.last_name

                            partner_name = ''
                            if oi.partner:
                                partner_name = oi.partner.name

                            csv_writer.writerow([
                                str(oi.pk),
                                str(oi.order.number),
                                str(name),
                                str(oi.order.email),
                                str(oi.order.country_code),
                                str(oi.order.mobile),
                                str(oi.product.get_name),
                                str(partner_name),
                                str(oi.get_oi_status),
                                str(writer),
                                str(oi.modified),
                                str(oi.get_draft_level()),
                                str(oi.draft_added_on),
                                str(oi.order.payment_date)])
                        except Exception as e:
                            logging.getLogger('error_log').error("%s " % str(e))
                            continue
                    response = HttpResponse(csvfile.getvalue())
                    file_name = queue_name + timezone.now().date().strftime("%Y-%m-%d")
                    response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
                return response

            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-rejectedbycandidate'))

        elif action == -1 and queue_name == 'rejectedbyadmin':
            try:
                csvfile = StringIO()
                csv_writer = csv.writer(
                    csvfile, delimiter=',', quotechar="'",
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([
                    'Orderitem Id', 'Order Number', 'Name',
                    'Email', 'Country Code', 'Mobile', 'Product Name', 'Partner', 'Flow Status',
                    'Expert Name', 'modified', 'Draft Level',
                    'Draft Submited On', 'Payment Date'])
            
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                if orderitems:
                    for oi in orderitems:
                        try:
                            if oi.assigned_to:
                                writer = oi.assigned_to.name or oi.assigned_to.email
                            else:
                                writer = ''

                            name = ''
                            if oi.order.first_name:
                                name = oi.order.first_name
                            if oi.order.last_name:
                                name = name + ' ' + oi.order.last_name

                            partner_name = ''
                            if oi.partner:
                                partner_name = oi.partner.name

                            csv_writer.writerow([
                                str(oi.pk),
                                str(oi.order.number),
                                str(name),
                                str(oi.order.email),
                                str(oi.order.country_code),
                                str(oi.order.mobile),
                                str(oi.product.get_name),
                                str(partner_name),
                                str(oi.get_oi_status),
                                str(writer),
                                str(oi.modified),
                                str(oi.get_draft_level()),
                                str(oi.draft_added_on),
                                str(oi.order.payment_date)])
                        except Exception as e:
                            logging.getLogger('error_log').error("%s " % str(e))
                            continue
                    response = HttpResponse(csvfile.getvalue())
                    file_name = queue_name + timezone.now().date().strftime("%Y-%m-%d")
                    response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
                return response

            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-rejectedbyadmin'))

        elif action == -1 and queue_name == 'booster':
            try:
                csvfile = StringIO()
                csv_writer = csv.writer(
                    csvfile, delimiter=',', quotechar="'",
                    quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([
                    'Orderitem Id', 'Order Number', 'Name',
                    'Email', 'Country Code', 'Mobile', 'Product Name', 'Partner', 'Flow Status',
                    'modified', 'Payment Date'])

                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                if orderitems:
                    for oi in orderitems:
                        try:
                            name = ''
                            if oi.order.first_name:
                                name = oi.order.first_name
                            if oi.order.last_name:
                                name = name + ' ' + oi.order.last_name

                            partner_name = ''
                            if oi.partner:
                                partner_name = oi.partner.name

                            csv_writer.writerow([
                                str(oi.pk),
                                str(oi.order.number),
                                str(name),
                                str(oi.order.email),
                                str(oi.order.country_code),
                                str(oi.order.mobile),
                                str(oi.product.get_name),
                                str(partner_name),
                                str(oi.get_oi_status),
                                str(oi.modified),
                                str(oi.order.payment_date)])
                        except Exception as e:
                            logging.getLogger('error_log').error("%s " % str(e))
                            continue
                    response = HttpResponse(csvfile.getvalue())
                    file_name = queue_name + timezone.now().date().strftime("%Y-%m-%d")
                    response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
                return response

            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-booster'))

        elif action == -3 and queue_name == 'booster':
            try:
                booster_ois = OrderItem.objects.filter(
                    id__in=selected_id,
                    product__type_flow__in=[7, 15],
                    oi_status__in=[5, 62, 4]
                ).annotate(
                    booster_counter=Count(Case(
                        When(emailorderitemoperation__email_oi_status=92, then=1),
                        output_field=IntegerField()
                    ))
                ).filter(
                    booster_counter__lte=2
                ).select_related('order')
                days = 7
                candidate_data = {}
                international_booster_candidate_list = []
                recruiter_data = {}
                candidate_list = []
                order_item_to_update_list = []
                mail_send = 0

                for oi in booster_ois:
                    token = TokenExpiry().encode(oi.order.email, oi.pk, days)
                    to_emails = [oi.order.email]
                    email_sets = list(oi.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                    candidate_data.update({
                        "email": oi.order.email,
                        "mobile": oi.order.mobile,
                        'subject': 'Your resume has been shared with relevant consultants',
                        "username": oi.order.first_name,
                    })

                    if oi.oi_draft or oi.oi_resume:
                        resumevar = "%s://%s/user/resume/download/?token=%s" % (
                            settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)
                        resumevar = textwrap.fill(resumevar, width=80)

                        link_title = candidate_data.get('username') if candidate_data.get('username') else candidate_data.get('email')
                        download_link = resumevar
                        data_dict = {}
                        data_dict.update({
                            "title": link_title,
                            "download_link": download_link,
                        })
                        if oi.product.type_flow == 7:
                            candidate_list.append(data_dict)
                        elif oi.product.type_flow == 15:
                            international_booster_candidate_list.append(data_dict)
                        mail_send += 1
                        order_item_to_update_list.append(oi.pk)
                    else:
                        continue

                try:
                    recruiter_data.update({
                        "data": candidate_list,
                    })
                    # send mail to rectuter
                    mail_type = 'BOOSTER_RECRUITER'
                    if candidate_list != []:
                        recruiters = BoosterRecruiter.objects.get(type_recruiter=0).recruiter_list.split(',')
                        send_booster_recruiter_mail_task.delay(
                            recruiters, mail_type, recruiter_data,
                            ois_to_update=order_item_to_update_list
                        )

                    recruiter_data.update({"data": international_booster_candidate_list})

                    if international_booster_candidate_list != []:
                        recruiters = BoosterRecruiter.objects.get(type_recruiter=1).recruiter_list.split(',')

                        send_booster_recruiter_mail_task.delay(
                            recruiters, mail_type, recruiter_data,
                            ois_to_update=order_item_to_update_list
                        )

                except Exception as e:
                    logging.getLogger('error_log').error("%s" % (str(e)))

                success_message = "%s Mail sent Successfully." % (str(mail_send))
                messages.add_message(request, messages.SUCCESS, success_message)
                return HttpResponseRedirect(reverse('console:queue-booster'))

            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-booster'))

        elif action == -4 and queue_name == "domesticprofileupdate":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                approval = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.orderitemoperation_set.create(
                        oi_status=23,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                    # Auto Approve the feature profile as per requirement from product.
                    # action == -5 and queue_name == "domesticprofileapproval"
                    last_oi_status = 23
                    obj.oi_status = 30  # approved
                    obj.last_oi_status = last_oi_status
                    obj.approved_on = timezone.now()
                    obj.save()
                    approval += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems updated and approval done.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -5 and queue_name == "domesticprofileapproval":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                approval = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 30  # approved
                    obj.last_oi_status = last_oi_status
                    obj.approved_on = timezone.now()
                    obj.save()
                    approval += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems approved.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -6 and queue_name == "domesticprofileapproval":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                approval = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 25  # rejected By Admin
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    approval += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems rejected.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -10 and queue_name == "internationalapproval":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                approval = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 4  # closed
                    obj.last_oi_status = 6
                    obj.approved_on = timezone.now()
                    obj.closed_on = timezone.now()
                    obj.save()
                    approval += 1

                    obj.orderitemoperation_set.create(
                        oi_status=6,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)

                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)

                    # mail to user about writer information
                    profile_obj = obj.product.productextrainfo_set.get(
                        info_type='profile_update')
                    country_obj = Country.objects.get(pk=profile_obj.object_id)
                    profiles = InternationalProfileCredential.objects.filter(
                        oi=obj.pk)
                    to_emails = [obj.order.email]
                    email_sets = list(
                        obj.emailorderitemoperation_set.all().values_list(
                            'email_oi_status', flat=True).distinct())
                    data = {}
                    data.update({
                        "username": obj.order.first_name,
                        "subject": "Your International Profile is updated",
                        "profiles": profiles,
                        "country_name": country_obj.name,
                    })
                    mail_type = 'INTERNATIONATIONAL_PROFILE_UPDATED'
                    if 62 not in email_sets:
                        send_email(
                            to_emails, mail_type, data, status=62, oi=obj.pk)
                    try:
                        SendSMS().send(sms_type=mail_type, data=data)
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "%s - %s" % (str(mail_type), str(e)))

                msg = str(approval) + ' orderitems approved.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -11 and queue_name == "internationalapproval":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                approval = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 25  # rejected By Admin
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    approval += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems rejected.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -15 and queue_name == "whatsappjoblist":
            try:
                orderitems = OrderItem.objects.filter(
                    id__in=selected_id,
                    oi_status=5,
                    product__type_flow=5).exclude(oi_status=4).select_related('order', 'product', 'partner')
                counter = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 4  # Closed
                    obj.last_oi_status = last_oi_status
                    obj.save()

                    obj.orderitemoperation_set.create(
                        oi_status=6,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)

                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=6,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                    counter += 1
                msg = str(counter) + ' orderitems closed.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        elif action == -7 and queue_name == "partnerinbox":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                hold = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 10  # on Hold
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    hold += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(hold) + ' orderitems are placed on hold.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:partner:' + queue_name))

        elif action == -8 and queue_name == "partnerholdqueue":
            try:
                orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
                unhold = 0
                for obj in orderitems:
                    last_oi_status = obj.oi_status
                    obj.oi_status = 12  # UnHold
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    unhold += 1
                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(unhold) + ' orderitems are unhold.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:partner:' + queue_name))

        elif action == -2 and queue_name == 'midout':
            orders = Order.objects.filter(id__in=selected_id)
            for order in orders:
                ord_items = order.orderitems.first()
                mid_out_sent = True
                if order.midout_sent_on and timezone.now().date() == order.midout_sent_on.date():
                    mid_out_sent = False
                if mid_out_sent:
                    # mail to user about writer information
                    to_emails = [order.email]
                    mail_type = "PENDING_ITEMS"
                    token = AutoLogin().encode(
                        order.email, order.candidate_id, days=None)
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': order.first_name if order.first_name else order.candidate_id,
                        'type_flow': ord_items.product.type_flow,
                        'product_name': ord_items.product.name,
                        'product_url': ord_items.product.get_url(),
                        'parent_name': ord_items.parent.product.name if ord_items.parent else None,
                        'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
                    })
                    try:
                        SendMail().send(to_emails, mail_type, data)
                        order.midout_sent_on = timezone.now()
                        order.save()
                    except Exception as e:
                        messages.add_message(request, messages.ERROR, str(e))
                        logging.getLogger('error_log').error("midout mail %s - %s - %s" % (str(to_emails), str(mail_type), str(e)))
            messages.add_message(request, messages.SUCCESS, "Midout sent Successfully for selected items")
            return HttpResponseRedirect(reverse('console:queue-midout'))
        messages.add_message(request, messages.ERROR, "Select Valid Action")
        try:
            return HttpResponseRedirect(reverse('console:queue-' + queue_name))
        except:
            return HttpResponseForbidden()






class AssignmentOrderItemView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_pk = int(request.POST.get('assign_to', '0'))
        except:
            user_pk = 0

        selected = request.POST.get('selected_id', '')
        selected_id = json.loads(selected)
        queue_name = request.POST.get('queue_name', '')

        if user_pk and selected_id and request.user.is_authenticated():
            try:
                User = get_user_model()
                assign_to = User.objects.get(pk=user_pk)
                ActionUserMixin().assign_single_orderitem(
                    orderitem_list=selected_id,
                    assigned_to=assign_to,
                    user=request.user
                )

                orderitem_objs = OrderItem.objects.filter(id__in=selected_id)

                display_message = str(len(orderitem_objs)) + ' orderitems are Assigned.'
                messages.add_message(request, messages.SUCCESS, display_message)
                return HttpResponseRedirect(reverse('console:queue-' + queue_name))
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
                return HttpResponseRedirect(reverse('console:queue-' + queue_name))




        messages.add_message(request, messages.ERROR, "Please select valid assignment.")
        return HttpResponseRedirect(reverse('console:queue-' + queue_name))


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_view_order_detail', login_url='/console/login/'), name='dispatch')
class ConsoleResumeDownloadView(View):

    def get(self, request, *args, **kwargs):
        current_time = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S %p")
        try:
            file = request.GET.get('path', None)
            next_url = request.GET.get('next', None)
            if file:
                if file.startswith('/'):
                    file = file[1:]
                file_path = settings.RESUME_DIR + file
                if not settings.IS_GCP:
                    fsock = FileWrapper(open(file_path, 'rb'))
                else:
                    fsock = GCPPrivateMediaStorage().open(file_path)
    
                filename = file.split('/')[-1]
                response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
                response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                return response
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
        logging.getLogger('info_log').info(
            '{},{},{},{}'.format(current_time, self.request.user.id, self.request.user.get_full_name(),
                                 'resume download'))
        return HttpResponseRedirect(next_url)


@method_decorator(permission_required('review.can_change_review_queue', login_url='/console/login/'), name='dispatch')
class ReviewModerateListView(ListView, PaginationMixin):

    context_object_name = 'review_list'
    template_name = 'console/order/review-moderation-list.html'
    model = Review
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query, self.created = '', ''
        self.status = -1

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.status = request.GET.get('filter_status', -1)
        self.created = request.GET.get('created', '')
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        paginator = Paginator(context['review_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "status": self.status
        }
        context.update({
            "query": self.query,
            "action_form": ReviewActionForm(),
            'filter_form': ReviewFilterForm(initial),
            "messages": alert,
        })
        return context

    def post(self, request, *args, **kwargs):
        try:
            review_list = request.POST.getlist('table_records', [])
            action_type = int(request.POST.get('action_type', '0'))
            if action_type == -1:
                messages.add_message(
                    request, messages.ERROR,
                    'Please select valid action first')
            elif action_type == 0:
                Review.objects.filter(id__in=review_list).update(status=0)
                messages.add_message(
                    request, messages.SUCCESS,
                    str(len(review_list)) + ' Review are required moderation.')
            elif action_type == 1:
                Review.objects.filter(id__in=review_list).update(status=1)
                messages.add_message(
                    request, messages.SUCCESS,
                    str(len(review_list)) + ' Review are approved.')
            elif action_type == 2:
                Review.objects.filter(id__in=review_list).update(status=2)
                messages.add_message(
                    request, messages.SUCCESS,
                    str(len(review_list)) + ' Review rejeted.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

        return HttpResponseRedirect(reverse('console:review-to-moderate'))

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        prd_obj = ContentType.objects.get_for_model(Product)
        queryset = Review.objects.filter(content_type=prd_obj)
        try:
            if self.query:
                queryset = queryset.filter(
                    Q(object_id__icontains=self.query) |
                    Q(user_email__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

        try:
            if int(self.status) != -1:
                queryset = queryset.filter(status=self.status)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))

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
        return queryset


@method_decorator(permission_required('review.can_change_review_queue', login_url='/console/login/'), name='dispatch')
class ReviewModerateView(UpdateView):
    model = Review
    template_name = 'console/order/review-moderation-update.html'
    success_url = "/console/queue/review/review-to-moderate/"
    http_method_names = [u'get', u'post']
    form_class = ReviewUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context


@Decorate(stop_browser_cache())
class WhatsappListQueueView(UserPermissionMixin, ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/whatsapp_list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']
    permission_to_check = ['Can view assigned jobs on the move', 'Can assign jobs on the move',
                           'Can send assigned jobs on the move']
    any_permission = True

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.sel_opt = 'number'
        self.oi_status = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.oi_status = request.GET.get('oi_status', '-1').strip()
        self.day_choice = request.GET.get('day_choice', '-1').strip()
        self.sel_opt = request.GET.get('rad_search', 'number')
        self.payment_date = self.request.GET.get('payment_date', '')
        return super(WhatsappListQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WhatsappListQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        initial = {"oi_status": self.oi_status}

        filter_form = OIFilterForm(initial, queue_name='queue-whatsappjoblist')
        context.update({"assignment_form": AssignmentActionForm(), "messages": alert, "query": self.query,
            "message_form": MessageForm(), "filter_form": filter_form,
            "action_form": OIActionForm(queue_name="queue-whatsappjoblist"), var: 'checked'})

        return context

    def get_queryset(self):
        query_filters = dict()
        query_filters_exclude = dict()
        queryset = super(WhatsappListQueueView, self).get_queryset()
        query_filters.update({'order__status__in': [1, 2, 3], 'product__type_flow': 5, 'no_process': False,
            'product__sub_type_flow': 502, 'order__welcome_call_done': True})
        query_filters_exclude.update({'wc_sub_cat__in': [64, 65]})
        user = self.request.user
        if user.is_superuser or user.has_perm('order.can_assign_jobs_on_the_move'):
            pass
        elif user.has_perm('order.can_view_assigned_jobs_on_the_move'):
            query_filters.update({'assigned_to': user})
            query_filters_exclude.update({'oi_status': 4})
        elif user.has_perm('order.can_send_jobs_on_the_move'):
            query_filters_exclude.update({'assigned_to': None})

        else:
            return queryset.none()
        try:
            if self.query:
                if self.sel_opt == 'number':
                    if self.query[:2].lower() == 'cp':
                        query_filters.update({'order__number__iexact': self.query})
                    else:
                        return queryset.none()
                elif self.sel_opt == 'id' and self.query.isdigit():
                    query_filters.update({'id': self.query})

                elif self.sel_opt == 'mobile':

                    query_filters.update({'order__mobile' : self.query})
                elif self.sel_opt == 'email':

                    query_filters.update({'order__email__iexact' : self.query})
                elif self.sel_opt == 'product':
                    queryset = queryset.select_related('parent')
                    queryset = queryset.filter(Q(product__name__icontains=self.query) | Q(parent__isnull=False,
                        parent__product__name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        queryset = queryset.filter(**query_filters)
        for key, value in query_filters_exclude.items():
            queryset = queryset.exclude(**{key: value})
        queryset = queryset.annotate(
            save_link=Count(Case(
                When(jobs_link__status=0, then=1),
                output_field=IntegerField()
            ))
        )
        if int(self.oi_status) != -1:
            if int(self.oi_status) == 33:
                queryset = queryset.filter(
                    oi_status=31, save_link__gt=0,
                    whatsapp_profile_orderitem__approved=True
                )
            elif int(self.oi_status) == 31:
                queryset = queryset.filter(
                    oi_status=31, save_link=0,
                    whatsapp_profile_orderitem__approved=True
                )
            elif int(self.oi_status) == 34:
                queryset = queryset.filter(
                    whatsapp_profile_orderitem__approved=False
                )
            else:
                queryset = queryset.filter(oi_status=self.oi_status)

        if self.payment_date:
            start_date, end_date = self.payment_date.split(' - ')
            start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y")
            end_date = end_date + relativedelta.relativedelta(days=1)
            queryset = queryset.filter(order__payment_date__range=[start_date, end_date])

        # data for whats app links:
        queryset = queryset.annotate(
            sent_link=Count(
                Case(
                    When(jobs_link__status=2, then=1),
                    output_field=IntegerField())
            ),
            save_link=Count(Case(
                When(jobs_link__status=0, then=1),
                output_field=IntegerField())
            )
        )
        if int(self.day_choice) != -1:
            q_objects = Q()
            if int(self.day_choice) == 1:
                today = timezone.now()
                date_list = [(today - relativedelta.relativedelta(days=i * 7)).date() for i in range(0,52) ]
                for d in date_list:
                    q_objects |= Q(orderitemoperation__oi_status=1, orderitemoperation__created__range=[d, d + relativedelta.relativedelta(days=1)])
            elif int(self.day_choice) == 2:
                tommorrow = timezone.now() + relativedelta.relativedelta(days=1)
                date_list = [(tommorrow - relativedelta.relativedelta(days=i * 7)).date() for i in range(0,52) ]
                for d in date_list:
                    q_objects |= Q(orderitemoperation__oi_status=1, orderitemoperation__created__range=[d, d + relativedelta.relativedelta(days=1)])
            queryset = queryset.filter(q_objects)

        queryset = queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-pending_links_count')

        return queryset

@method_decorator(permission_required('order.can_generate_compliance_report', login_url='/console/login/'), name='dispatch')
class ComplianceReport(TemplateView):
    model = OrderItem
    template_name = 'console/order/compliance_report.html'

    def post(self,request,*args,**kwargs):
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        context = super(self.__class__, self).get_context_data(**kwargs)
        if not start_date or not end_date:
            messages.add_message(
                request, messages.ERROR,
                'Please select the both the date')
            return render(request, self.template_name)
        today = timezone.now()
        start = start_date.split('/')
        end = end_date.split('/')
        if len(start) != 3 or len(end) != 3 :
            messages.add_message(
                request, messages.ERROR,
                'Something went wrong')
            return render(request, self.template_name)
        start_date = datetime.datetime(int(start[2]),int(start[0]),int(start[1]),0,0,0,0,\
                                     tzinfo=today.tzinfo)
        end_date = datetime.datetime(int(end[2]), int(end[0]), int(end[1]),11, 59, 59, 0,\
                                     tzinfo=today.tzinfo)

        if start_date > end_date:
             messages.add_message(
                request, messages.ERROR,
                'Please select the correct dates,end date should be greater than start date')
             return render(request, self.template_name)

        reporting_limit = relativedelta.relativedelta(end_date,start_date)
        if reporting_limit.years or reporting_limit.months > 4:
            messages.add_message(
                request, messages.ERROR,
                'Please select the dates ranging within 3 months')
            return render(request, self.template_name)

        start_date = date_timezone_convert(start_date)
        end_date = date_timezone_convert(end_date)

        Task = Scheduler.objects.create(
            task_type=6,
            created_by=request.user,
        )
        generate_compliance_report.delay(
            task_id=Task.pk,
            start_date=start_date,
            end_date=end_date)

        logging.getLogger('info_log').info("Compliance Report Downloaded | {},{},{},{},{}".\
                format(request.user.id,request.user.get_full_name(),\
                    datetime.datetime.now(),start_date,end_date))

        messages.add_message(
            request, messages.SUCCESS,
            'Task Created SuccessFully, Compliance Report is generating')
        return HttpResponseRedirect(reverse('console:tasks:tasklist'))


    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context


@method_decorator(permission_required('order.can_show_inbox_queue', login_url='/console/login/'), name='dispatch')
class ReplacedOrderListView(PaginationMixin, ListView):
    context_object_name = 'inbox_list'
    template_name = 'console/order/replace-order-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']
    page = 1
    paginated_by = 50
    query = ''
    sel_opt = 'number'
    created = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.sel_opt = request.GET.get('rad_search', 'number')
        self.created = request.GET.get('created', '')
        return super(ReplacedOrderListView, self).get(request, args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ReplacedOrderListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['inbox_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)
        filter_form = OIFilterForm()

        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
            var: "checked",
        })
        return context

    def get_queryset(self):
        queryset = super(ReplacedOrderListView, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            wc_sub_cat__in=[64, 65])

        if self.query:
            if self.sel_opt == 'id':
                    queryset = queryset.filter(id__iexact=self.query)
            elif self.sel_opt == 'number':
                    queryset = queryset.filter(order__number__iexact=self.query)
            elif self.sel_opt == 'mobile':
                queryset = queryset.filter(order__mobile__iexact=self.query)
            elif self.sel_opt == 'email':
                queryset = queryset.filter(order__email__iexact=self.query)
            elif self.sel_opt == 'product':
                queryset = queryset.select_related('parent')
                queryset = queryset.filter(
                    Q(product__name__icontains=self.query) |
                    Q(parent__isnull=False, parent__product__name__icontains=self.query)
                )

        return queryset.select_related('order').order_by('-modified')


@method_decorator(permission_required('order.can_show_certification_queue', login_url='/console/login/'), name='dispatch')
class CertficationProductQueueView(PaginationMixin, ListView):
    context_object_name = 'object_list'
    template_name = 'console/order/certification-order-item-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']
    page = 1
    paginated_by = 20
    query = ''
    created = ''
    sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.created = request.GET.get('created', '')
        self.sel_opt = request.GET.get('rad_search','number')
        self.modified = request.GET.get('modified', '')
        return super(CertficationProductQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CertficationProductQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        var = self.sel_opt
        alert = messages.get_messages(self.request)

        filter_form = OIFilterForm()
        context.update({
            "assignment_form": AssignmentActionForm(),
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
            var: 'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(CertficationProductQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3],
            product__type_flow=16, no_process=False,
            oi_status__in=[5, 4],
            product__sub_type_flow__in=[1601, 1602],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        if self.query:
            if self.sel_opt == 'number':
                if self.query[:2] == 'cp' or self.query[:2] == 'CP':
                    queryset = queryset.filter(order__number__iexact=self.query)
                else:
                    queryset = queryset.none()
            elif self.sel_opt == 'id':
                    queryset = queryset.filter(id__iexact=self.query)
            elif self.sel_opt == 'mobile':
                queryset = queryset.filter(order__mobile=self.query)
            elif self.sel_opt == 'email':
                queryset = queryset.filter(order__email__iexact=self.query)
            elif self.sel_opt == 'product':
                queryset = queryset.select_related('parent')
                queryset = queryset.filter(Q(product__name__icontains=self.query) |
                                           Q(parent__isnull=False, parent__product__name__icontains=self.query))

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

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')


class WhatsAppScheduleView(UserPermissionMixin, DetailView, PaginationMixin):
    template_name = 'console/order/whats_app_schedule.html'
    model = OrderItem
    context_object_name = 'orderitem'
    page = 1
    any_permission = True
    paginated_by = 10
    permission_to_check = ['Can view assigned jobs on the move', 'Can assign jobs on the move',
                           'Can send assigned jobs on the move']

    def get(self, request, *args, **kwargs):
        obj = self.object = self.get_object()
        if request.user.is_superuser or request.user.has_perm('order.can_assign_jobs_on_the_move'):
            pass
        elif request.user.has_perm('order.can_send_jobs_on_the_move') and obj.assigned_to:
            pass
        elif request.user.has_perm('order.can_view_assigned_jobs_on_the_move') and request.user == obj.assigned_to:
            pass
        else:
            messages.add_message(self.request,messages.ERROR,'You are not authorised to view this order.')
            return HttpResponseRedirect("/console/")
        return super(WhatsAppScheduleView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        obj = self.object = self.get_object()
        self.page = self.request.GET.get('page', 1)
        context = super(WhatsAppScheduleView, self).get_context_data(**kwargs)
        joblinkformset = modelformset_factory(
            JobsLinks,
            form=JobLinkForm,
            can_delete=True,
            extra=4
        )

        formset = joblinkformset(
            queryset=JobsLinks.objects.filter(oi=obj, status__in=[0])
        )

        # previously sent link
        previous_links = JobsLinks.objects.filter(oi=obj, status__in=[2]).order_by('-sent_date')
        paginator = Paginator(previous_links, self.paginated_by)
        context.update(self.pagination(paginator, self.page))

        if getattr(obj, 'whatsapp_profile_orderitem', None):
            profile_form = ProductUserProfileForm(instance=obj.whatsapp_profile_orderitem)
        else:
            profile_form = ProductUserProfileForm()
        context.update({'formset': formset, 'previous_links': previous_links, 'profile_form': profile_form})
        return context

    def attach_object_with_data(self, request, *args, **kwargs):

        fields = ['id', 'company_name', 'location', 'experience', 'job_title', 'link','status']
        total_forms = int(request.POST.get('form-TOTAL_FORMS', 0))

        request_copy = request.POST.copy()
        for i in range(total_forms):
            prefix = "form-{}-".format(i)
            form_to_consider = any([bool(request.POST.get(prefix + field)) for field in fields])
            if not form_to_consider:
                continue

            request_copy.update({prefix + "oi": self.object.id})
        return request_copy

    def post(self, request, *args, **kwargs):
        obj = self.object = self.get_object()
        user = self.request.user
        objects = []
        joblinkformset = modelformset_factory(
            JobsLinks,
            form=JobLinkForm,
            can_delete=True,
            extra=4
        )
        action_type = int(request.POST.get('action_type', 0))
        context = self.get_context_data()
        post_data = self.attach_object_with_data(request, *args, **kwargs)
        if action_type != 3:
            formset = joblinkformset(post_data)
            if formset.is_valid():
                saved_formset = formset.save()

                if getattr(formset, '_queryset', None) and not saved_formset:
                    objects = list(formset._queryset.filter(status=0, oi=obj))
                elif getattr(formset, '_queryset', None) and saved_formset:
                    objects = list(formset._queryset.filter(status=0, oi=obj))
                elif saved_formset:
                    objects = saved_formset
                job_message = None

                if action_type == 2:
                    for k in objects:
                        k.sent_date = timezone.now()
                        k.last_modified_by = request.user
                        if not k.created_by:
                            k.created_by = request.user
                        k.status = 2
                        k.save()
                        obj.update_pending_links_count()
                        if obj.pending_links_count == 0 and obj.oi_status == 31:
                            last_oi_status = obj.oi_status
                            obj.oi_status = 32
                            obj.save()
                            obj.orderitemoperation_set.create(
                                oi_status=obj.oi_status,
                                last_oi_status=last_oi_status,
                                assigned_to=obj.assigned_to,
                                added_by=request.user
                            )
                    obj.update_pending_links_count()
                    context = self.get_context_data()
                    messages.success(self.request, "Job Link marked as Sent")
                elif action_type == 4:
                    job_data = ''
                    for k in objects:
                        job_data += k.company_name + ' - ' + k.job_title + ' - '+ \
                            k.location + ' -    ' + k.shorten_url + '<br><br>'
                    if job_data:
                        job_message = settings.WHATS_APP_MESSAGE_FORMAT.format(job_data)

                else:
                    for k in saved_formset:
                        k.last_modified_by = request.user
                        if not k.created_by:
                            k.created_by = request.user
                        k.save()
                    messages.success(self.request, "Job Links are Saved")
                context.update({'job_message': job_message})

            else:
                context.update({'formset': formset})
                messages.error(
                    self.request,
                    "Job Link Scheduled Failed, Changes not Saved")
        else:
            profile_form = ProductUserProfileForm(data=request.POST, instance=obj.whatsapp_profile_orderitem)
            if profile_form.is_valid:
                profile_form.save()
                messages.success(
                    self.request,
                    "Profile Changes Saved")
            else:
                messages.error(
                    self.request,
                    "Profile Changes not Saved")
            context.update({'profile_form': profile_form})
        return TemplateResponse(
            request, [
                "console/order/whats_app_schedule.html"
            ], context)


