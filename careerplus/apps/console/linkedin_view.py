import json
import logging
import datetime

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    FormView, TemplateView, ListView, DetailView, CreateView, View)
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponse,)
from weasyprint import HTML
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from linkedin.models import Draft, Organization, Education
from geolocation.models import Country
from quizs.models import QuizResponse
from shop.models import DeliveryService
from emailers.tasks import send_email_task

from .linkedin_form import (
    DraftForm,
    LinkedinInboxActionForm,
    OrganizationForm,
    EducationForm,
    OrganizationInlineFormSet,
    EducationInlineFormSet,
    LinkedinOIFilterForm,
    AssignmentInterNationalForm)

from .order_form import MessageForm, OIActionForm
from blog.mixins import PaginationMixin
from order.models import OrderItem, Order, InternationalProfileCredential

from emailers.sms import SendSMS
from django.conf import settings


class LinkedinQueueView(ListView, PaginationMixin):
    context_object_name = 'orderitem_list'
    template_name = 'console/linkedin/linkedin_inbox_list.html'
    model = OrderItem

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.writer, self.created = '', ''
        self.draft_level = -1
        self.delivery_type = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.writer = request.GET.get('writer', '')
        self.modified = request.GET.get('modified', '')
        self.delivery_type = request.GET.get('delivery_type', '')
        try:
            self.draft_level = int(request.GET.get('draft_level', -1))
        except:
            self.draft_level = -1
        return super(LinkedinQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['orderitem_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "modified": self.modified, "writer": self.writer,
            "draft_level": self.draft_level,
            "delivery_type": self.delivery_type}
        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "action_form": LinkedinInboxActionForm(),
            "messages": alert,
            'filter_form': filter_form,
            "message_form": MessageForm(),
            "query": self.query,
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                data = {"display_message": ''}
                orderitem_list = request.POST.getlist('selected_id[]', [])
                writer_pk = int(request.POST.get('action_type', '0'))
                orderitem_objs = OrderItem.objects.filter(id__in=orderitem_list)
                if writer_pk == 0:
                    messages.add_message(request, messages.ERROR, 'Please select valid action first')
                else:
                    User = get_user_model()
                    try:
                        writer = User.objects.get(pk=writer_pk)
                        for obj in orderitem_objs:
                            email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                            obj.assigned_to = writer
                            obj.assigned_by = request.user
                            obj.save()

                            # mail to user about writer information
                            to_emails = [obj.order.email]
                            mail_type = 'ALLOCATED_TO_WRITER'
                            data = {}
                            data.update({
                                "username": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                                "writer_name": writer.name,
                                "writer_email": writer.email,
                                "subject": "Your developed document has been shared with our expert",
                            })

                            if 101 not in email_sets:
                                send_email_task.delay(to_emails, mail_type, data, status=101, oi=obj.pk)
                            if obj.delivery_service:
                                if obj.delivery_service.slug == 'super-express':
                                    try:
                                        SendSMS().send(sms_type=mail_type, data=data)
                                    except Exception as e:
                                        logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                            obj.orderitemoperation_set.create(
                                oi_status=1,
                                last_oi_status=obj.oi_status,
                                assigned_to=obj.assigned_to,
                                added_by=request.user,
                            )
                        data['display_message'] = str(len(orderitem_objs)) + ' orderitems are Assigned.'
                    except Exception as e:
                        data['display_message'] = str(e)
            except Exception as e:
                data['display_message'] = str(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()

    def get_queryset(self):
        queryset = super(LinkedinQueueView, self).get_queryset()
        queryset = queryset.filter(order__status=1, no_process=False, product__type_flow=8).exclude(oi_status__in=[4,45,46,47,48, 161, 162, 163])
        user = self.request.user
        if user.is_superuser:
            pass
        elif user.has_perm('order.writer_inbox_assigner'):
            queryset = queryset.filter(assigned_to=None)
        elif user.has_perm('order.writer_inbox_assignee'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
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
        except:
            pass

        try:
            if self.writer:
                queryset = queryset.filter(assigned_to=self.writer)
        except:
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(draft_counter=self.draft_level)
        except:
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
        except:
            pass

        return queryset.select_related('order', 'product', 'delivery_service').order_by('-modified')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LinkedinQueueView, self).dispatch(request, *args, **kwargs)


class LinkedinOrderDetailVeiw(DetailView):
    model = Order
    template_name = "console/order/order-detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(LinkedinOrderDetailVeiw, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(LinkedinOrderDetailVeiw, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        obj = self.get_object()
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        order = self.get_object()
        order_items = order.orderitems.all().select_related('product', 'partner')
        context.update({
            "order": order,
            'orderitems': list(order_items),
            "max_limit_draft": max_limit_draft,
            "messages": alert,
            "message_form": MessageForm(),
        })
        return context


class ChangeDraftView(DetailView):
    template_name = 'console/linkedin/change_draft.html'
    model = Draft

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeDraftView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeDraftView, self).get_object(queryset)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            ord_obj = OrderItem.objects.get(oio_linkedin=self.object)
            q_resp = QuizResponse.objects.get(oi=ord_obj)
            if not q_resp.submitted:
                messages.error(self.request, "First Submit Councelling Form")
                return HttpResponseRedirect(reverse('console:linkedin-inbox')) 

        except Exception as e:
            pass
        return super(ChangeDraftView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChangeDraftView, self).get_context_data(**kwargs)

        OrganizationFormset = inlineformset_factory(
            Draft, Organization,
            form=OrganizationForm, formset=OrganizationInlineFormSet,
            can_delete=True, extra=0, max_num=10)

        EducationFormset = inlineformset_factory(
            Draft, Education,
            form=EducationForm, formset=EducationInlineFormSet,
            can_delete=True, extra=0, max_num=10)

        org_formset = OrganizationFormset(instance=self.get_object())
        edu_formset = EducationFormset(instance=self.get_object())
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert,
            'org_formset': org_formset,
            'edu_formset': edu_formset,
            'form': DraftForm(instance=self.get_object()),
        })
        return context

    def post(self, request, *args, **kwargs):
        try:
            draft_obj = Draft.objects.get(pk=kwargs.get('pk'))
            ord_obj = OrderItem.objects.get(oio_linkedin=draft_obj)
            if ord_obj:
                OrganizationFormset = inlineformset_factory(
                    Draft, Organization,
                    form=OrganizationForm, formset=OrganizationInlineFormSet,
                    can_delete=True, extra=1)

                EducationFormset = inlineformset_factory(
                    Draft, Education,
                    form=EducationForm, formset=OrganizationInlineFormSet,
                    can_delete=True, extra=1)

                org_formset = OrganizationFormset(request.POST, instance=self.get_object())
                edu_formset = EducationFormset(request.POST, instance=self.get_object())
                draft_form = DraftForm(request.POST, instance=self.get_object())
                if draft_form.is_valid() and org_formset.is_valid() and edu_formset.is_valid():
                    draft_obj = draft_form.save()
                    for form in org_formset.forms:
                        org_obj = form.save(commit=False)
                        org_obj.draft = draft_obj
                        org_obj.save()

                    for form in org_formset.deleted_forms:
                        form.instance.delete()

                    for form in edu_formset.forms:
                        edu_obj = form.save(commit=False)
                        edu_obj.draft = draft_obj
                        edu_obj.save()

                    for form in edu_formset.deleted_forms:
                        form.instance.delete()
                    # for update oi status
                    last_status = ord_obj.oi_status  
                    ord_obj.oi_status = 45  # pending Approval
                    ord_obj.last_oi_status = last_status
                    ord_obj.draft_added_on = timezone.now()
                    ord_obj.save()
                    ord_obj.orderitemoperation_set.create(
                        linkedin = draft_obj,
                        draft_counter=ord_obj.draft_counter + 1,
                        oi_status=44,
                        last_oi_status=last_status,
                        assigned_to=ord_obj.assigned_to,
                        added_by=request.user)
                    ord_obj.orderitemoperation_set.create(
                        oi_status=ord_obj.oi_status,
                        last_oi_status=44,
                        assigned_to=ord_obj.assigned_to,
                        added_by=request.user)

                    messages.success(self.request, "Draft Saved Successfully")
                    return HttpResponseRedirect(reverse('console:linkedin-inbox'))

                self.object = self.get_object()
                context = super(ChangeDraftView, self).get_context_data(**kwargs)
                context['form'] = draft_form
                context['org_formset'] = org_formset
                context['edu_formset'] = edu_formset
                messages.success(self.request, "Draft is not Saved successfully", 'error')
                return render(request, self.template_name, context)

            else:
                messages.success(self.request, "Draft not exist with this order" 'error')
                return render(request, self.template_name, context)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return render(request, self.template_name, context)


