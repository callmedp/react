from collections import OrderedDict

from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from .decorators import Decorate, check_permission
from django.core.paginator import Paginator
from django.db.models import Q

from linkedin.models import Draft, Organization, Education, QuizResponse
from .linkedin_form import DraftForm


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
        


class LinkedinQueueView(TemplateView):
    template_name = 'console/linkedin/linkedin_queue.html'
    
    def get(self, request, *args, **kwargs):
        return super(LinkedinQueueView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinQueueView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        quiz_obj = QuizResponse.objects.all()
        context.update({
            'messages': alert,
            'quiz_obj': quiz_obj
        })
        return context


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
