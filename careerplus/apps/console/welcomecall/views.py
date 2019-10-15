import logging
import datetime

from django.views.generic import (
    TemplateView, ListView, DetailView,
    View, UpdateView)
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import (
    HttpResponseRedirect,
    Http404)

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.shortcuts import render



from order.models import Order, OrderItem
from blog.mixins import PaginationMixin
from console.decorators import (
    Decorate,
    stop_browser_cache,
    check_group, has_group
)
from core.mixins import InvoiceGenerate
from console.welcome_form import (
    WelcomeCallAssignedForm)
from console.tasks import mock_welcomecall_assignment
from console.order_form import (
    OrderFilterForm,
)
from order.choices import (
    WC_CATEGORY, WC_SUB_CATEGORY1,
    WC_SUB_CATEGORY2, WC_SUB_CATEGORY3,
    WC_SUB_CAT2
)
from emailers.sms import SendSMS

User = get_user_model()


class WelcomeCallInfo(object):
    def get_welcome_list(self, order_items=[]):
        wc_items = []
        for data in order_items:
            data_dict = {}
            oi = data.get('oi')
            # Do not consider assesment items in welcome call
            if (oi.product.type_flow == 16 or oi.product.vendor.slug == 'neo' \
                or oi.product.type_flow ==17 or oi.product.sub_type_flow == 100):
                continue
            addons = data.get('addons')
            variations = data.get('variations')
            combos = data.get('combos')
            if oi.product.is_course and variations:
                data_dict = {
                    "oi": variations.first(),
                    "combos": [],
                }
                wc_items.append(data_dict)
                for addon in addons:
                    data_dict = {
                        "oi": addon,
                        "combos": [],
                    }
                    wc_items.append(data_dict)

            else:
                data_dict = {
                    "oi": oi,
                    "combos": combos,
                }
                wc_items.append(data_dict)
                for var in variations:
                    data_dict = {
                        "oi": var,
                        "combos": [],
                    }
                    wc_items.append(data_dict)
                for addon in addons:
                    data_dict = {
                        "oi": addon,
                        "combos": [],
                    }
                    wc_items.append(data_dict)
        return wc_items


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.OPS_HEAD_GROUP_LIST]))
class WelcomeQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/welcome-queue.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 30
        self.query = ''
        self.assigned = -1
        self.payment_date, self.created = '', ''
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        self.assigned = request.GET.get('assigned', '-1')
        self.sel_opt = request.GET.get('rad_search','')
        return super(WelcomeQueueView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            order_list = request.POST.getlist('table_records', [])
            user = int(request.POST.get('action_type', '0'))
            order_objs = Order.objects.filter(
                id__in=order_list, welcome_call_done=False)
            try:
                user = User.objects.get(
                    pk=user,
                    groups__name__in=settings.WELCOMECALL_GROUP_LIST,
                    is_active=True)
                for order in order_objs:
                    op_status = 1
                    if order.assigned_to:
                        op_status = 2
                    order.assigned_to = user
                    order.save()
                    order.welcomecalloperation_set.create(
                        wc_cat=order.wc_cat,
                        wc_sub_cat=order.wc_sub_cat,
                        wc_status=op_status,
                        assigned_to=order.assigned_to
                    )
                messages.add_message(request, messages.SUCCESS, str(len(order_objs)) + ' orders are assigned successfully.')
            except:
                messages.add_message(request, messages.ERROR, 'Please select valid action first')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

        return HttpResponseRedirect(reverse('console:welcomecall:queue'))

    def get_context_data(self, **kwargs):
        context = super(WelcomeQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "created": self.created,
            "assigned": self.assigned,
        }
        filter_form = OrderFilterForm(initial)
        context.update({
            "action_form": WelcomeCallAssignedForm(),
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
            self.sel_opt: 'checked',
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeQueueView, self).get_queryset()
        queryset = queryset.filter(
            status=1, welcome_call_done=False)
        try:
            if self.query:

                if self.sel_opt == 'number':
                    queryset = queryset.filter(number=self.query)
                elif self.sel_opt == 'email':
                    queryset = queryset.filter(email=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(mobile=self.query)

        except Exception as e:
            logging.getLogger('error_log').error(str(e))
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
            if int(self.assigned) == -2:
                queryset = queryset.exclude(assigned_to=None)
            elif int(self.assigned) == -3:
                queryset = queryset.filter(assigned_to=None)
            elif int(self.assigned) == -1:
                pass
            else:
                queryset = queryset.filter(assigned_to=self.assigned)
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


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST]))
class WelcomeAssignedView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/assigned.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 30

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        return super(WelcomeAssignedView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeAssignedView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        today = timezone.now()
        date_start = datetime.datetime(
            today.year, today.month, today.day, 0, 0, 0, 0, today.tzinfo)
        date_end = datetime.datetime(
            today.year, today.month, today.day, 23, 59, 59, 0, today.tzinfo)
        followup_today = Order.objects.filter(
            assigned_to=self.request.user,
            welcome_call_done=False,
            wc_cat=23,
            wc_follow_up__range=[date_start, date_end]
        )

        context.update({
            "messages": alert,
            "followup_today": followup_today,
            "count_follow_up": len(followup_today),
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeAssignedView, self).get_queryset()
        user = self.request.user
        queryset = queryset.filter(
            assigned_to=user, welcome_call_done=False, wc_cat=0)

        if not queryset:
            mock_welcomecall_assignment(user=user.pk)
        queryset = queryset.order_by('payment_date')
        queryset = queryset[: 1]
        return queryset


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST]))
class WelcomeCallbackView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/callback.html'
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
        return super(WelcomeCallbackView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeCallbackView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "created": self.created,
        }
        filter_form = OrderFilterForm(initial)
        context.update({
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeCallbackView, self).get_queryset()
        queryset = queryset.filter(
            status=1, welcome_call_done=False, wc_cat=23)

        user = self.request.user

        if has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
            pass
        else:
            queryset = queryset.filter(
                assigned_to=user)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(number=self.query) |
                    Q(email=self.query) |
                    Q(mobile=self.query))
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

        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST]))
class WelcomeServiceIssueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/service_issue.html'
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
        return super(WelcomeServiceIssueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeServiceIssueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "created": self.created,
        }
        filter_form = OrderFilterForm(initial)
        context.update({
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeServiceIssueView, self).get_queryset()
        queryset = queryset.filter(
            status=1, welcome_call_done=False, wc_cat=22)

        user = self.request.user

        if has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
            pass
        else:
            queryset = queryset.filter(
                assigned_to=user)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(number=self.query) |
                    Q(email=self.query) |
                    Q(mobile=self.query))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
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
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST]))
class WelcomeCallDoneView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/welcomecall/welcomecall_done.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 30
        self.query = ''
        self.payment_date, self.created = '', ''
        self.sel_opt = 'number'

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.payment_date = request.GET.get('payment_date', '')
        self.created = request.GET.get('created', '')
        self.assigned = request.GET.get('assigned', '-1')
        self.sel_opt = request.GET.get('rad_search','')
        return super(WelcomeCallDoneView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeCallDoneView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "created": self.created,
            "assigned": self.assigned
        }
        filter_form = OrderFilterForm(initial)
        context.update({
            "messages": alert,
            "filter_form": filter_form,
            "query": self.query,
            self.sel_opt: 'checked'
        })

        return context

    def get_queryset(self):
        queryset = super(WelcomeCallDoneView, self).get_queryset()
        queryset = queryset.filter(
            status=1, welcome_call_done=True)

        user = self.request.user

        if has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
            pass
        else:
            queryset = queryset.filter(
                assigned_to=user)

        try:
            if self.query:
                if self.sel_opt == 'number':
                    queryset = queryset.filter(number=self.query)
                elif self.sel_opt =='email':
                    queryset = queryset.filter(email=self.query)
                elif self.sel_opt == 'mobile':
                    queryset = queryset.filter(mobile=self.query)

        except Exception as e:
            logging.getLogger('error_log').error(str(e))

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

        try:
            if int(self.assigned) == -2:
                queryset = queryset.exclude(assigned_to=None)
            elif int(self.assigned) == -3:
                queryset = queryset.filter(assigned_to=None)
            elif int(self.assigned) == -1:
                pass
            else:
                queryset = queryset.filter(assigned_to=self.assigned)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        return queryset.order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST]))