class LinkedinRejectedByAdminView(ListView, PaginationMixin):
    context_object_name = 'rejectedbylinkedinadmin_list'
    template_name = 'console/linkedin/rejectedbylinkedinadmin-list.html'
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
        self.delivery_type = request.GET.get('delivery_type', -1)
        return super(LinkedinRejectedByAdminView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinRejectedByAdminView, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbylinkedinadmin_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(LinkedinRejectedByAdminView, self).get_queryset()
        queryset = queryset.filter(order__status=1, no_process=False, oi_status=47, product__type_flow=8)
        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
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
        except:
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except:
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except:
            pass

        try:
            if self.delivery_typ:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.slug == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except:
            pass
        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to').order_by('-modified')


class LinkedinRejectedByCandidateView(ListView, PaginationMixin):
    context_object_name = 'rejectedbylinkedincandidate_list'
    template_name = 'console/linkedin/reject-linkedin-candidate.html'
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
        return super(LinkedinRejectedByCandidateView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinRejectedByCandidateView, self).get_context_data(**kwargs)
        paginator = Paginator(context['rejectedbylinkedincandidate_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT
        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level, }
        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "query": self.query,
            "action_form": LinkedinInboxActionForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(LinkedinRejectedByCandidateView, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=48, product__type_flow__in=[8])

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
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
        except:
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except:
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except:
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.name == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except:
            pass

        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to').order_by('-modified')


class LinkedinApprovalVeiw(ListView, PaginationMixin):
    context_object_name = 'approval_list'
    template_name = 'console/linkedin/linkedin-approval-list.html'
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
        return super(LinkedinApprovalVeiw, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinApprovalVeiw, self).get_context_data(**kwargs)
        paginator = Paginator(context['approval_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        max_limit_draft = settings.DRAFT_MAX_LIMIT

        initial = {
            "modified": self.modified,
            "writer": self.writer,
            "delivery_type": self.delivery_type,
            "draft_level": self.draft_level,
        }

        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "messages": alert,
            "max_limit_draft": max_limit_draft,
            "filter_form": filter_form,
            "query": self.query,
            "action_form": OIActionForm(),
        })
        return context

    def get_queryset(self):
        queryset = super(LinkedinApprovalVeiw, self).get_queryset()
        queryset = queryset.filter(order__status=1, oi_status=45, product__type_flow__in=[8]).exclude(oi_status=9)
        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
        except:
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
        except:
            pass

        try:
            if self.writer:
                queryset = queryset.filter(
                    assigned_to=self.writer)
        except:
            pass

        try:
            if self.draft_level != -1:
                queryset = queryset.filter(
                    draft_counter=self.draft_level)
        except:
            pass

        try:
            if self.delivery_type:
                delivery_obj = DeliveryService.objects.get(pk=self.delivery_type)
                if delivery_obj.name == 'normal':
                    queryset = queryset.filter(
                        Q(delivery_service=self.delivery_type) |
                        Q(delivery_service__isnull=True))
                else:
                    queryset = queryset.filter(
                        delivery_service=self.delivery_type)
        except:
            pass

        return queryset.select_related('order', 'product', 'assigned_by', 'assigned_to').order_by('-modified')


class InterNationalUpdateQueueView(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/international-profile-update-list.html'
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
        return super(InterNationalUpdateQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InterNationalUpdateQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "modified": self.modified, }
        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "assignment_form": AssignmentInterNationalForm(),
            "messages": alert,
            "query": self.query,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name="internationalprofileupdate"),
        })

        return context

    def get_queryset(self):
        queryset = super(InterNationalUpdateQueueView, self).get_queryset()
        queryset = queryset.filter(order__status__in=[1, 3], product__type_flow=4, no_process=False, oi_status__in=[5, 25, 61])
        user = self.request.user
        q1 = queryset.filter(oi_status=61)
        exclude_list = []
        for oi in q1:
            closed_ois = oi.order.orderitems.filter(product__type_flow=12, oi_status=4, no_process=False)
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
        user = self.request.user
        if user.is_superuser or user.has_perm('order.international_profile_update_assigner'):
            pass
        elif user.has_perm('order.international_profile_update_assigner'):
            queryset = queryset.filter(assigned_to__isnull=True)
        elif user.has_perm('order.international_profile_update_assignee'):
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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
        except:
            pass

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')


