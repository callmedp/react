import json
import datetime
import logging

from collections import OrderedDict
from decimal import Decimal

from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView, View, DetailView
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from order.models import RefundRequest, Order, OrderItem
from blog.mixins import PaginationMixin
from order.choices import TYPE_REFUND

from .decorators import Decorate, stop_browser_cache, has_group, check_group
from .refund_form import RefundFilterForm


class RefundInfoMixin(object):
    def get_order_item_list(self, order=None):
        order_items = []
        if order:
            parent_ois = order.orderitems.filter(
                parent=None).select_related('product', 'partner').exclude(oi_status=163)
            for p_oi in parent_ois:
                data = {}
                if p_oi.product.type_flow == 16:
                    continue
                data['oi'] = p_oi
                data['addons'] = order.orderitems.filter(
                    parent=p_oi,
                    is_addon=True,
                    no_process=False).select_related('product', 'partner').exclude(oi_status=163)
                data['variations'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_variation=True).select_related('product', 'partner').exclude(oi_status=163)
                data['combos'] = order.orderitems.filter(
                    parent=p_oi, no_process=False,
                    is_combo=True).select_related('product', 'partner').exclude(oi_status=163)
                order_items.append(data)
        return order_items

    def update_refund_oi_status(self, status, refund_obj):
        if refund_obj and status:
            refunditems = refund_obj.refunditem_set.all().select_related('oi')
            for refunditem in refunditems:
                oi = refunditem.oi
                last_oi_status = oi.oi_status
                oi.oi_status = status
                oi.last_oi_status = last_oi_status
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to,
                    added_by=self.request.user,
                )


