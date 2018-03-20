import json
import csv
import datetime
import logging
import mimetypes
import textwrap

from io import StringIO
from wsgiref.util import FileWrapper
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    TemplateView, ListView, DetailView, View, UpdateView)
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

from geolocation.models import Country
from order.models import Order, OrderItem, InternationalProfileCredential, OrderItemOperation
from shop.models import DeliveryService, Product
from blog.mixins import PaginationMixin
from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from core.mixins import TokenExpiry
from payment.models import PaymentTxn
from linkedin.autologin import AutoLogin
from order.functions import send_email


from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from review.models import Review

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
    ReviewUpdateForm,)
from .mixins import ActionUserMixin


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        self.status = request.GET.get('status', -1)
        return super(OrderListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['order_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {"payment_date": self.payment_date, "created": self.created, "status": self.status}
        filter_form = OrderFilterForm(initial)
        context.update({
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
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
                    queryset = queryset.filter(
                        Q(number__icontains=self.query) |
                        Q(email__icontains=self.query) |
                        Q(mobile__icontains=self.query) |
                        Q(id__icontains=self.query))

        except Exception as e:
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

        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_welcome_queue', login_url='/console/login/'), name='dispatch')
class WelcomeCallVeiw(ListView, PaginationMixin):
    context_object_name = 'welcome_list'
    template_name = 'console/order/welcome-list.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.payment_date, self.created = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        return super(WelcomeCallVeiw, self).get(request, args, **kwargs)

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
        context = super(WelcomeCallVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['welcome_list'], self.paginated_by)
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
        queryset = super(WelcomeCallVeiw, self).get_queryset()
        queryset = queryset.filter(status=1, welcome_call_done=False)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(number__icontains=self.query) |
                    Q(email__icontains=self.query) |
                    Q(mobile__icontains=self.query) |
                    Q(id__icontains=self.query))
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

        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@method_decorator(permission_required('order.can_show_midout_queue', login_url='/console/login/'), name='dispatch')
class MidOutQueueView(TemplateView, PaginationMixin):
    # context_object_name = 'midout_list'
    template_name = 'console/order/midout-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query, self.modified = '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        return super(MidOutQueueView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ResumeUploadForm(request.POST, request.FILES)
        obj_pk = request.POST.get('oi_pk', None)
        if form.is_valid():
            try:
                oi = OrderItem.objects.get(pk=obj_pk)
                order = oi.order
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
        paginator = Paginator(midout_list, self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "modified": self.modified,
        }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "form": ResumeUploadForm(),
            "query": self.query,
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name='midout'),
        })
        return context

    def get_queryset(self):
        queryset = OrderItem.objects.all().select_related('order', 'product')
        queryset = queryset.filter(
            order__status=1, no_process=False, oi_status=2)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__email__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__number__icontains=self.query))
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

        return queryset.order_by('-modified')


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.writer = request.GET.get('writer', '')
        self.created = request.GET.get('created', '')
        self.delivery_type = request.GET.get('delivery_type', '')
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

        return queryset.select_related('order', 'product', 'delivery_service').order_by('-modified')

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
        excl_order_list = excl_txns.all().values_list('order__pk', flat=True)
        queryset = queryset.exclude(id__in=excl_order_list)
        queryset = queryset.filter(status=1)

        try:
            if self.query:
                q1 = queryset.filter(
                    Q(number=self.query) |
                    Q(email=self.query) |
                    Q(mobile=self.query))

                pay_txns = PaymentTxn.objects.filter(txn=self.query)
                order_pks = pay_txns.all().values_list('order__pk', flat=True)
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
class OrderDetailVeiw(DetailView):
    model = Order
    template_name = "console/order/order-detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(OrderDetailVeiw, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(OrderDetailVeiw, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = self.get_object()
        max_limit_draft = settings.DRAFT_MAX_LIMIT

        order_items = order.orderitems.all().select_related('product', 'partner').order_by('id')

        context.update({
            "order": order,
            'orderitems': list(order_items),
            "max_limit_draft": max_limit_draft,
            "messages": alert,
            "message_form": MessageForm(),
        })
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
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
        })
        return context

    def get_queryset(self):
        queryset = super(ApprovedQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, no_process=False,
            oi_status=24, product__type_flow__in=[1, 3, 5],
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.modified = request.GET.get('modified', '')
        self.writer = request.GET.get('writer', '')
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.writer = request.GET.get('writer', '')
        self.created = request.GET.get('created', '')
        self.oi_status = request.GET.get('oi_status', '')
        self.delivery_type = request.GET.get('delivery_type', '')
        return super(AllocatedQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AllocatedQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['allocated_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        return super(ClosedOrderItemQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClosedOrderItemQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['closed_oi_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "payment_date": self.payment_date, }
        filter_form = OIFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
        })

        return context

    def get_queryset(self):
        queryset = super(ClosedOrderItemQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3], oi_status=4,
            no_process=False)
        user = self.request.user
        vendor_employee_list = user.employees.filter(active=True).values_list('vendee', flat=True)  # user's associated vendor ids

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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        return super(DomesticProfileUpdateQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomesticProfileUpdateQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
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
        })

        return context

    def get_queryset(self):
        queryset = super(DomesticProfileUpdateQueueView, self).get_queryset()
        queryset = queryset.filter(
            order__status__in=[1, 3],
            product__type_flow=5, no_process=False,
            oi_status__in=[5, 25, 61],
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        self.modified = request.GET.get('modified', '')
        return super(DomesticProfileApprovalQueue, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomesticProfileApprovalQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
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
        })

        return context

    def get_queryset(self):
        queryset = super(DomesticProfileApprovalQueue, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, product__type_flow=5,
            oi_status=23, no_process=False,
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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
        self.payment_date = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.payment_date = request.GET.get('payment_date', '')
        return super(BoosterQueueVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoosterQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['booster_list'], self.paginated_by)
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
        })

        return context

    def get_queryset(self):
        queryset = super(BoosterQueueVeiw, self).get_queryset()
        queryset = queryset.filter(
            order__status=1, product__type_flow=7,
            no_process=False, oi_status__in=[5, 61],
            order__welcome_call_done=True).exclude(
            wc_sub_cat__in=[64, 65])
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
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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
                booster_ois = OrderItem.objects.filter(id__in=selected_id, product__type_flow=7, oi_status=5).select_related('order')
                days = 7
                candidate_data = {}
                recruiter_data = {}
                candidate_list = []
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
                        candidate_list.append(data_dict)
                        try:
                            # send mail to candidate
                            if 93 not in email_sets:
                                mail_type = 'BOOSTER_CANDIDATE'
                                send_email_task.delay(
                                    to_emails, mail_type,
                                    candidate_data, status=93, oi=oi.pk)

                            SendSMS().send(
                                sms_type="BOOSTER_CANDIDATE",
                                data=candidate_data)
                            last_oi_status = oi.oi_status
                            oi.oi_status = 62
                            oi.last_oi_status = last_oi_status
                            oi.save()
                            oi.orderitemoperation_set.create(
                                oi_status=62,
                                last_oi_status=last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user,
                            )
                            mail_send += 1

                        except Exception as e:
                            error_message = "Mail Action Failed on item id - %s due to %s" % (oi.id, str(e))
                            messages.add_message(request, messages.ERROR, error_message)
                    else:
                        continue

                try:
                    recruiter_data.update({
                        "data": candidate_list,
                    })
                    # send mail to rectuter
                    recruiters = settings.BOOSTER_RECRUITERS
                    mail_type = 'BOOSTER_RECRUITER'
                    if candidate_list != []:
                        send_email_task.delay(
                            recruiters, mail_type, recruiter_data)
                        for oi in booster_ois:
                            oi.emailorderitemoperation_set.create(
                                email_oi_status=92)
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
                    obj.oi_status = 23  # pending Approval
                    obj.last_oi_status = last_oi_status
                    obj.save()
                    approval += 1
                    obj.orderitemoperation_set.create(
                        oi_status=23,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems send for approval.'
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
            orderitems = OrderItem.objects.filter(id__in=selected_id).select_related('order', 'product', 'partner')
            for oi in orderitems:
                order = oi.order
                mid_out_sent = True
                if order.midout_sent_on and timezone.now().date() == order.midout_sent_on.date():
                    mid_out_sent = False

                if mid_out_sent:
                    # mail to user about writer information
                    to_emails = [order.email]
                    mail_type = "PENDING_ITEMS"
                    token = AutoLogin().encode(oi.order.email, oi.order.candidate_id, days=None)
                    data = {}
                    data.update({
                        'subject': 'To initiate your services fulfil these details',
                        'username': order.first_name if order.first_name else order.candidate_id,
                        'type_flow': oi.product.type_flow,
                        'product_name': oi.product.name,
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