class WelcomeCallUpdateView(DetailView, WelcomeCallInfo):
    model = Order
    template_name = "console/welcomecall/wc_detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(
                pk=pk, welcome_call_done=False)
        try:
            obj = queryset.get()
            user = self.request.user
            if obj.assigned_to == user or has_group(user=user, grp_list=settings.OPS_HEAD_GROUP_LIST):
                pass
            else:
                raise PermissionDenied
        except:
            raise Http404
        return obj

    def is_order_valid_for_replacement(self, curr_order, order_ids, replacement_amount):
        msg = None
        for order_id in order_ids:
            order_id = order_id.upper()
            if 'CP' in order_id:
                order = Order.objects.filter(number=order_id).first()
            else:
                if order_id.isdigit():
                    order = Order.objects.filter(id=order_id).first()
                else:
                    msg = (False, 'Please Enter correct Order id')
                    break
            if not order:
                msg = (False, 'Order {} Does Not Exist'.format(order_id))
                break

            if OrderItem.objects.filter(Q(replacement_order_id=order.id) | Q(replacement_order_id=order.number)).first():
                msg = (False, 'Order {} Already used as replacement for another order'.format(order_id))
                break

            if curr_order.id == order.id:
                msg = (False, 'Replacing Order {} cannot be same as current order.'.format(order_id))
                break

            if order.ordertxns.exists() and order.ordertxns.first().payment_mode !=1:
                msg = (False, "Replacing Order {} is Not Paid by Cash".format(order_id))
                break
        if msg:
            return msg
        order_ids = set([o.replace('CP', '') for o in order_ids])
        new_order_price = sum(list(Order.objects.filter(id__in=order_ids).values_list('total_incl_tax', flat=True)))
        current_order_price = replacement_amount
        difference = abs(current_order_price - new_order_price)
        percentage_difference = (difference * 100) / current_order_price
        if percentage_difference > 10:
            return (False, 'New Order Differ by more than 10 percent from previous order')

        return (True, 'Valid Order')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(WelcomeCallUpdateView, self).get(request, *args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object
        message = request.POST.get('message', '').strip()
        follow = request.POST.get('follow', '').strip()
        if not follow:
            follow = None
        valid = True
        error = ''
        data = request.POST
        cat_dict = dict(WC_CATEGORY)
        sub_cat1_dict = dict(WC_SUB_CATEGORY1)
        sub_cat2_dict = dict(WC_SUB_CATEGORY2)
        sub_cat3_dict = dict(WC_SUB_CATEGORY3)
        wc_sub_cat2_dict = dict(WC_SUB_CAT2)
        replace_order_ids = []
        replacement_amount = 0
        order_items = InvoiceGenerate().get_order_item_list(
            order=self.object)
        wc_items = self.get_welcome_list(
            order_items=order_items)

        try:
            cat = int(request.POST.get('cat'))
            enddt = timezone.now()
            startdt = enddt - datetime.timedelta(hours=24)
            ops = order.welcomecalloperation_set.filter(wc_cat=cat, created__range=(startdt,enddt))
            if cat == 23 and len(ops) == 0:
                mail_type = "WELCOME_CALL_BACK"
                email_dict = {
                    "first_name": order.first_name,
                    "mobile": order.mobile,
                 }
                SendSMS().send(sms_type=mail_type, data=email_dict)
        except:
            valid = False
            error = 'Enter valid category'
        try:
            subcat = int(request.POST.get('subcat'))
        except:
            valid = False
            error = 'Enter valid sub-category'

        if valid and not message and cat != 21:
            valid = False
            error = 'message is required'
        elif valid and not cat:
            valid = False
            error = 'Category is required'
        elif valid and not subcat:
            valid = False
            error = 'Sub Category is required'
        elif valid and cat == 23 and not follow:
            valid = False
            error = 'Follow up datetime is required'

        if valid and cat == 23 and follow:
            try:
                follow = datetime.datetime.strptime(follow, "%Y-%m-%d %H:%M:%S")
            except:
                valid = False
                error = 'Enter Valid Follow-up datetime'

        if valid:
            if cat == 21 and subcat in list(sub_cat1_dict.keys()):
                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)
                    try:
                        oi_category = int(data.get(name))
                    except:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break
                    if oi_category in list(sub_cat1_dict.keys()):
                        pass
                    else:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break
            elif cat == 22 and subcat in list(wc_sub_cat2_dict.keys()):
                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)
                    try:
                        oi_category = int(data.get(name))
                    except:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break
                    if oi_category in list(sub_cat2_dict.keys()):
                        pass
                    else:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break

                    if oi_category == 65 and oi.wc_sub_cat != 65:
                        replace_order_id = 'replacement_order_id' + str(oi.pk)
                        replace_order_id = request.POST.get(replace_order_id, None)
                        if not replace_order_id:
                            valid = False
                            error = 'Please Provide Replace Order Id'
                            break
                        replacement_amount += oi.selling_price
                        replace_order_ids.append(replace_order_id.strip())
                if valid and replace_order_ids:
                    valid, error = self.is_order_valid_for_replacement(order, replace_order_ids, replacement_amount)
            elif cat == 23 and subcat in list(sub_cat3_dict.keys()):
                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)
                    try:
                        oi_category = int(data.get(name))
                    except:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break
                    if oi_category in list(sub_cat3_dict.keys()):
                        pass
                    else:
                        valid = False
                        error = 'Enter valid item level sub-category'
                        break
            else:
                valid = False
                error = 'Enter valid category and sub-category'

        if valid:
            if cat == 21:
                order.wc_cat = cat
                order.wc_sub_cat = subcat
                order.wc_status = subcat
                order.welcome_call_done = True
                order.save()
                order.welcomecalloperation_set.create(
                    wc_cat=order.wc_cat,
                    wc_sub_cat=order.wc_sub_cat,
                    message=message,
                    wc_status=order.wc_status,
                    assigned_to=order.assigned_to,
                    created_by=request.user
                )

                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)

                    oi_category = int(data.get(name))
                    oi.wc_cat = cat
                    oi.wc_sub_cat = oi_category
                    oi.wc_status = oi_category
                    oi.save()
            elif cat == 22:
                order.wc_cat = cat
                order.wc_sub_cat = subcat
                order.wc_status = subcat
                order.save()
                order.welcomecalloperation_set.create(
                    wc_cat=order.wc_cat,
                    wc_sub_cat=order.wc_sub_cat,
                    wc_status=order.wc_status,
                    message=message,
                    assigned_to=order.assigned_to,
                    created_by=request.user
                )
                ct = 0
                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)

                    oi_category = int(data.get(name))
                    oi.wc_cat = cat
                    oi.wc_sub_cat = oi_category
                    oi.wc_status = oi_category
                    oi.save()
                    if oi_category in [63, 64, 65]:
                        ct += 1
                        for oi_cmb in oi_data.get('combos', []):
                            oi_cmb.wc_cat = cat
                            oi_cmb.wc_sub_cat = oi_category
                            oi_cmb.wc_status = oi_category
                            oi_cmb.save()
                            if oi_cmb.wc_sub_cat == 65:
                                replace_order_id = 'replacement_order_id' + str(oi.pk)
                                replace_order_id = request.POST.get(replace_order_id, None)
                                oi_cmb.replacement_order_id = replace_order_id.strip()
                                oi_cmb.oi_status = 164
                                oi_cmb.save()
                                oi_cmb.orderitemoperation_set.create(
                                    oi_status=oi_cmb.oi_status,
                                    last_oi_status=oi_cmb.last_oi_status,
                                    assigned_to=oi_cmb.assigned_to,
                                    added_by=request.user)
                        if oi_category == 65:
                            replace_order_id = 'replacement_order_id' + str(oi.pk)
                            replace_order_id = request.POST.get(replace_order_id, None)
                            oi.replacement_order_id = replace_order_id.strip()
                            oi.oi_status = 164
                            oi.save()
                            oi.orderitemoperation_set.create(
                                oi_status=oi.oi_status,
                                last_oi_status=oi.last_oi_status,
                                assigned_to=oi.assigned_to,
                                added_by=request.user)

                if ct == len(wc_items):
                    order.welcome_call_done = True
                    order.save()

            elif cat == 23:
                order.wc_cat = cat
                order.wc_sub_cat = subcat
                order.wc_status = subcat
                order.wc_follow_up = follow
                order.save()
                order.welcomecalloperation_set.create(
                    wc_cat=order.wc_cat,
                    wc_sub_cat=order.wc_sub_cat,
                    message=message,
                    wc_status=order.wc_status,
                    assigned_to=order.assigned_to,
                    created_by=request.user
                )
                for oi_data in wc_items:
                    oi = oi_data.get('oi')
                    name = 'subcategory' + str(oi.pk)
                    oi_category = int(data.get(name))
                    oi.wc_cat = cat
                    oi.wc_sub_cat = oi_category
                    oi.wc_status = oi_category
                    oi.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Welcome call order - %s updated successfully.' % (order.id))

            return HttpResponseRedirect(
                reverse('console:welcomecall:assigned'))
        else:
            messages.add_message(
                request, messages.ERROR,
                error)
            return HttpResponseRedirect(
                reverse(
                    'console:welcomecall:update',
                    kwargs={'pk': order.pk}))

    def get_context_data(self, **kwargs):
        context = super(WelcomeCallUpdateView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = self.get_object()
        order_items = InvoiceGenerate().get_order_item_list(
            order=order)
        wc_items = self.get_welcome_list(
            order_items=order_items)

        cat_dict = dict(WC_CATEGORY)
        sub_cat1_dict = dict(WC_SUB_CATEGORY1)
        sub_cat2_dict = dict(WC_SUB_CATEGORY2)
        sub_cat3_dict = dict(WC_SUB_CATEGORY3)
        wc_sub_cat2_dict = dict(WC_SUB_CAT2)

        context.update({
            "order": order,
            "orderitems": wc_items,
            "messages": alert,
            "cat_dict": cat_dict,
            "sub_cat1_dict": sub_cat1_dict,
            "sub_cat2_dict": sub_cat2_dict,
            "sub_cat3_dict": sub_cat3_dict,
            "wc_sub_cat2_dict": wc_sub_cat2_dict,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.WELCOMECALL_GROUP_LIST + settings.OPS_HEAD_GROUP_LIST]))
class WelcomeCallHistoryView(DetailView, WelcomeCallInfo):
    model = Order
    template_name = "console/welcomecall/history.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(
                pk=pk)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(WelcomeCallHistoryView, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(WelcomeCallHistoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = self.get_object()

        order_items = InvoiceGenerate().get_order_item_list(
            order=order)
        wc_items = self.get_welcome_list(
            order_items=order_items)
        ops = order.welcomecalloperation_set.all()
        ops = ops.order_by('-created')
        context.update({
            "order": order,
            "orderitems": wc_items,
            "messages": alert,
            "ops": ops,
        })
        return context


class ShowNumberField(View):
    template_name = "admin/shownumber.html"

    def get(self, request, *args, **kwargs):
        has_permission = request.user.user_permissions.filter(codename='can_change_exotel_status')
        shownum = cache.get('exoitel_status', '')
        if not has_permission:
            raise PermissionDenied()
        shownum = 'checked' if shownum else ""
        return render(request, self.template_name, {'check': shownum})

    def post(self,request,*args,**kwargs):
        value = self.request.POST.get('switch', '')
        value = True if value == 'on' else False
        shownum = 'checked' if value else ""
        cache.set('exoitel_status', value,timeout=None)
        return render(request, self.template_name, {'check': shownum})