class InterNationalApprovalQueue(ListView, PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/order/international-profile-approval-list.html'
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
        return super(InterNationalApprovalQueue, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InterNationalApprovalQueue, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial = {
            "payment_date": self.payment_date,
            "modified": self.modified, }
        filter_form = LinkedinOIFilterForm(initial)
        context.update({
            "messages": alert,
            "query": self.query,
            "message_form": MessageForm(),
            "filter_form": filter_form,
            "action_form": OIActionForm(queue_name="internationalapproval"),
        })

        return context

    def get_queryset(self):
        queryset = super(InterNationalApprovalQueue, self).get_queryset()
        queryset = queryset.filter(order__status=1, product__type_flow=4, oi_status=23, no_process=False)

        try:
            if self.query:
                queryset = queryset.filter(Q(id__icontains=self.query) |
                    Q(product__name__icontains=self.query) |
                    Q(order__number__icontains=self.query) |
                    Q(order__mobile__icontains=self.query) |
                    Q(order__email__icontains=self.query))
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
        except:
            pass

        return queryset.select_related('order', 'product', 'assigned_to', 'assigned_by').order_by('-modified')


class ProfileUpdationView(DetailView):
    model = OrderItem
    template_name = "console/order/updateprofile.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(ProfileUpdationView, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdationView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        profile_url_dict = {}
        country_obj = None
        profile_urls = None
        order = self.get_object()
        try:
            profile_obj = order.product.productextrainfo_set.get(info_type='profile_update')
            country_obj = Country.objects.get(pk=profile_obj.object_id)
            profile_urls = country_obj.profile_url.split(',')
            profile_info = InternationalProfileCredential.objects.filter(oi=order.pk)
            for profile in profile_info:
                profile_url_dict[profile.site_url] = profile
        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % (str(profile_url_dict), str(e)))

        context.update({
            "messages": alert,
            "order": order,
            "profile_urls": profile_urls,
            'country_obj': country_obj,
            "action_form": OIActionForm(queue_name="internationalprofileupdate"),
            "profile_url_dict": profile_url_dict,
        })
        return context

    def post(self, request, *args, **kwargs):
        try:
            action = int(request.POST.get('action', '0'))
        except:
            action = 0
        selected = request.POST.get('selected_id', '')
        queue_name = request.POST.get('queue_name', '')
        update_sub = request.POST.get('update', '')
        count = request.POST.get('count', None)
        username = request.POST.get('username' + str(count) + '', None)
        password = request.POST.get('password' + str(count) + '', None)
        site = request.POST.get('site' + str(count) + '', None)
        flag = request.POST.get('flag' + str(count) + '', None)

        if action == -9 and queue_name == "internationalprofileupdate":
            selected_id = json.loads(selected)
            try:
                orderitem = OrderItem.objects.select_related(
                    'order', 'product', 'partner').get(
                    id__in=selected_id)
                objs = orderitem.internationalprofilecredential_set.all()
                for obj in objs:
                    if not obj.username and not password:
                        msg = 'Please update all the profiles first'
                        messages.add_message(request, messages.SUCCESS, msg)
                        return HttpResponseRedirect(reverse(
                            'console:international_profile_update',
                            kwargs={'pk': kwargs.get('pk')}))
                approval = 0
                if orderitem:
                    last_oi_status = orderitem.oi_status
                    orderitem.oi_status = 23  # pending Approval
                    orderitem.last_oi_status = last_oi_status
                    orderitem.save()
                    approval += 1
                    orderitem.orderitemoperation_set.create(
                        oi_status=23,
                        last_oi_status=last_oi_status,
                        assigned_to=orderitem.assigned_to,
                        added_by=request.user)
                msg = str(approval) + ' orderitems send for approval.'
                messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse(
                'console:international_profile_update',
                kwargs={'pk': int(selected_id[0])}))

        elif update_sub == "1":
            try:
                orderitem = OrderItem.objects.select_related(
                    'order', 'product',
                    'partner').get(id=kwargs.get('pk'))
                if username and password and flag:
                    orderitem.internationalprofilecredential_set.update(
                        username=username,
                        password=password,
                        candidateid=orderitem.order.candidate_id,
                        site_url=site,
                        profile_status=True,
                    )
                    return HttpResponse(
                        json.dumps({'success': True}),
                        content_type="application/json"
                    )
                return HttpResponse(
                    json.dumps({'success': False}),
                    content_type="application/json"
                )
            except Exception as e:
                logging.getLogger('error_log').error("%s - %s" % (
                    str(update_sub), str(e)))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdationView, self).dispatch(
            request, *args, **kwargs)


