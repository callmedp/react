import json

from django.views.generic import TemplateView, ListView, DetailView
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

from order.models import Order, OrderItem
from blog.mixins import PaginationMixin

from .welcome_form import WelcomeCallActionForm
from .order_form import (
    ResumeUploadForm,
    InboxActionForm,
    FileUploadForm,
    MessageForm,)


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(OrderListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['order_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
        })
        return context

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        user = self.request.user

        if user.has_perm('order.can_show_all_order'):
            queryset = queryset
        elif user.has_perm('order.can_show_paid_order'):
            queryset = queryset.filter(status=1)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(email__icontains=self.query) | Q(mobile__icontains=self.query))
        except:
            pass
        return queryset


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
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
        context.update({
            "action_form": WelcomeCallActionForm(),
            "messages": alert,
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeCallVeiw, self).get_queryset()
        queryset = queryset.filter(status=1, welcome_call_done=False).order_by('payment_date')
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(email__icontains=self.query) | Q(mobile__icontains=self.query))
        except:
            pass
        return queryset


@method_decorator(permission_required('order.can_show_midout_queue', login_url='/console/login/'), name='dispatch')
class MidOutQueueView(TemplateView, PaginationMixin):
    # context_object_name = 'midout_list'
    template_name = 'console/order/midout-list.html'
    model = OrderItem
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(MidOutQueueView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ResumeUploadForm(request.POST, request.FILES)
        obj_pk = request.POST.get('oi_pk', None)
        if form.is_valid():
            try:
                oi = OrderItem.objects.get(pk=obj_pk)
                order = oi.order
                oi.oi_resume = request.FILES.get('oi_resume', '')
                oi.save()
                messages.add_message(request, messages.SUCCESS, 'resume uploded Successfully')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            context = self.get_context_data(**kwargs)
            context.update({
                "form": form,
            })
            error_message = form.errors.get('oi_resume')
            if error_message:
                messages.add_message(request, messages.ERROR, error_message)
            # return TemplateResponse(
            #   request, self.template_name, context)
        return HttpResponseRedirect(reverse("console:queue-midout"))

    def get_context_data(self, **kwargs):
        context = super(MidOutQueueView, self).get_context_data(**kwargs)
        midout_list = self.get_queryset()
        paginator = Paginator(midout_list, self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
            "form": ResumeUploadForm(),
        })
        return context

    def get_queryset(self):
        queryset = OrderItem.objects.all().select_related('order', 'product')
        queryset = queryset.filter(order__status=1,
            product__type_flow__in=[1], oi_resume='')
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query))
        except:
            pass

        return queryset


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(InboxQueueVeiw, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                data = {"display_message": ''}
                orderitem_list = request.POST.getlist('selected_id[]', [])
                writer_pk = int(request.POST.get('action_type', '0'))
                orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list)
                if writer_pk == 0:
                    data['display_message'] = 'Please select valid action first.'
                else:
                    User = get_user_model()
                    try:
                        writer = User.objects.get(pk=writer_pk)
                        for obj in orderitem_objs:
                            obj.assigned_to = writer
                            obj.assigned_by = request.user
                            obj.save()
                            obj.orderitemoperation_set.create(
                                oi_status=1,
                                last_oi_status=obj.oi_status,
                                assigned_to=obj.assigned_to,
                                added_by=request.user
                            )
                            obj.orderitemoperation_set.create(
                                oi_status=obj.oi_status,
                                last_oi_status=1,
                                assigned_to=obj.assigned_to,
                                added_by=request.user
                            )
                            # mail to user about writer information
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
        context.update({
            "action_form": InboxActionForm(),
            "messages": alert,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(InboxQueueVeiw, self).get_queryset()
        queryset = queryset.filter(order__status=1, product__type_flow__in=[1], oi_draft='').exclude(oi_resume='').exclude(oi_status=9)
        user = self.request.user
        if user.has_perm('order.can_show_unassigned_inbox') and user.has_perm('order.can_show_assigned_inbox'):
            pass
        elif user.has_perm('order.can_show_unassigned_inbox'):
            queryset = queryset.filter(assigned_to=None)
        elif user.has_perm('order.can_show_assigned_inbox'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InboxQueueVeiw, self).dispatch(request, *args, **kwargs)


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
                if obj.oi_status == 8:
                    obj.draft_counter += 1
                elif not obj.draft_counter:
                        obj.draft_counter += 1
                obj.oi_status = 5  # pending Approval
                obj.last_oi_status = last_status
                obj.draft_added_on = timezone.now()
                obj.save()
                messages.add_message(request, messages.SUCCESS, 'draft uploded Successfully')
                obj.orderitemoperation_set.create(
                    oi_draft=obj.oi_draft,
                    draft_counter=obj.draft_counter,
                    oi_status=4,
                    last_oi_status=last_status,
                    assigned_to=obj.assigned_to,
                    added_by=request.user)
                obj.orderitemoperation_set.create(
                    oi_status=obj.oi_status,
                    last_oi_status=4,
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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ApprovalQueueVeiw, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(ApprovalQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['approval_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
        })
        return context

    def get_queryset(self):
        queryset = super(ApprovalQueueVeiw, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=5, product__type_flow__in=[1]).exclude(oi_status=9)
        # user = self.request.user
        # if user.has_perm('order.can_show_unassigned_inbox') and user.has_perm('order.can_show_assigned_inbox'):
        #     pass
        # elif user.has_perm('order.can_show_unassigned_inbox'):
        #     queryset = queryset.filter(assigned_to=None)
        # elif user.has_perm('order.can_show_assigned_inbox'):
        #     queryset = queryset.filter(assigned_to=user)
        # else:
        #     queryset = queryset.none()
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to')


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ApprovedQueueVeiw, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(ApprovedQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['approved_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
        })
        return context

    def get_queryset(self):
        queryset = super(ApprovedQueueVeiw, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=6, product__type_flow__in=[1])
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to')


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(RejectedByAdminQueue, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(RejectedByAdminQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbyadmin_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(RejectedByAdminQueue, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=7, product__type_flow__in=[1])
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to')


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(RejectedByCandidateQueue, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(RejectedByCandidateQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbycandidate_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "draft_form": FileUploadForm(),
            "message_form": MessageForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(RejectedByCandidateQueue, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=8, product__type_flow__in=[1])
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to')


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

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(AllocatedQueueVeiw, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            orderitem_list = request.POST.getlist('table_records', [])
            writer_pk = int(request.POST.get('action_type', '0'))
            orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list)
            if writer_pk == 0:
                messages.add_message(request, messages.ERROR, 'Please select valid action first')
            else:
                User = get_user_model()
                try:
                    writer = User.objects.get(pk=writer_pk)
                    for obj in orderitem_objs:
                        obj.assigned_to = writer
                        obj.assigned_by = request.user
                        obj.save()
                        obj.orderitemoperation_set.create(
                            oi_status=1,
                            last_oi_status=obj.oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user
                        )
                        obj.orderitemoperation_set.create(
                            oi_status=obj.oi_status,
                            last_oi_status=1,
                            assigned_to=obj.assigned_to,
                            added_by=request.user
                        )
                        # mail to user about writer information
                    messages.add_message(request, messages.SUCCESS, str(len(orderitem_objs)) + ' orderitems are Re Assigned')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, str(e))
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('console:queue-allocated'))

    def get_context_data(self, **kwargs):
        context = super(AllocatedQueueVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['allocated_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "action_form": InboxActionForm(),
            "messages": alert,
        })

        return context

    def get_queryset(self):
        queryset = super(AllocatedQueueVeiw, self).get_queryset()
        queryset = queryset.filter(order__status=1, product__type_flow__in=[1]).exclude(assigned_to=None)
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__id__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by')