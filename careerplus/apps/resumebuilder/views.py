from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView

from .mixins import SessionManagerMixin


class WriteResumeView(TemplateView):
    template_name = 'frontend/index.html'

