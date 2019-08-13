import requests
import logging
import json
from datetime import datetime,timedelta

from django.conf import settings
from django.views.generic import (DetailView,ListView,TemplateView)
from django.shortcuts import redirect,reverse,render
from django.http import HttpResponseRedirect

from django.core.cache import cache

#local imports

from .models import Question, Test
from .utils import TestCacheUtil
from shop.models import Category


class VskillTestView(DetailView):
    template_name = 'vskill/test-paper.html'
    model = Test

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": '/practice-tests', "name": 'practice-test'})
        test = self.get_object()
        category = test.category
        parent_category = category.get_parent().first() if category.get_parent() else None
        if parent_category:
            breadcrumbs.append({"url": '/practice-tests/' + parent_category.slug, "name": parent_category.name})
        breadcrumbs.append({"url": '/practice-tests/' + category.slug +'/sub', "name": category.name})
        breadcrumbs.append({"url": None, "name": 'test'})
        return breadcrumbs

    def dispatch(self,request,*args,**kwargs):
        if not request.session.session_key:
            request.session.cycle_key()
        
        self.cache_test = TestCacheUtil(request=request)
        response = super(VskillTestView, self).dispatch(request, args, **kwargs)
        original_context = response.context_data
        test_object = original_context['object']
        show_test, delete_ans = self.cache_test.show_test_remove_local_storage(\
            key='test-' + str(test_object.id))
        if not show_test:
            return redirect(reverse('assessment:vskill-result', kwargs={'slug': test_object.slug}))
        
        response.context_data = original_context
        return response

    def get_context_data(self, **kwargs):
        context = super(VskillTestView, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs()})
        test_object = context['object']
        show_test, delete_ans = self.cache_test.show_test_remove_local_storage\
            (key='test-'+str(test_object.id))
        if not show_test:
            context.update({'show_test': show_test})
        context.update({'delete_ans': delete_ans})
        questions_list = Question.objects.filter(test_id=test_object.pk)
        if not questions_list:
            return context
        test_list = self.request.session.get('vskill_appeared') if\
            self.request.session.get('vskill_appeared') else []
        test_list.append(test_object)
        self.request.session.update({'vskill_appeared': test_list})
        lead_created = self.request.session.get('is_lead_created')
        context.update({'questions_list': questions_list,'lead_created': lead_created})
        return context


class AssessmentLandingPage(TemplateView):
    template_name = 'vskill/vskill_landing.html'

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": None, "name": 'practice-tests'})
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
                "url": '/practice-tests/'+parent[0].slug, "name": parent[0].name,
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


class AssessmentResultPage(TemplateView):
    template_name = 'vskill/test-answers.html'

    def get_redirection_path(self):
        test_slug = self.kwargs.get('slug')
        test_object = Test.objects.filter(slug=test_slug).first()
        session_id = self.request.session.session_key
        key = session_id + 'test-' + str(test_object.id)
        category = getattr(Test.objects.filter(slug=test_slug).first(), 'category', None)
        if not cache.get(key) and category:
            return reverse('assessment:vskill-subcategory',\
                kwargs={'slug': category.slug}) if category else reverse("'homepage'")
        elif cache.get(key).get('timeout') or cache.get(key).get('test_submit'):
            return
        else:
            return reverse('assessment:vskill-exam', \
             kwargs={'slug': test_slug}) if category else reverse("homepage")

    def get(self,request,*args,**kwargs):
        if not request.session.session_key:
            request.session.cycle_key()

        if self.get_redirection_path():
            return HttpResponseRedirect(self.get_redirection_path())
        return super(AssessmentResultPage, self).get(request, *args, **kwargs)

    def get_breadcrumbs(self,test):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": '/practice-tests/', "name": 'practice-test'})
        if test.category.get_parent():
            breadcrumbs.append({"url": '/practice-tests/'+test.category.get_parent()[0].slug, "name": test.category.get_parent()[0].name})
        if test.category:
            breadcrumbs.append({"url": '/practice-tests/'+test.category.slug +'/sub', "name": test.category.name})
        breadcrumbs.append({"url": '', "name": test.slug + '-test'})
        return breadcrumbs

    def get_context_data(self, **kwargs):
        session_id = self.request.session.session_key
        slug = kwargs.get('slug')
        test = Test.objects.filter(slug=slug).first()
        context = super(AssessmentResultPage, self).get_context_data(**kwargs)
        context.update({'breadcrumbs': self.get_breadcrumbs(test)})
        questions_list = Question.objects.filter(test_id=test.pk)
        context.update({'questions_list': questions_list})
        context.update({'object': test})
        return context



