from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView

from .mixins import SessionManagerMixin


class WriteResumeView(SessionManagerMixin, TemplateView):
    template_name = 'frontend/index.html'