class InterNationalAssignmentOrderItemView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_pk = int(request.POST.get('assign_to', '0'))
        except:
            user_pk = 0

        selected = request.POST.get('selected_id', '')
        selected_id = json.loads(selected)
        queue_name = request.POST.get('queue_name', '')

        if user_pk:
            try:
                User = get_user_model()
                assign_to = User.objects.get(pk=user_pk)
                orderitem_objs = OrderItem.objects.filter(id__in=selected_id)
                for obj in orderitem_objs:
                    obj.assigned_to = assign_to
                    obj.assigned_by = request.user
                    obj.save()
                    # mail to user about writer information
                    email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                    to_emails = [obj.order.email]

                    data = {}
                    data.update({
                        "username": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                        "writer_name": assign_to.name,
                        "subject": "Your developed document has been shared with our expert",
                        "writer_email": assign_to.email,
                    })
                    mail_type = 'ALLOCATED_TO_WRITER'
                    if 63 not in email_sets:
                        send_email_task.delay(to_emails, mail_type, data, status=63, oi=obj.pk)
                    if obj.delivery_service and (obj.delivery_service.slug == 'super-express'):
                        try:
                            SendSMS().send(sms_type=mail_type, data=data)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    obj.orderitemoperation_set.create(
                        oi_status=1,
                        last_oi_status=obj.oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user
                    )

                display_message = str(len(orderitem_objs)) + ' orderitems are Assigned.'
                messages.add_message(request, messages.SUCCESS, display_message)
                return HttpResponseRedirect(reverse('console:queue-' + queue_name))
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
                return HttpResponseRedirect(reverse('console:queue-' + queue_name))

        messages.add_message(request, messages.ERROR, "Please select valid assignment.")
        return HttpResponseRedirect(reverse('console:queue-' + queue_name))


class ProfileCredentialDownload(View):

    def get(self, request, *args, **kwargs):
        oi = kwargs.get('oi', '')
        try:
            profile_credentials = InternationalProfileCredential.objects.filter(oi=oi)
            try:
                context_dict = {
                    'pagesize': 'A4',
                    'profile_credentials': profile_credentials,
                }
                template = get_template('console/order/profile-update-credentials.html')
                context = Context(context_dict)
                html = template.render(context)
                pdf_file = HTML(string=html).write_pdf()
                http_response = HttpResponse(pdf_file, content_type='application/pdf')
                http_response['Content-Disposition'] = 'filename="profile_credential.pdf"'
                return http_response
            except:
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()
