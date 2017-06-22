from collections import OrderedDict

from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from .decorators import Decorate, check_permission
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from linkedin.models import Draft, Organization, Education, QuizResponse
from .linkedin_form import DraftForm, LinkedinInboxActionForm
from blog.mixins import PaginationMixin
from order.models import OrderItem
from emailers.email import SendMail


class LinkedinProfileView(FormView):
    template_name = 'console/linkedin/save-draft.html'
    model = Draft
    form_class = DraftForm

    def get(self, request, *args, **kwargs):
        return super(LinkedinProfileView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinProfileView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        form = self.get_form()
        context.update({
            'messages': alert,
            'form': form
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(request, commit=True)
            messages.add_message(request, messages.SUCCESS, 'Draft Saved')
            return HttpResponseRedirect(reverse('draft-listing'))
        form = self.get_form()
        return render(request, self.template_name, {'form': form})
        


class LinkedinQueueView(ListView, PaginationMixin):
    context_object_name = 'orderitem_list'
    template_name = 'console/linkedin/linkedin_queue.html'
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


class DraftListing(ListView):
    model = Draft
    template_name = 'console/linkedin/draft_list.html'

    def get(self, request, *args, **kwargs):
        return super(DraftListing, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DraftListing, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert,
        })
        return context