@method_decorator(permission_required('order.can_view_refund_approval_queue', login_url='/console/login/'), name='dispatch')
class RefundRequestApprovalView(ListView, PaginationMixin):
    context_object_name = 'refund_approval_list'
    template_name = 'console/refund/refund-approval-list.html'
    model = RefundRequest
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.created, self.status = '', -1

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.created = request.GET.get('created', '')
        try:
            self.status = int(request.GET.get('status', -1))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get status %s' % str(e))
            self.status = -1
        return super(RefundRequestApprovalView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(
            RefundRequestApprovalView, self).get_context_data(**kwargs)
        paginator = Paginator(
            context['refund_approval_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "status": self.status,
        }
        filter_form = RefundFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
        })
        return context

    def get_queryset(self):
        queryset = super(RefundRequestApprovalView, self).get_queryset()
        queryset = queryset.filter(status__in=[1, 3, 5, 8])
        user = self.request.user
        if user.is_superuser:
            pass
        elif has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
            queryset = queryset.filter(status=1)

        elif has_group(user=user, grp_list=settings.BUSINESS_HEAD_GROUP_LIST):
            queryset = queryset.filter(status=3)

        elif has_group(user=user, grp_list=settings.DEPARTMENT_HEAD_GROUP_LIST):
            queryset = queryset.filter(status=5)

        elif has_group(user=user, grp_list=settings.FINANCE_GROUP_LIST):
            queryset = queryset.filter(status=8)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(order__number__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            pass

        try:
            if self.status != -1:
                queryset = queryset.filter(status=self.status)
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
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
            else:
                end_date = timezone.now()
                start_date = end_date - datetime.timedelta(days=30)
                queryset = queryset.filter(
                    created__range=[start_date, end_date])

                start = start_date.strftime("%d/%m/%Y")
                end = end_date.strftime("%d/%m/%Y")

                self.created = start + ' - ' + end
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set within date-range%s'%str(e))
            pass

        return queryset.order_by('-modified')


@method_decorator(permission_required('order.can_view_refund_request_queue', login_url='/console/login/'), name='dispatch')
class RefundOrderRequestView(ListView, PaginationMixin):
    context_object_name = 'refund_request_list'
    template_name = 'console/refund/refund-request-list.html'
    model = RefundRequest
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.created, self.status = '', -1

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.created = request.GET.get('created', '')
        try:
            self.status = int(request.GET.get('status', -1))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get status %s' % str(e))
            self.status = -1
        return super(RefundOrderRequestView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(
            RefundOrderRequestView, self).get_context_data(**kwargs)
        paginator = Paginator(
            context['refund_request_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "created": self.created,
            "status": self.status,
        }
        filter_form = RefundFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": filter_form,
        })
        return context

    def get_queryset(self):
        queryset = super(RefundOrderRequestView, self).get_queryset()
        user = self.request.user
        grp_list = settings.OPS_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST + settings.WELCOMECALL_GROUP_LIST
        if user.is_superuser:
            pass
        elif has_group(user=user, grp_list=grp_list):
            pass
        else:
            queryset = queryset.none()

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(order__number__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            pass

        try:
            if self.status != -1:
                queryset = queryset.filter(status=self.status)
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
            else:
                end_date = timezone.now()
                start_date = end_date - datetime.timedelta(days=30)
                queryset = queryset.filter(
                    created__range=[start_date, end_date])

                start = start_date.strftime("%d/%m/%Y")
                end = end_date.strftime("%d/%m/%Y")

                self.created = start + ' - ' + end
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set within date range%s'%str(e))

            pass

        return queryset.order_by('-modified')


class RefundRequestDetail(DetailView, RefundInfoMixin):
    model = RefundRequest
    template_name = "console/refund/refund-request-detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
            user = self.request.user
            if has_group(user=user, grp_list=settings.REFUND_GROUP_LIST):
                pass
            else:
                raise Http404
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(RefundRequestDetail, self).get(request, *args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        try:
            refund_pk = request.POST.get('refund_pk', None)
            txn = request.POST.get('txn', '').strip()
            refund_mode = request.POST.get('refund_mode', 'select').strip()
            refund_obj = RefundRequest.objects.get(pk=refund_pk, status=8)

            if refund_obj and refund_mode and txn and has_group(user=request.user, grp_list=settings.FINANCE_GROUP_LIST):
                if refund_mode in ['neft', 'cheque', 'dd']:
                    last_status = refund_obj.status
                    refund_obj.status = 11
                    refund_obj.last_status = last_status
                    refund_obj.refund_mode = refund_mode
                    refund_obj.txn = txn
                    refund_obj.refund_date = timezone.now()
                    refund_obj.save()

                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        added_by=request.user
                    )
                    self.update_refund_oi_status(
                        status=163, refund_obj=refund_obj)

                    order = refund_obj.order
                    if refund_obj.refund_mode == 'neft':
                        payment_mode = 10
                    else:
                        payment_mode = 4
                    order.ordertxns.create(
                        txn=txn,
                        status=6,
                        payment_mode=payment_mode,
                        payment_date=refund_obj.refund_date,
                        currency=refund_obj.currency,
                        txn_amount=float(refund_obj.refund_amount)
                    )

                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Refund Settled Successfully.')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'select valid refund mode')

                return HttpResponseRedirect(reverse('console:refundrequest-detail', kwargs={"pk": refund_obj.pk}))

        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                str(e))

        if refund_obj:
            return HttpResponseRedirect(reverse('console:refundrequest-detail', kwargs={"pk": refund_obj.pk}))
        return HttpResponseRedirect(reverse('console:refund-request-approval'))

    def get_context_data(self, **kwargs):
        context = super(RefundRequestDetail, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        refund_obj = self.get_object()
        refunditems = refund_obj.refunditem_set.all().select_related('oi')
        refundops = refund_obj.refundoperation_set.all()

        edit_group = settings.OPS_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST
        if refund_obj.status in [0, 1, 9] and has_group(user=self.request.user, grp_list=edit_group):
            edit_permission = True
        else:
            edit_permission = False

        if refund_obj.status == 1 and has_group(user=self.request.user, grp_list=settings.OPS_HEAD_GROUP_LIST):
            approval_permission = True
        elif refund_obj.status == 3 and has_group(user=self.request.user, grp_list=settings.BUSINESS_HEAD_GROUP_LIST):
            approval_permission = True
        elif refund_obj.status == 5 and has_group(user=self.request.user, grp_list=settings.DEPARTMENT_HEAD_GROUP_LIST):
            approval_permission = True
        else:
            approval_permission = False

        context.update({
            "refund_obj": refund_obj,
            "order": refund_obj.order,
            "messages": alert,
            "refunditems": refunditems,
            "refundops": refundops,
            "edit_permission": edit_permission,
            "approval_permission": approval_permission,
        })

        return context


@Decorate(stop_browser_cache())
class RefundRequestEditView(DetailView, RefundInfoMixin):
    template_name = 'console/refund/refundrequest-edit.html'
    model = RefundRequest
    http_method_names = [u'get', u'post']

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(pk=pk, status__in=[0, 1, 9])
        try:
            obj = queryset.get()
            user = self.request.user
            edit_group = settings.OPS_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST + settings.WELCOMECALL_GROUP_LIST
            if obj.status in [0, 1, 9] and has_group(user=user, grp_list=edit_group):
                pass
            else:
                raise Http404
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(RefundRequestEditView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist('item_name', [])
        attached_file = request.FILES.get('attach_file', '')
        message = request.POST.get('message', '').strip()
        valid = True
        refund_obj = self.get_object()
        order = refund_obj.order

        if not refund_obj:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You can edit request only once you raised the request first.')

            messages.add_message(
                self.request,
                messages.ERROR,
                'A refund request is already raise on this order, you can edit that request only.')

        elif refund_obj and refund_obj.status in [3, 5, 7]:
            messages.add_message(
                self.request,
                messages.ERROR,
                'You can\'t edit this request, this request went for higher level approval.')
            messages.add_message(
                self.request,
                messages.ERROR,
                'You can\'t edit this request only, if this request rejected by higher level approval.')
            valid = False

        orderitems = order.orderitems.all()

        if not message and valid:
            messages.add_message(
                self.request,
                messages.ERROR, "message is required")
            valid = False

        elif not selected_items and valid:
            valid = False
            messages.add_message(
                self.request, messages.ERROR,
                "Atleast one item required to update refund request")

        elif valid and orderitems.filter(id__in=selected_items).count() != len(selected_items):
            messages.add_message(
                request, messages.ERROR,
                "Please select valid items to refund")
            valid = False
        elif valid and selected_items and order.status in [1, 3]:
            for item_id in selected_items:
                oi = orderitems.get(id=item_id)
                payment_type = 'type-payment' + str(item_id)
                payment_type = request.POST.get(payment_type)
                if payment_type == 'full':
                    pass
                elif payment_type == 'partial':
                    refund_amount = 'refund-amount-' + str(item_id)
                    refund_amount = Decimal(request.POST.get(refund_amount, 0))
                    if refund_amount == Decimal(0):
                        messages.add_message(
                            request, messages.ERROR,
                            "partial payment must be greater than 0")
                        valid = False
                    elif refund_amount >= oi.get_refund_amount():
                        messages.add_message(
                            request, messages.ERROR,
                            "partial payment must be less than max refund amount")
                        valid = False
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        "Please select valid payment type")
                    valid = False

            if valid and selected_items:
                refund_items = refund_obj.refunditem_set.all()
                excluded_items = list(refund_items.all().values_list('oi', flat=True))
                excluded_ois = order.orderitems.filter(id__in=excluded_items)
                refund_items.all().delete()
                for oi in excluded_ois:
                    if str(oi.pk) not in selected_items:
                        if oi.oi_status == 161:
                            last_oi_status = oi.oi_status
                            oi.oi_status = oi.last_oi_status
                            oi.last_oi_status = last_oi_status
                            oi.save()
                            oi.orderitemoperation_set.create(
                                oi_status=oi.oi_status,
                                last_oi_status=oi.last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user
                            )

                        if oi.is_combo and not oi.parent:
                            combos = oi.order.orderitems.filter(
                                parent=oi, is_combo=True)
                            for combo in combos:
                                if combo.oi_status == 161:
                                    last_oi_status = combo.oi_status
                                    combo.oi_status = combo.last_oi_status
                                    combo.last_oi_status = last_oi_status
                                    combo.save()

                                    combo.orderitemoperation_set.create(
                                        oi_status=combo.oi_status,
                                        last_oi_status=combo.last_oi_status,
                                        assigned_to=combo.assigned_to,
                                        added_by=request.user
                                    )

                total_refund = Decimal(0)
                for item_id in selected_items:
                    oi = orderitems.get(id=item_id)
                    payment_type = 'type-payment' + str(item_id)
                    payment_type = request.POST.get(payment_type)
                    if payment_type == 'full':
                        refund_amount = Decimal(oi.get_refund_amount())
                        refund_obj.refunditem_set.create(
                            oi=oi,
                            type_refund=payment_type,
                            amount=refund_amount
                        )
                        total_refund += refund_amount
                        if oi.oi_status != 161:
                            oi.last_oi_status = oi.oi_status
                            oi.oi_status = 161
                        oi.save()
                        ops_set = oi.orderitemoperation_set.all()
                        if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                            oi.orderitemoperation_set.create(
                                oi_status=oi.oi_status,
                                last_oi_status=oi.last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user
                            )

                        if oi.is_combo and not oi.parent:
                            combos = oi.order.orderitems.filter(parent=oi, is_combo=True)
                            for combo in combos:
                                if combo.oi_status != 161:
                                    combo.last_oi_status = combo.oi_status
                                    combo.oi_status = 161
                                combo.save()
                                ops_set = combo.orderitemoperation_set.all()
                                if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                    combo.orderitemoperation_set.create(
                                        oi_status=combo.oi_status,
                                        last_oi_status=combo.last_oi_status,
                                        assigned_to=combo.assigned_to,
                                        added_by=request.user
                                    )
                    elif payment_type == 'partial':
                        refund_amount = 'refund-amount-' + str(item_id)
                        refund_amount = Decimal(request.POST.get(refund_amount, 0))
                        if refund_amount > 0 and refund_amount < oi.get_refund_amount():
                            refund_obj.refunditem_set.create(
                                oi=oi,
                                type_refund=payment_type,
                                amount=refund_amount
                            )
                            total_refund += refund_amount
                            if oi.oi_status != 161:
                                oi.last_oi_status = oi.oi_status
                                oi.oi_status = 161
                            oi.save()
                            ops_set = oi.orderitemoperation_set.all()
                            if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                oi.orderitemoperation_set.create(
                                    oi_status=oi.oi_status,
                                    last_oi_status=oi.last_oi_status,
                                    assigned_to=oi.assigned_to,
                                    added_by=request.user
                                )

                            if oi.is_combo and not oi.parent:
                                combos = oi.order.orderitems.filter(parent=oi, is_combo=True)
                                for combo in combos:
                                    if combo.oi_status != 161:
                                        combo.last_oi_status = combo.oi_status
                                        combo.oi_status = 161
                                    combo.save()
                                    ops_set = combo.orderitemoperation_set.all()
                                    if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                        combo.orderitemoperation_set.create(
                                            oi_status=combo.oi_status,
                                            last_oi_status=combo.last_oi_status,
                                            assigned_to=combo.assigned_to,
                                            added_by=request.user
                                        )

                refund_obj.refund_amount = total_refund
                refund_obj.message = message
                refund_obj.document = attached_file
                last_status = refund_obj.status
                refund_obj.status = 1
                # if request.user.has_group 'ops'
                #     refund_obj.last_status = refund_obj.status
                #     refund_obj.status = 9

                refund_obj.save()

                refund_obj.refundoperation_set.create(
                    status=12,
                    last_status=last_status,
                    message=message,
                    added_by=request.user,
                )
                messages.add_message(
                    request, messages.SUCCESS,
                    "refund request changed successfully of order number %s" % (order.number))
        next_url = reverse('console:refundrequest-edit', kwargs={"pk": refund_obj.pk})
        return HttpResponseRedirect(next_url)

    def get_context_data(self, **kwargs):
        context = super(
            RefundRequestEditView, self).get_context_data(**kwargs)
        refund_obj = self.get_object()
        order = refund_obj.order
        alert = messages.get_messages(self.request)

        context.update({
            "messages": alert,
        })

        if order.status in [1, 3] and refund_obj.status in [0, 1, 9]:
            orderitems = self.get_order_item_list(order=order)
            refunditems = refund_obj.refunditem_set.all()
            refunditems_ois = refunditems.values_list('oi', flat=True)
            refunditems = refunditems.select_related('oi')
            refundedit_items = []
            for data in orderitems:
                data_dict = {}
                oi = data.get('oi')
                addons = data.get('addons')
                variations = data.get('variations')
                combos = data.get('combos')
                refund_item = None
                if oi.product.is_course and oi.is_variation and variations:
                    if variations.first().pk in refunditems_ois:
                        refund_item = refunditems.get(oi=variations.first())
                    else:
                        refund_item = None
                    data_dict = {
                        "oi": variations.first(),
                        "combos": [],
                        "refund_item": refund_item
                    }
                    refundedit_items.append(data_dict)
                    for addon in addons:
                        if addon.pk in refunditems_ois:
                            refund_item = refunditems.get(oi=addon)
                        else:
                            refund_item = None

                        data_dict = {
                            "oi": addon,
                            "combos": [],
                            "refund_item": refund_item,
                        }
                        refundedit_items.append(data_dict)
                else:
                    if oi.pk in refunditems_ois:
                        refund_item = refunditems.get(oi=oi)
                    else:
                        refund_item = None
                    data_dict = {
                        "oi": oi,
                        "combos": combos,
                        "refund_item": refund_item,
                    }
                    refundedit_items.append(data_dict)
                    for var in variations:
                        if var.pk in refunditems_ois:
                            refund_item = refunditems.get(oi=var)
                        else:
                            refund_item = None

                        data_dict = {
                            "oi": var,
                            "combos": [],
                            "refund_item": refund_item,
                        }
                        refundedit_items.append(data_dict)
                    for addon in addons:
                        if addon.pk in refunditems_ois:
                            refund_item = refunditems.get(oi=addon)
                        else:
                            refund_item = None

                        data_dict = {
                            "oi": addon,
                            "combos": [],
                            "refund_item": refund_item,
                        }
                        refundedit_items.append(data_dict)

            cancel_permission = False

            if has_group(user=self.request.user, grp_list=settings.OPS_HEAD_GROUP_LIST):
                cancel_permission = True
            elif has_group(user=self.request.user, grp_list=settings.OPS_GROUP_LIST):
                cancel_permission = True

            context.update({
                "order": order,
                "refunditems": refunditems,
                "refund_obj": refund_obj,
                "refundedit_items": refundedit_items,
                "cancel_permission": cancel_permission,
            })
            context.update({
                "type_refund_dict": OrderedDict(TYPE_REFUND),
            })
        else:
            messages.add_message(
                self.request, messages.ERROR,
                "please select valid refund request to edit.")
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.OPS_GROUP_LIST, settings.OPS_HEAD_GROUP_LIST]))
class RefundRaiseRequestView(TemplateView, RefundInfoMixin):
    template_name = 'console/refund/raise-refundrequest.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.query = ''

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('query', '')
        return super(RefundRaiseRequestView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist('item_name', [])
        attached_file = request.FILES.get('attach_file', '')
        message = request.POST.get('message', '').strip()
        order_pk = request.POST.get('order_pk', None)
        valid = True
        order = None
        try:
            order = Order.objects.get(pk=order_pk, status__in=[1, 3])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get order object %s' % str(e))

            messages.add_message(
                request, messages.ERROR,
                'please select valid order to raise refund request.')
            valid = False

        if valid:
            refund_objs = order.refundrequest_set.all().exclude(
                status__in=[11, 13])
            orderitems = order.orderitems.all()
            if refund_objs.exists():
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'A refund request is already raise on this order, you can edit that request only.')
                valid = False

        if not message and valid:
            messages.add_message(
                self.request,
                messages.ERROR, "message is required")
            valid = False
        elif not selected_items and valid:
            valid = False
            messages.add_message(
                self.request, messages.ERROR,
                "Atleast one item required to raise refund request")
        elif valid and orderitems.filter(id__in=selected_items).count() != len(selected_items):
            messages.add_message(
                request, messages.ERROR,
                "Please select valid items to refund")
            valid = False
        elif valid and selected_items and order.status in [1, 3]:
            for item_id in selected_items:
                oi = orderitems.get(id=item_id)
                payment_type = 'type-payment' + str(item_id)
                payment_type = request.POST.get(payment_type)
                if payment_type == 'full':
                    pass
                elif payment_type == 'partial':
                    refund_amount = 'refund-amount-' + str(item_id)
                    refund_amount = Decimal(request.POST.get(refund_amount, 0))
                    if refund_amount == Decimal(0):
                        messages.add_message(
                            request, messages.ERROR,
                            "partial payment must be greater than 0")
                        valid = False
                    elif refund_amount >= oi.get_refund_amount():
                        messages.add_message(
                            request, messages.ERROR,
                            "partial payment must be less than max refund amount")
                        valid = False
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        "Please select valid refund type")
                    valid = False

            if valid and selected_items:
                refund_obj = RefundRequest.objects.create(
                    order=order,
                    message=message,
                    document=attached_file,
                    status=1,
                    last_status=0,
                    currency=order.currency,
                    added_by=request.user
                )
                total_refund = Decimal(0)
                for item_id in selected_items:
                    oi = orderitems.get(id=item_id)
                    payment_type = 'type-payment' + str(item_id)
                    payment_type = request.POST.get(payment_type)
                    if payment_type == 'full':
                        refund_amount = Decimal(oi.get_refund_amount())
                        refund_obj.refunditem_set.create(
                            oi=oi,
                            type_refund=payment_type,
                            amount=refund_amount
                        )
                        total_refund += refund_amount
                        oi.last_oi_status = oi.oi_status
                        oi.oi_status = 161
                        oi.save()
                        ops_set = oi.orderitemoperation_set.all()
                        if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                            oi.orderitemoperation_set.create(
                                oi_status=oi.oi_status,
                                last_oi_status=oi.last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user
                            )
                        if oi.is_combo and not oi.parent:
                            combos = oi.order.orderitems.filter(parent=oi, is_combo=True)
                            for combo in combos:
                                combo.last_oi_status = combo.oi_status
                                combo.oi_status = 161
                                combo.save()
                                ops_set = combo.orderitemoperation_set.all()
                                if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                    combo.orderitemoperation_set.create(
                                        oi_status=combo.oi_status,
                                        last_oi_status=combo.last_oi_status,
                                        assigned_to=combo.assigned_to,
                                        added_by=request.user
                                    )

                    elif payment_type == 'partial':
                        refund_amount = 'refund-amount-' + str(item_id)
                        refund_amount = Decimal(request.POST.get(refund_amount, 0))
                        if refund_amount > 0 and refund_amount < oi.get_refund_amount():
                            refund_obj.refunditem_set.create(
                                oi=oi,
                                type_refund=payment_type,
                                amount=refund_amount
                            )
                            total_refund += refund_amount

                            oi.last_oi_status = oi.oi_status
                            oi.oi_status = 161
                            oi.save()
                            ops_set = oi.orderitemoperation_set.all()
                            if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                oi.orderitemoperation_set.create(
                                    oi_status=oi.oi_status,
                                    last_oi_status=oi.last_oi_status,
                                    assigned_to=oi.assigned_to,
                                    added_by=request.user
                                )

                            if oi.is_combo and not oi.parent:
                                combos = oi.order.orderitems.filter(parent=oi, is_combo=True)
                                for combo in combos:
                                    combo.last_oi_status = combo.oi_status
                                    combo.oi_status = 161
                                    combo.save()
                                    ops_set = combo.orderitemoperation_set.all()
                                    if (ops_set.exists() and ops_set.last().oi_status != 161) or (not ops_set.exists()):
                                        combo.orderitemoperation_set.create(
                                            oi_status=combo.oi_status,
                                            last_oi_status=combo.last_oi_status,
                                            assigned_to=combo.assigned_to,
                                            added_by=request.user
                                        )

                refund_obj.refund_amount = total_refund
                refund_obj.save()

                refund_obj.refundoperation_set.create(
                    status=9,
                    message=message,
                    last_status=refund_obj.last_status,
                    added_by=request.user,
                )

                refund_obj.refundoperation_set.create(
                    status=refund_obj.status,
                    last_status=9,
                    added_by=request.user,
                )
                messages.add_message(
                    request, messages.SUCCESS,
                    "refund request raised successfully on order number %s" %(order.number))
        if valid:
            next_url = reverse('console:refund-request')
        else:
            next_url = reverse('console:refund-raiserequest') + '?query=' + str(order.number)
        return HttpResponseRedirect(next_url)

    def get_context_data(self, **kwargs):
        context = super(
            RefundRaiseRequestView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = None
        if self.query:
            try:
                order = Order.objects.get(number=self.query, status__in=[1, 3])
            except Exception as e:
                logging.getLogger('error_log').error('unable to get order object%s' % str(e))
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'Order not found.'
                )

        context.update({
            "messages": alert,
            "query": self.query,
        })
        if order:
            refund_objs = order.refundrequest_set.all().exclude(
                status__in=[11, 13])
            if refund_objs.exists():
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'A refund request is already raise on this order, you can edit that request only.')
                return context
            orderitems = self.get_order_item_list(order=order)

            refundedit_items = []
            for data in orderitems:
                data_dict = {}
                oi = data.get('oi')
                addons = data.get('addons')
                variations = data.get('variations')
                combos = data.get('combos')
                if oi.product.is_course and variations:
                    data_dict = {
                        "oi": variations.first(),
                        "combos": [],
                    }
                    refundedit_items.append(data_dict)
                    for addon in addons:
                        data_dict = {
                            "oi": addon,
                            "combos": [],
                        }
                        refundedit_items.append(data_dict)

                else:
                    data_dict = {
                        "oi": oi,
                        "combos": combos,
                    }
                    refundedit_items.append(data_dict)
                    for var in variations:
                        data_dict = {
                            "oi": var,
                            "combos": [],
                        }
                        refundedit_items.append(data_dict)
                    for addon in addons:
                        data_dict = {
                            "oi": addon,
                            "combos": [],
                        }
                        refundedit_items.append(data_dict)

            if not refundedit_items:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'This order is already refunded or there is no item to refund.')
                return context
            context.update({
                "order": order,
                "refundedit_items": refundedit_items,
            })

        context.update({
            "type_refund_dict": OrderedDict(TYPE_REFUND),
        })
        return context


