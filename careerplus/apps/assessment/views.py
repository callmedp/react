import requests
import logging
import json

from django.conf import settings
from django.views.generic import (DetailView,ListView,TemplateView)
from django.shortcuts import redirect,reverse,render
from django.core.cache import cache

#local imports

from .models import Question, Test

from shop.models import Category




class VskillTestView(DetailView):
    template_name = 'vskill/vskill_test.html'
    model =Test


    def get(self, request, *args, **kwargs):
        test = self.get_object()
        if not test:
            return redirect(reverse('assessment:vskill-landing'))
        return super(VskillTestView,self).get(request, args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(VskillTestView, self).get_context_data(**kwargs)
        test_id = self.get_object()
        questions_list = Question.objects.filter(test_id=test_id.pk)
        if not questions_list:
            return context

        test_list = self.request.session.get('vskill_appeared') if\
            self.request.session.get('vskill_appeared') else []
        test_list.append(test_id)
        self.request.session.update({'vskill_appeared': test_list})
        lead_created = self.request.session.get('is_lead_created')
        context.update({'questions_list': questions_list,'lead_created':lead_created})
        return context


class AssessmentLandingPage(TemplateView):
    template_name = 'vskill/vskill_landing.html'


    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": None, "name": 'practice-test'})
        return breadcrumbs

    def get_func_area_ids(self):
        if cache.get('TestCategory'):
            pass
        category_ids = list(set(Test.objects.filter(category__categoryproducts__type_flow=16,category__active=True)\
            .values_list('category__id', flat=True)))
        return category_ids

    def get_test(self):
        test = Test.objects.filter(is_active=True)[:4]
        return test

    def get_context_data(self, **kwargs):

        context = super(AssessmentLandingPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        category_ids = self.get_func_area_ids()
        if category_ids:
            category_ids = Category.objects.filter(id__in=category_ids, from_category__active=True,
                                          from_category__is_main_parent=True).values_list\
                ('from_category__related_to__id', flat=True)
        if category_ids:
            category_ids = Category.objects.filter(id__in=category_ids)
        context.update({'func_area': category_ids})
        context.update({'test_list': self.get_test()})
        return context


class AssessmentCategoryPage(DetailView):
    template_name = 'vskill/sales-marketing-test.html'
    model = Category
    slug_url_kwarg = 'slug'
    context_object_name = 'Category'

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": '/practice-tests/', "name": 'practice-test'})
        breadcrumbs.append({"url": '', "name": self.object.name})
        return breadcrumbs


    def get_context_data(self, **kwargs):
        context = super(AssessmentCategoryPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        category = self.object.get_childrens()
        cat_ids = Test.objects.exclude(category=None).values_list('category__id', flat=True)
        category = category.filter(id__in=cat_ids)
        context.update({'category': category})
        return context


class AssessmentSubCategoryPage(DetailView):
    template_name = 'vskill/brand-manager-test.html'
    model = Category
    slug_url_kwarg = 'slug'
    context_object_name = 'Category'


    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": '/practice-tests/', "name": 'practice-test'})
        parent = self.object.get_parent() if self.object.type_level == 3 else None
        if parent:
            breadcrumbs.append({
                "url": '/practice-tests/'+parent[0].slug + '/', "name": parent[0].name,
            })

        breadcrumbs.append({"url": '', "name": self.object.name})
        return breadcrumbs

    def get_free_test(self):
        category = self.object
        all_test = category.test_set.all()
        return all_test


    def get_context_data(self, **kwargs):
        context = super(AssessmentSubCategoryPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        all_test = self.get_free_test()
        context.update({'all_test': all_test})
        return context












