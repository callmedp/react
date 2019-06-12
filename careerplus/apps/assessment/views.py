import requests
import logging
import json

from django.conf import settings
from django.views.generic import (DetailView,ListView,TemplateView)
from django.shortcuts import redirect,reverse,render

#local imports

from .models import Question, Test
from shop.models import Category
from blog.mixins import PaginationMixin,LoadCommentMixin
from django.core.paginator import Paginator



class VskillTestView(DetailView):
    template_name = 'vskill/vskill_test.html'
    model =Test

    def get(self, request, *args, **kwargs):

        test_id = self.request.GET.get('test', '')
        if not test_id:
            return redirect(reverse('assessment:vskill-landing'))
        return super(VskillTestView,self).get(request, args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(VskillTestView, self).get_context_data(**kwargs)
        test_id = self.get_object()
        questions_list = Question.objects.filter(test_id=test_id.pk)
        if not questions_list:
            return redirect(reverse('assessment:vskill-landing'))

        test_list = self.request.session.get('vskill_appeared') if\
            self.request.session.get('vskill_appeared') else []
        test_list.append(test_id)
        self.request.session.update({'vskill_appeared': test_list})
        lead_created = self.request.session.get('is_lead_created')
        context.update({'questions_list': questions_list,'lead_created':lead_created})
        return context




class AssessmentLandingPage(TemplateView):
    template_name = 'vskill/vskill_landing.html'

    def __init__(self):
        self.page = 1
        self.paginated_by = 8

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": None, "name": 'practice-test'})
        # data = {"breadcrumbs": breadcrumbs}
        return breadcrumbs

    def get_func_areas(self,filter_dict):
        category = Category.objects.filter(**filter_dict)[:8]
        return category

    def get_test(self):
        test = Test.objects.filter(is_active=True)[:4]
        return test


    def get_context_data(self, **kwargs):
        filter_dict = {'active': 'True', 'type_level':2 }
        context = super(AssessmentLandingPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        context.update({'func_area': self.get_func_areas(filter_dict)})
        context.update({'test_list': self.get_test()})
        return context


class AssessmentCategoryPage(DetailView):
    template_name = 'vskill/vskill_category.html'
    model = Category
    slug_url_kwarg = 'slug'

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": None, "name": 'practice-test'})
        parent = self.object.get_parent() if self.object.type_level == 3 else None
        if parent:
            breadcrumbs.append({
                "url": parent[0].get_absolute_url(), "name": parent[0].name,
            })
        breadcrumbs.append({"url": '', "name": self.object.name})
        return breadcrumbs


    def get_context_data(self, **kwargs):
        context = super(AssessmentCategoryPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        category = self.object.get_childrens()[:4]
        context.update({'category':category})
        return context