class ValidateCheckedItems(View):
    def get(self, request, *args, **kwargs):
        item_list = []
        data = {
            "status": 0,
            "item_list": item_list,
            "error_message": '',
        }
        item_id = request.GET.get('item_id', None)
        if request.is_ajax() and request.user.is_authenticated and item_id:
            try:
                var_list = []
                addon_list = []
                oi = OrderItem.objects.get(id=item_id, order__status__in=[1, 3])
                if not oi.parent:
                    variations = oi.order.orderitems.filter(
                        parent=oi, is_variation=True)
                    var_list = list(variations.all().values_list(
                        'id', flat=True))
                    addons = oi.order.orderitems.filter(
                        parent=oi, is_addon=True)
                    addon_list = list(addons.all().values_list(
                        'id', flat=True))
                elif oi.is_variation:
                    parent_oi = oi.parent
                    variations = parent_oi.order.orderitems.filter(
                        parent=parent_oi, is_variation=True)
                    if variations.count() > 1:
                        variations = []
                    else:
                        variations = variations.exclude(id=oi.pk)

                        addons = parent_oi.order.orderitems.filter(
                            parent=parent_oi, is_addon=True)
                        if not parent_oi.product.is_course and parent_oi.no_process:
                            variations = variations | parent_oi.order.orderitems.filter(id=parent_oi.pk)
                        var_list = list(variations.all().values_list(
                            'id', flat=True))
                        addon_list = list(addons.all().values_list(
                            'id', flat=True))

                item_list.append(oi.pk)
                data['item_list'] = item_list + addon_list + var_list
                data['status'] = 1

            except Exception as e:
                data['error_message'] = str(e)

        return HttpResponse(json.dumps(data), content_type="application/json")


