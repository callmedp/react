from collections import OrderedDict

from django.views.generic import (
    FormView, TemplateView, ListView, DetailView, CreateView)
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponse,)
from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse
from .decorators import Decorate, check_permission
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator

from linkedin.models import Draft, Organization, Education
from quizs.models import QuizResponse
from .linkedin_form import (
    DraftForm, LinkedinInboxActionForm, OrganizationForm,
    EducationForm, OrganizationInlineFormSet, EducationInlineFormSet)
from blog.mixins import PaginationMixin
from order.models import OrderItem
from emailers.email import SendMail
from django.conf import settings


class LinkedinQueueView(ListView, PaginationMixin):
    context_object_name = 'orderitem_list'
    template_name = 'console/linkedin/linkedin_inbox_list.html'
    model = OrderItem

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(LinkedinQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['orderitem_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "action_form": LinkedinInboxActionForm(),
            "messages": alert,
        })
        return context

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
                        # mail to user about writer information
                        order_id = orderitem_objs.first()
                        email_to = request.session.get('email', '')
                        mail_type = '2'
                        data = {
                            'orderitem': order_id.id,
                            'cc': writer.email,
                            'candidateid': request.session.get('candidate_id', '') 
                        }
                        SendMail().send([email_to], mail_type, data)
                    messages.add_message(request, messages.SUCCESS, str(len(orderitem_objs)) + ' orderitems are Assigned')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, str(e))
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('console:linkedin-queue'))

    def get_queryset(self):
        queryset = super(LinkedinQueueView, self).get_queryset()
        queryset = queryset.filter(product__type_flow=8, assigned_to=None)
        return queryset


class DraftListing(ListView, PaginationMixin):
    model = Draft
    context_object_name = 'draft_list'
    template_name = 'console/linkedin/draft_list.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(DraftListing, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(DraftListing, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(DraftListing, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DraftListing, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['draft_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@method_decorator(login_required(login_url='/console/login/'), name='dispatch')
class LinkedinOrderDetailVeiw(DetailView):
    model = OrderItem
    template_name = "console/linkedin/linkedin-order-detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(LinkedinOrderDetailVeiw, self).get(request, *args, **kwargs)
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
        context = super(LinkedinOrderDetailVeiw, self).get_context_data(**kwargs)
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
            # "draft_form": FileUploadForm(),
            "messages": alert,
            # "message_form": MessageForm(),
            "communications": communications,
            "operations": operations,
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
            messages.success(self.request, "Draft updated Successfully")
            return HttpResponseRedirect(reverse('console:change-draft', kwargs={'pk': self.get_object().pk}))

        self.object = self.get_object()
        context = super(ChangeDraftView, self).get_context_data(**kwargs)
        context['form'] = draft_form
        context['org_formset'] = org_formset
        context['edu_formset'] = edu_formset
        messages.success(self.request, "Draft is not updated successfully")
        return render(request, self.template_name, context)