class ValidateUnCheckedItems(View):
    def get(self, request, *args, **kwargs):
        item_list = []
        data = {
            "status": 0,
            "item_list": item_list,
            "error_message": '',
        }
        item_id = request.GET.get('item_id', None)
        if request.is_ajax() and request.user.is_authenticated and item_id:
            try:
                var_list = []
                addon_list = []
                oi = OrderItem.objects.get(id=item_id, order__status__in=[1, 3])
                if not oi.parent:
                    variations = oi.order.orderitems.filter(
                        parent=oi, is_variation=True)
                    var_list = list(variations.all().values_list(
                        'id', flat=True))
                    addons = oi.order.orderitems.filter(
                        parent=oi, is_addon=True)
                    addon_list = list(addons.all().values_list(
                        'id', flat=True))
                elif oi.is_variation:
                    parent_oi = oi.parent
                    if not parent_oi.product.is_course and parent_oi.no_process:
                        variations = parent_oi.order.orderitems.filter(
                            id=parent_oi.pk)
                        var_list = list(variations.all().values_list(
                            'id', flat=True))
                elif oi.is_addon:
                    parent_oi = oi.parent
                    variations = oi.order.orderitems.filter(
                        parent=parent_oi, is_variation=True)
                    if parent_oi.product.is_course and parent_oi.is_variation:
                        pass
                    else:
                        variations = variations | oi.order.orderitems.filter(
                            id=parent_oi.pk
                        )
                    var_list = list(variations.all().values_list(
                        'id', flat=True))
                item_list.append(oi.pk)
                data['item_list'] = item_list + addon_list + var_list
                data['status'] = 1

            except Exception as e:
                data['error_message'] = str(e)

        return HttpResponse(json.dumps(data), content_type="application/json")


class RejectRefundRequestView(View):
    def post(self, request, *args, **kwargs):
        try:
            message = request.POST.get('message', '').strip()
            refund_pk = request.POST.get('refund_pk', None)
            if message and refund_pk:
                refund_obj = RefundRequest.objects.get(
                    pk=refund_pk, status__in=[1, 3, 5])
                user = request.user
                if refund_obj.status == 1 and has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    refund_obj.status = 9
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                elif refund_obj.status == 3 and has_group(user=user, grp_list=settings.BUSINESS_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    refund_obj.status = 1
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                elif refund_obj.status == 5 and has_group(user=user, grp_list=settings.DEPARTMENT_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    refund_obj.status = 3
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                else:
                    raise PermissionDenied

                messages.add_message(
                    request, messages.SUCCESS,
                    'Refund Request %s rejected Successfully.' % (refund_obj.order.number))

                return HttpResponseRedirect(reverse('console:refund-request-approval'))

        except Exception as e:
            messages.add_message(
                request, messages.ERROR,
                str(e))
        return HttpResponseRedirect(reverse('console:refund-request'))


class ApproveRefundRequestView(View, RefundInfoMixin):
    def post(self, request, *args, **kwargs):
        try:
            message = request.POST.get('message', '').strip()
            refund_pk = request.POST.get('refund_pk', None)
            if message and refund_pk:
                refund_obj = RefundRequest.objects.get(
                    pk=refund_pk, status__in=[1, 3, 5])
                user = request.user
                if refund_obj.status == 1 and has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    refund_obj.status = 3
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                elif refund_obj.status == 3 and has_group(user=user, grp_list=settings.BUSINESS_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    if refund_obj.refund_amount > settings.BUSINESS_APPROVAL_LIMIT:
                        refund_obj.status = 5
                    else:
                        refund_obj.status = 8
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                    if refund_obj.status == 8:
                        self.update_refund_oi_status(status=162, refund_obj=refund_obj)

                elif refund_obj.status == 5 and has_group(user=user, grp_list=settings.DEPARTMENT_HEAD_GROUP_LIST):
                    last_status = refund_obj.status
                    refund_obj.status = 8
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )
                    self.update_refund_oi_status(status=162, refund_obj=refund_obj)
                else:
                    raise PermissionDenied

                messages.add_message(
                    request, messages.SUCCESS,
                    'Refund Request %s Approved Successfully.' % (refund_obj.order.number))

                return HttpResponseRedirect(reverse('console:refund-request-approval'))

        except Exception as e:
            messages.add_message(
                request, messages.ERROR,
                str(e))
        return HttpResponseRedirect(reverse('console:refund-request'))


class CancelRefundRequestView(View, RefundInfoMixin):
    def post(self, request, *args, **kwargs):
        try:
            message = request.POST.get('message', '').strip()
            refund_pk = request.POST.get('refund_pk', None)
            if message and refund_pk:
                refund_obj = RefundRequest.objects.get(
                    pk=refund_pk, status__in=[0, 1, 9])
                user = request.user
                order = refund_obj.order
                grp_list = settings.OPS_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST
                if has_group(user=user, grp_list=grp_list):
                    refund_items = refund_obj.refunditem_set.all()
                    excluded_items = list(refund_items.all().values_list('oi', flat=True))
                    excluded_ois = order.orderitems.filter(id__in=excluded_items)
                    # refund_items.all().delete()
                    for oi in excluded_ois:
                        if oi.oi_status == 161:
                            last_oi_status = oi.oi_status
                            oi.oi_status = oi.last_oi_status
                            oi.last_oi_status = last_oi_status
                            oi.save()

                            oi.orderitemoperation_set.create(
                                oi_status=oi.oi_status,
                                last_oi_status=oi.last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user
                            )

                        if oi.is_combo and not oi.parent:
                            combos = oi.order.orderitems.filter(
                                parent=oi, is_combo=True)
                            for combo in combos:
                                if combo.oi_status == 161:
                                    last_oi_status = combo.oi_status
                                    combo.oi_status = combo.last_oi_status
                                    combo.last_oi_status = last_oi_status
                                    combo.save()
                                    combo.orderitemoperation_set.create(
                                        oi_status=combo.oi_status,
                                        last_oi_status=combo.last_oi_status,
                                        assigned_to=combo.assigned_to,
                                        added_by=request.user
                                    )

                    last_status = refund_obj.status
                    refund_obj.status = 13
                    refund_obj.last_status = last_status
                    refund_obj.save()
                    refund_obj.refundoperation_set.create(
                        status=refund_obj.status,
                        last_status=refund_obj.last_status,
                        message=message,
                        added_by=request.user,
                    )

                else:
                    raise PermissionDenied

                messages.add_message(
                    request, messages.SUCCESS,
                    'Refund Request %s Canceled Successfully.' % (refund_obj.order.number))

                return HttpResponseRedirect(reverse('console:refund-request'))
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'cancel message is required')
                return HttpResponseRedirect(reverse('console:refundrequest-edit'))

        except Exception as e:
            messages.add_message(
                request, messages.ERROR,
                str(e))
        return HttpResponseRedirect(reverse('console:refund-request'))
