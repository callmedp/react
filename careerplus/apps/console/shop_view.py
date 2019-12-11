import json, os
import logging
import csv
import bson
import mimetypes
from collections import OrderedDict
from datetime import datetime
from io import StringIO

from django.views.generic import (
    View, UpdateView, FormView,
    TemplateView, ListView, DetailView)

from django.http import (
    HttpResponseForbidden, HttpResponse,
    HttpResponseRedirect, HttpResponseBadRequest, Http404)
from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.forms.models import modelformset_factory
from dateutil.relativedelta import relativedelta
from django.shortcuts import render

from .decorators import (
    has_group,
    Decorate, check_permission,
    check_group, stop_browser_cache)
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings

from dal import autocomplete

from partner.models import Vendor, VendorHierarchy
from blog.mixins import PaginationMixin
from shop.models import (
    Category, Keyword,
    Attribute, AttributeOptionGroup,
    Product, Chapter, Skill, ProductAuditHistory, UniversityCoursePayment,
    SubHeaderCategory,SubCategory
)
from homepage.models import Testimonial
from .shop_form import (
    AddCategoryForm, ChangeCategoryForm,
    ChangeCategorySEOForm,
    CategoryRelationshipForm,
    RelationshipInlineFormSet,
    ChangeCategorySkillForm, SkillAddForm,
    SkillChangeForm,
    ProductSkillForm, SkillInlineFormSet,
    UniversityCourseForm,
    UniversityCoursePaymentForm,
    UniversityCoursesPaymentInlineFormset,
    SubHeaderCategoryForm, SubHeaderInlineFormSet,
    TestimonialModelForm,
    AddSubCategoryForm,ChangeSubCategoryForm
)

from scheduler.models import Scheduler
from console.schedule_tasks.tasks import generate_discount_report
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage

from shop.forms import (
    AddKeywordForm, AddAttributeOptionForm, AddAttributeForm,
    ChangeProductForm, ChangeProductSEOForm,
    ChangeProductOperationForm, ProductCategoryForm,
    CategoryInlineFormSet, ProductPriceForm,
    ProductCountryForm, ProductAttributeForm,
    FAQInlineFormSet, ProductFAQForm, ProductVariationForm,
    VariationInlineFormSet, ProductChildForm,
    ChildInlineFormSet, ProductRelatedForm,
    RelatedInlineFormSet, ChangeProductVariantForm,
    ChapterInlineFormSet, ProductChapterForm)

from shop.utils import CategoryValidation, ProductValidation
from faq.forms import (
    AddFaqForm,
    ChangeFaqForm,
    ChangePublicFaqForm,)
from shop.choices import SUB_FLOWS
from homepage.config import (
    UNIVERSITY_PAGE, UNIVERSITY_COURSE)

from faq.models import FAQuestion
from users.mixins import UserGroupMixin
from wsgiref.util import FileWrapper


class SkillAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Skill.objects.none()
        qs = Skill.objects.filter(active=True)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ProductAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Product.objects.none()
        qs = Product.objects.filter(is_indexed=True,active=True)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs



@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class SkillChangeView(UpdateView):
    model = Skill
    template_name = 'console/skill/change_skill.html'
    success_url = reverse_lazy('console:skill-list')
    http_method_names = [u'get', u'post']
    form_class = SkillChangeForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(SkillChangeView, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(SkillChangeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            try:
                form.save()
                valid_form = self.form_valid(form)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Skill %s - %s Updated Successfully.' % (
                        self.object.name, self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Blog %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class SkillChangeView(UpdateView):
    model = Skill
    template_name = 'console/skill/change_skill.html'
    success_url = reverse_lazy('console:skill-list')
    http_method_names = [u'get', u'post']
    form_class = SkillChangeForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(SkillChangeView, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(SkillChangeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            try:
                form.save()
                valid_form = self.form_valid(form)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Skill %s - %s Updated Successfully.' % (
                        self.object.name, self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR,
                                     'Blog %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class SkillAddView(FormView):
    form_class = SkillAddForm
    template_name = 'console/skill/add_skill.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:skill-list')

    def get(self, request, *args, **kwargs):
        return super(SkillAddView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SkillAddView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a Skill"
        )
        self.success_url = reverse_lazy('console:skill-list')
        return super(SkillAddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your addition has not been saved. Try again."
        )
        return super(SkillAddView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class SkillListView(ListView, PaginationMixin):
    model = Skill
    context_object_name = 'skill_list'
    template_name = 'console/skill/list_skill.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(SkillListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(SkillListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SkillListView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['skill_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context

    def get_queryset(self):
        queryset = super(SkillListView, self).get_queryset()

        if self.query:
            queryset = queryset.filter(Q(name__icontains=self.query))
        
        return queryset


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_add_category'))
class AddCategoryView(FormView):
    form_class = AddCategoryForm
    template_name = 'console/shop/add_category.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:category-add')

    def get(self, request, *args, **kwargs):
        return super(AddCategoryView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a catagory"
        )
        self.success_url = reverse_lazy('console:category-list')
        return super(AddCategoryView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your addition has not been saved. Try again."
        )
        return super(AddCategoryView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_category'))
class ChangeCategoryView(DetailView):
    template_name = 'console/shop/change_category.html'
    model = Category

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeCategoryView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeCategoryView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeCategoryView, self).get_context_data(**kwargs)
        CategoryRelationshipFormSet = inlineformset_factory(
            Category, Category.related_to.through, fk_name='related_from',
            form=CategoryRelationshipForm,
            can_delete=False,
            formset=RelationshipInlineFormSet, extra=1,
            max_num=20, validate_max=True)

        SubHeaderFormSet = inlineformset_factory(
            Category, SubHeaderCategory,
            fk_name='category',
            form=SubHeaderCategoryForm,
            can_delete=False,
            formset=SubHeaderInlineFormSet, extra=1,
            max_num=5, validate_max=True)

        TestimonialModelFormset = modelformset_factory(
            Testimonial, form=TestimonialModelForm,
            can_delete=True, extra=1, max_num=5,
            validate_max=True)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeCategoryForm(
            instance=self.get_object())
        seo_change_form = ChangeCategorySEOForm(
            instance=self.get_object())
        if self.object.type_level in [2, 3, 4]:
            skill_change_form = ChangeCategorySkillForm(
            instance=self.get_object())
            context.update({'skill_form': skill_change_form})

        if self.object.type_level in [2, 3, 4]:
            relationship_formset = CategoryRelationshipFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'relationship_formset': relationship_formset})

        if self.object.type_level in [3, 4]:
            sub_heading_formset = SubHeaderFormSet(instance=self.get_object())
            context.update({'sub_heading_formset': sub_heading_formset})

        if self.object.type_level in [3, 4]:
            testimonial_model_formset = TestimonialModelFormset(
                data=None,
                queryset=Testimonial.objects.filter(
                    page=UNIVERSITY_PAGE,
                    object_id=self.object.pk))
            context.update({'testimonial_model_formset': testimonial_model_formset})

        childrens = self.object.category_set.filter(
            from_category__related_to=self.object)
        products = self.object.check_products()
        context.update({
            'messages': alert,
            'form': main_change_form,
            'seo_form': seo_change_form,
            "childrens": childrens,
            "products": products})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                cat = int(request.POST.get('category'))
                if obj == cat:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if slug == 'main':
                        form = ChangeCategoryForm(
                            request.POST, request.FILES, instance=obj)
                        if form.is_valid():
                            form.save()
                            url = obj.get_full_url()
                            Category.objects.filter(pk=obj.pk).update(url=url)
                            messages.success(
                                self.request,
                                "Category Changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:category-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Category Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_category.html"
                                ], context)
                    elif slug == 'seo':
                        form = ChangeCategorySEOForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Category SEO Changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:category-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'seo_form': form})
                            messages.error(
                                self.request,
                                "Category SEO Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_category.html"
                                ], context)
                    elif slug == 'skill':
                        form = ChangeCategorySkillForm(
                            request.POST, request.FILES, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Category Skill Changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:category-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'skill_form': form})
                            messages.error(
                                self.request,
                                "Category Skill Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_category.html"
                                ], context)
                    elif slug == 'relation':
                        CategoryRelationshipFormSet = inlineformset_factory(
                            Category, Category.related_to.through,
                            fk_name='related_from',
                            can_delete=False,
                            form=CategoryRelationshipForm,
                            formset=RelationshipInlineFormSet, extra=1,
                            max_num=20, validate_max=True)

                        if self.object.type_level in [2, 3, 4]:
                            formset = CategoryRelationshipFormSet(request.POST, instance=obj)
                            from django.db import transaction
                            if formset.is_valid():
                                with transaction.atomic():
                                    formset.save(commit=False)
                                    saved_formset = formset.save(commit=False)
                                    for ins in formset.deleted_objects:
                                        ins.delete()

                                    for form in saved_formset:
                                        form.save()
                                    formset.save_m2m()

                                messages.success(
                                    self.request,
                                    "Category Relationship changed Successfully")
                                return HttpResponseRedirect(reverse('console:category-change',kwargs={'pk': obj.pk}))
                            else:
                                context = self.get_context_data()
                                if formset:
                                    context.update({'relationship_formset': formset})
                                messages.error(
                                    self.request,
                                    "Category Relationship Change Failed, Changes not Saved")
                                return TemplateResponse(
                                    request, [
                                        "console/shop/change_category.html"
                                    ], context)
                        else:
                            messages.error(
                                self.request,
                                "You cannot add parent for level1")
                            return HttpResponseRedirect(
                                reverse('console:category-change', kwargs={'pk': cat}))
                    elif slug == 'subheading':
                        import ipdb; ipdb.set_trace()
                        SubHeaderFormSet = inlineformset_factory(
                            Category, SubHeaderCategory,
                            fk_name='category',
                            form=SubHeaderCategoryForm,
                            can_delete=True,
                            formset=SubHeaderInlineFormSet, extra=1,
                            max_num=5, validate_max=True)

                        if self.object.type_level in [3, 4]:
                            formset = SubHeaderFormSet(request.POST, instance=obj)
                            from django.db import transaction
                            if formset.is_valid():
                                with transaction.atomic():
                                    formset.save(commit=False)
                                    saved_formset = formset.save(commit=False)
                                    for ins in formset.deleted_objects:
                                        ins.delete()

                                    for form in saved_formset:
                                        form.save()
                                    formset.save_m2m()

                                messages.success(
                                    self.request,
                                    "Category Sub header changed Successfully")
                                return HttpResponseRedirect(reverse('console:category-change',kwargs={'pk': obj.pk}))
                            else:
                                context = self.get_context_data()
                                if formset:
                                    context.update({'sub_heading_formset': formset})
                                messages.error(
                                    self.request,
                                    "Category Sub Header Change Failed, Changes not Saved")
                                return TemplateResponse(
                                    request, [
                                        "console/shop/change_category.html"
                                    ], context)
                        else:
                            messages.error(
                                self.request,
                                "You cannot add Sub Header for level1 and Level2")
                            return HttpResponseRedirect(
                                reverse('console:category-change', kwargs={'pk': cat}))

                    elif slug == 'testimonial_model':
                        TestimonialModelFormset = modelformset_factory(
                            Testimonial,
                            form=TestimonialModelForm,
                            can_delete=True,
                            extra=1,
                            max_num=5, validate_max=True)

                        if self.object.type_level in [3, 4]:
                            formset = TestimonialModelFormset(
                                request.POST, request.FILES,
                                queryset=Testimonial.objects.filter(
                                    page=UNIVERSITY_PAGE, object_id=obj.pk))
                            from django.db import transaction
                            if formset.is_valid():
                                with transaction.atomic():
                                    formset.save(commit=False)
                                    saved_formset = formset.save(commit=False)
                                    for ins in formset.deleted_objects:
                                        ins.delete()

                                    for form in saved_formset:
                                        form.page = UNIVERSITY_PAGE
                                        form.object_id = obj.pk
                                        form.save()
                                    formset.save_m2m()

                                messages.success(
                                    self.request,
                                    "Category Testimonial changed Successfully")
                                return HttpResponseRedirect(reverse('console:category-change',kwargs={'pk': obj.pk}))
                            else:
                                context = self.get_context_data()
                                if formset:
                                    context.update({'testimonial_model_formset': formset})
                                messages.error(
                                    self.request,
                                    "Category Testimonial Change Failed, Changes not Saved")
                                return TemplateResponse(
                                    request, [
                                        "console/shop/change_category.html"
                                    ], context)
                        else:
                            messages.error(
                                self.request,
                                "You cannot add Testimonial for level1 and Level2")
                            return HttpResponseRedirect(
                                reverse('console:category-change', kwargs={'pk': cat}))

                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:category-change', kwargs={'pk': cat}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            return HttpResponseRedirect(
                reverse('console:category-change', kwargs={'pk': cat}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_category'))
class ListCategoryView(ListView, PaginationMixin):
    model = Category
    context_object_name = 'category_list'
    template_name = 'console/shop/list_category.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListCategoryView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListCategoryView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query set%s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListCategoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['category_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_category'))
class ListCategoryRelationView(TemplateView):
    template_name = "console/shop/tree_category.html"
    
    def get(self, request, *args, **kwargs):
        return super(ListCategoryRelationView, self).get(request, args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(ListCategoryRelationView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        levelOne = Category.objects.filter(type_level=1)
        level1 = []
        for l1 in levelOne:
            level2 = []
            levelTwo = l1.get_childrens()
            if levelTwo:
                for l2 in levelTwo:
                    level3 = []
                    levelThree = l2.get_childrens()
                    if levelThree:
                        for l3 in levelThree:
                            level4 = []
                            levelFour = l3.get_childrens()
                            if levelFour:
                                for l4 in levelFour:
                                    level4.append(
                                        OrderedDict({
                                            'pk':l4.pk,
                                            'name': l4.name,
                                            'url': l4.get_full_url(),
                                            'active': l4.active}))
                            level3.append(
                                OrderedDict({
                                    'pk':l3.pk,
                                    'name': l3.name,
                                    'url': l3.get_full_url(),
                                    'active': l3.active,
                                    'childrens': level4}))
                    level2.append(
                        OrderedDict({
                            'pk':l2.pk,
                            'name': l2.name,
                            'url': l2.get_full_url(),
                            'active': l2.active,
                            'childrens': level3}))
            level1.append(
                OrderedDict({
                    'pk':l1.pk,
                    'name': l1.name,
                    'url': l1.get_full_url(),
                    'active': l1.active,
                    'childrens': level2}))
        context.update({
            'messages': alert,
            'level1': level1})
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_add_faq'))
class AddFaqView(FormView):
    form_class = AddFaqForm
    template_name = 'console/shop/add_faq.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:faquestion-add')

    def get(self, request, *args, **kwargs):
        return super(AddFaqView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        user = self.request.user
        if user.has_perm('faq.console_add_faq'):
            faq = form.save()
            messages.success(
                self.request,
                "You have successfully added a faq"
            )
            self.success_url = reverse_lazy('console:faq-list')
            return super(AddFaqView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "You don't have permission to add faq.")
            return super(AddFaqView, self).form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddFaqView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_change_faq'))
class ListFaqView(ListView, PaginationMixin):
    model = FAQuestion
    context_object_name = 'faq_list'
    template_name = 'console/shop/list_faq.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListFaqView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListFaqView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(text__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['faq_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_change_faq'))
class ChangeFaqView(DetailView):
    template_name = 'console/shop/change_faq.html'
    model = FAQuestion

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeFaqView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeFaqView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeFaqForm(
            instance=self.get_object())
        vendor_form = ChangePublicFaqForm(
            instance=self.get_object())
        
        context.update({
            'messages': alert,
            'form': main_change_form,
            'vendor_form': vendor_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                faq = int(request.POST.get('faq'))
                if obj == faq:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if slug == 'main':
                        form = ChangeFaqForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "FAQ Changed Successfully")
                            return HttpResponseRedirect(reverse('console:faq-list',))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "FAQ Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_faq.html"
                                ], context)
                    elif slug == "vendor":
                        form = ChangePublicFaqForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "FAQ Changed Successfully")
                            return HttpResponseRedirect(reverse('console:faq-list',))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'vendor_form': form})
                            messages.error(
                                self.request,
                                "FAQ Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_faq.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faquestion-change', kwargs={'pk': faq}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                return HttpResponseRedirect(
                    reverse('console:faquestion-change', kwargs={'pk': faq}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_add_keyword'))
class AddKeywordView(FormView):
    form_class = AddKeywordForm
    template_name = 'console/shop/add_keyword.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:keyword-add')

    def get(self, request, *args, **kwargs):
        return super(AddKeywordView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddKeywordView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a Keyword"
        )
        self.success_url = reverse_lazy('console:keyword-list')
        return super(AddKeywordView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddKeywordView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_keyword'))
class ListKeywordView(ListView, PaginationMixin):
    model = Keyword
    context_object_name = 'keyword_list'
    template_name = 'console/shop/list_keyword.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListKeywordView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListKeywordView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListKeywordView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListKeywordView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['keyword_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_keyword'))
class ChangeKeywordView(DetailView):
    template_name = 'console/shop/change_keyword.html'
    model = Keyword

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeKeywordView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return super(ChangeKeywordView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeKeywordView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeKeywordView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = AddKeywordForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                key = int(request.POST.get('keyword'))
                if obj == key:
                    obj = self.object = self.get_object()
                    form = None
                    form = AddKeywordForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "Keyword Changed Successfully")
                        return HttpResponseRedirect(reverse('console:keyword-list',))
                    else:
                        context = self.get_context_data()
                        if form:
                            context.update({'form': form})
                        messages.error(
                            self.request,
                            "Keyword Object Change Failed, Changes not Saved")
                        return TemplateResponse(
                            request, [
                                "console/shop/change_keyword.html"
                            ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:keyword-change', kwargs={'pk': key}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                return HttpResponseRedirect(
                    reverse('console:keyword-change', kwargs={'pk': key}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_add_attribute'))
class AddAttributeView(FormView):
    form_class = AddAttributeForm
    template_name = 'console/shop/add_attribute.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:attribute-add')

    def get(self, request, *args, **kwargs):
        return super(AddAttributeView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddAttributeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a attribute"
        )
        self.success_url = reverse_lazy('console:attribute-list')
        return super(AddAttributeView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddAttributeView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_attribute'))
class ListAttributeView(ListView, PaginationMixin):
    model = Attribute
    context_object_name = 'attribute_list'
    template_name = 'console/shop/list_attribute.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListAttributeView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListAttributeView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListAttributeView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListAttributeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['attribute_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_attribute'))
class ChangeAttributeView(DetailView):
    template_name = 'console/shop/change_attribute.html'
    model = Attribute

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeAttributeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeAttributeView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeAttributeView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeAttributeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = AddAttributeForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                attr = int(request.POST.get('attribute'))
                if obj == attr:
                    obj = self.object = self.get_object()
                    form = None
                    form = AddAttributeForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "Attribute Changed Successfully")
                        return HttpResponseRedirect(reverse('console:attribute-list',))
                    else:
                        context = self.get_context_data()
                        if form:
                            context.update({'form': form})
                        messages.error(
                            self.request,
                            "Attribute Object Change Failed, Changes not Saved")
                        return TemplateResponse(
                            request, [
                                "console/shop/change_attribute.html"
                            ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:attribute-change', kwargs={'pk': attr}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            return HttpResponseRedirect(
                    reverse('console:attribute-change', kwargs={'pk': attr}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST, settings.OPERATION_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ListProductView(ListView, PaginationMixin):
    model = Product
    context_object_name = 'product_list'
    template_name = 'console/shop/list_product.html'
    http_method_names = [u'get', ]
    vendor_list = []
    vendor_select = None
    status = None

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        self.status = request.GET.get('is_active', '')
        self.vendor_select = request.GET.get('vendor', '')
        self.vendor_list=Vendor.objects.all().values_list('name',flat=True).distinct()
        return super(ListProductView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListProductView, self).get_queryset()
        queryset = queryset.exclude(type_product=2)
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
            if self.vendor_select:
               queryset=queryset.filter(vendor__name=self.vendor_select)
            if self.status:
                queryset = queryset.filter(active=self.status)

        except Exception as e:
            logging.getLogger('error_log').error('unable to get query-set%s'%str(e))
            pass
        return queryset.select_related('vendor')

    def get_context_data(self, **kwargs):
        context = super(ListProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['product_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
            'vendor_list':self.vendor_list,
            'vendor_select':self.vendor_select,
            self.status: 'selected',
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ChangeProductView(DetailView):
    template_name = 'console/shop/change_product.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.type_product == 2:
            raise Http404
        return super(ChangeProductView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ChangeProductView, self).get_queryset()
        return queryset.select_related('product_class', 'vendor')

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeProductView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeProductForm(
            instance=self.get_object())
        seo_change_form = ChangeProductSEOForm(
            instance=self.get_object())
        op_change_form = ChangeProductOperationForm(
            instance=self.get_object())
        con_change_form = ProductCountryForm(
            instance=self.get_object())
        price_change_form = ProductPriceForm(
            instance=self.get_object())

        attribute_form = ProductAttributeForm(
            instance=self.get_object(),)
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            vendor = self.get_object().vendor
        else:
            vendor = self.request.user.get_vendor()

        ProductSkillFormSet = inlineformset_factory(
            Product, Skill.skillproducts.through,
            fk_name='product',
            form=ProductSkillForm,
            can_delete=True,
            formset=SkillInlineFormSet, extra=1,
            max_num=15, validate_max=True)

        if self.object:
            prdskill_formset = ProductSkillFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdskill_formset': prdskill_formset})

        ProductCategoryFormSet = inlineformset_factory(
            Product, Product.categories.through, fk_name='product',
            form=ProductCategoryForm,
            can_delete=False,
            formset=CategoryInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdcat_formset = ProductCategoryFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdcat_formset': prdcat_formset})

        ProductFAQFormSet = inlineformset_factory(
            Product, Product.faqs.through, fk_name='product',
            form=ProductFAQForm,
            can_delete=False,
            formset=FAQInlineFormSet, extra=1,
            max_num=50, validate_max=True)
        if self.object:
            prdfaq_formset = ProductFAQFormSet(
                instance=self.get_object(),
                form_kwargs={
                    'object': self.get_object(),
                    'vendor': vendor},)
            context.update({'prdfaq_formset': prdfaq_formset})

        ProductChapterFormSet = inlineformset_factory(
            Product, Chapter, fk_name='product',
            form=ProductChapterForm,
            can_delete=False,
            formset=ChapterInlineFormSet, extra=1,
            max_num=50, validate_max=True)
        if self.object:
            prdchapter_formset = ProductChapterFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()},)
            context.update({'prdchapter_formset': prdchapter_formset})

        if self.object.type_product == 1:
            ProductVariationFormSet = inlineformset_factory(
                Product, Product.variation.through, fk_name='main',
                form=ProductVariationForm,
                can_delete=False,
                formset=VariationInlineFormSet, extra=0,
                max_num=20, validate_max=True)
            if self.object:
                prdvar_formset = ProductVariationFormSet(
                    instance=self.get_object(),
                    form_kwargs={'object': self.get_object()})
                context.update({'prdvars_formset': prdvar_formset})
        if self.object.type_product == 3:
            ProductChildFormSet = inlineformset_factory(
                Product, Product.childs.through, fk_name='father',
                form=ProductChildForm,
                can_delete=False,
                formset=ChildInlineFormSet, extra=1,
                max_num=20, validate_max=True)
            if self.object:
                prdchild_formset = ProductChildFormSet(
                    instance=self.get_object(),
                    form_kwargs={'object': self.get_object()})
                context.update({'prdchild_formset': prdchild_formset})
        if self.object.type_product in [0, 1, 3, 5]:
            ProductRelatedFormSet = inlineformset_factory(
                Product, Product.related.through, fk_name='primary',
                form=ProductRelatedForm,
                can_delete=False,
                formset=RelatedInlineFormSet, extra=1,
                max_num=20, validate_max=True)
            if self.object:
                prdrelated_formset = ProductRelatedFormSet(
                    instance=self.get_object(),
                    form_kwargs={'object': self.get_object()})
                context.update({'prdrelated_formset': prdrelated_formset})
        if self.object.type_flow == 14:
            context.update({'prd_university_form': UniversityCourseForm(
                instance=self.object.university_course_detail)})
            TestimonialModelFormset = modelformset_factory(
                Testimonial, form=TestimonialModelForm,
                can_delete=True, extra=1, max_num=5,
                validate_max=True)
            testimonial_model_formset = TestimonialModelFormset(
                data=None,
                queryset=Testimonial.objects.filter(
                    page=UNIVERSITY_COURSE,
                    object_id=self.object.pk))
            context.update({'testimonial_model_formset': testimonial_model_formset})
            UniversityCoursesPaymentFormset = inlineformset_factory(
                Product, UniversityCoursePayment,
                fk_name='product',
                form=UniversityCoursePaymentForm,
                can_delete=True,
                formset=UniversityCoursesPaymentInlineFormset, extra=1,
                max_num=15, validate_max=True
            )
            university_payment_formset = UniversityCoursesPaymentFormset(instance=self.object)
            context.update({'prd_university_payment_formset': university_payment_formset })

        context.update({
            'sub_type_flow_choices': json.dumps(SUB_FLOWS),
            'messages': alert,
            'form': main_change_form,
            'seo_form': seo_change_form,
            'op_form': op_change_form,
            'country_form': con_change_form,
            'price_form': price_change_form,
            'attribute_form': attribute_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if obj.type_product == 2:
                        messages.error(
                        self.request,
                        "Product is a child variation")
                        return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                    
                    if slug == 'main':
                        form = ChangeProductForm(
                            request.POST, request.FILES, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Object Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Product Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'seo':
                        form = ChangeProductSEOForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product SEO Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'seo_form': form})
                            messages.error(
                                self.request,
                                "Product SEO Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'operation':
                        form = ChangeProductOperationForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Operation Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'op_form': form})
                            messages.error(
                                self.request,
                                "Product Operation Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'country':
                        form = ProductCountryForm(request.POST, instance=obj)
                        if form.is_valid():
                            product = form.save()
                            messages.success(
                                self.request,
                                "Product Countries Visible changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'country_form': form})
                            messages.error(
                                self.request,
                                "Product Country Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'price':
                        form = ProductPriceForm(request.POST, instance=obj)
                        if form.is_valid():
                            product = form.save()
                            messages.success(
                                self.request,
                                "Product Prices changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'price_form': form})
                            messages.error(
                                self.request,
                                "Product Prices Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'attribute':
                        form = ProductAttributeForm(
                                request.POST,
                                request.FILES,
                                instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Attributes changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'attribute_form': form})
                            messages.error(
                                self.request,
                                "Product Attributes Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'prdcategory':
                        ProductCategoryFormSet = inlineformset_factory(
                            Product, Product.categories.through,
                            fk_name='product',
                            form=ProductCategoryForm,
                            can_delete=False,
                            formset=CategoryInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductCategoryFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                            obj.title=obj.get_title()
                            obj.save()
                            messages.success(
                                self.request,
                                "Product Category changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdcat_formset': formset})
                            messages.error(
                                self.request,
                                "Product Category Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'faqs':
                        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                            vendor = self.get_object().vendor
                        else:
                            vendor = self.request.user.get_vendor()
                        
                        ProductFAQFormSet = inlineformset_factory(
                            Product, Product.faqs.through, fk_name='product',
                            form=ProductFAQForm,
                            can_delete=False,
                            formset=FAQInlineFormSet, extra=0,
                            max_num=50, validate_max=True)
                        formset = ProductFAQFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj,
                                'vendor':vendor },)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                
                            messages.success(
                                self.request,
                                "Product FAQ changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdfaq_formset': formset})
                            messages.error(
                                self.request,
                                "Product FAQ Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'vars':
                        ProductVariationFormSet = inlineformset_factory(
                            Product, Product.variation.through, fk_name='main',
                            form=ProductVariationForm,
                            can_delete=False,
                            formset=VariationInlineFormSet, extra=0,
                            max_num=20, validate_max=True)
                        formset = ProductVariationFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                if obj.type_product == 1:
                                    obj.is_indexable = False
                                    obj.save()
                                    childs = obj.mainproduct.all()
                                    for child in childs:
                                        sibling = child.sibling
                                        sibling.is_indexable = False
                                        sibling.save()
                            
                            messages.success(
                                self.request,
                                "Product Variation changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdvars_formset': formset})
                            messages.error(
                                self.request,
                                "Product Variation Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'child':
                        ProductChildFormSet = inlineformset_factory(
                            Product, Product.childs.through, fk_name='father',
                            form=ProductChildForm,
                            can_delete=False,
                            formset=ChildInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductChildFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj})
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Child changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdchild_formset': formset})
                            messages.error(
                                self.request,
                                "Product Child Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'relation':
                        ProductRelatedFormSet = inlineformset_factory(
                            Product, Product.related.through, fk_name='primary',
                            form=ProductRelatedForm,
                            can_delete=False,
                            formset=RelatedInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductRelatedFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj})
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Related changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdrelated_formset': formset})
                            messages.error(
                                self.request,
                                "Product Related Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'chapter':
                        ProductChapterFormSet = inlineformset_factory(
                            Product, Chapter, fk_name='product',
                            form=ProductChapterForm,
                            can_delete=False,
                            formset=ChapterInlineFormSet, extra=1,
                            max_num=50, validate_max=True)
                        formset = ProductChapterFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                
                            messages.success(
                                self.request,
                                "Product Chapter changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdchapter_formset': formset})
                            messages.error(
                                self.request,
                                "Product Chapter Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)

                    elif slug == 'university':
                        form = UniversityCourseForm(request.POST, request.FILES, instance=obj.university_course_detail)
                        application_process_priority = [k for k in form.data['application_process_priority'].split(',') if k]

                        if application_process_priority:
                            form.data['application_process'] = str(application_process_priority)

                        benefits_priority = [k for k in form.data['benefits_priority'].split(',') if k]
                        form.data['benefits'] = str(benefits_priority) if benefits_priority else ''
                        headings = [key for key in form.data.keys() if key.startswith('heading')]
                        attendees_criteria = []

                        for heading in sorted(headings):
                            if form.data[heading] or form.data['sub' + heading]:
                                attendees_criteria.append((form.data[heading], form.data['sub'+heading]))

                        form.data['attendees_criteria'] = str(attendees_criteria)

                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "University course details changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'prd_university_form': form})
                            messages.error(
                                self.request,
                                "University course details Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)

                    elif slug == 'university_payment':
                        UniversityCoursesPaymentFormset = inlineformset_factory(
                            Product, UniversityCoursePayment,
                            form=UniversityCoursePaymentForm,
                            can_delete=True,
                            extra=2,
                            max_num=15, validate_max=True
                        )
                        formset = UniversityCoursesPaymentFormset(
                            request.POST, instance=obj)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                            messages.success(
                                self.request,
                                "University course Changed Successfully")
                            return HttpResponseRedirect(
                                reverse(
                                    'console:product-change',
                                    kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prd_university_payment_formset': formset})
                            messages.error(
                                self.request,
                                "University course payment Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                    elif slug == 'testimonial_model':
                        TestimonialModelFormset = modelformset_factory(
                            Testimonial,
                            form=TestimonialModelForm,
                            can_delete=True,
                            extra=1,
                            max_num=5, validate_max=True)

                        if self.object.type_flow == 14:
                            formset = TestimonialModelFormset(
                                request.POST, request.FILES,
                                queryset=Testimonial.objects.filter(
                                    page=UNIVERSITY_COURSE, object_id=obj.pk))
                            from django.db import transaction
                            if formset.is_valid():
                                with transaction.atomic():
                                    formset.save(commit=False)
                                    saved_formset = formset.save(commit=False)
                                    for ins in formset.deleted_objects:
                                        ins.delete()

                                    for form in saved_formset:
                                        form.page = UNIVERSITY_COURSE
                                        form.object_id = obj.pk
                                        form.save()
                                    formset.save_m2m()

                                messages.success(
                                    self.request,
                                    "University Course Testimonial changed Successfully")
                                return HttpResponseRedirect(
                                    reverse(
                                        'console:product-change',
                                        kwargs={'pk': obj.pk}))
                            else:
                                context = self.get_context_data()
                                if formset:
                                    context.update({'testimonial_model_formset': formset})
                                messages.error(
                                    self.request,
                                    "University Course Testimonial Change Failed, Changes not Saved")
                                return TemplateResponse(
                                    request, [
                                        "console/shop/change_product.html"
                                    ], context)
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prd_university_payment_formset': formset})
                            messages.error(
                                self.request,
                                "University Course Change Failed, \
                                Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_product.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST, settings.OPERATION_GROUP_LIST ]))
@Decorate(check_permission('shop.console_change_product'))
class OPChangeProductView(DetailView):
    template_name = 'console/shop/change_productops.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(OPChangeProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if product.type_product == 2:
            raise Http404
        return super(OPChangeProductView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(OPChangeProductView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(OPChangeProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        op_change_form = ChangeProductOperationForm(
            instance=self.get_object())
        
        context.update({
            'messages': alert,
            'op_form': op_change_form,
            })
        return context

    def post(self, request, *args, **kwargs ):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    if obj.type_product == 2:
                        messages.error(
                        self.request,
                        "Product is a child variation")
                        return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                    
                    form = None
                    if slug == 'operation':
                        form = ChangeProductOperationForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Operation Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-opschange',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'op_form': form})
                            messages.error(
                                self.request,
                                "Product Operation Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productops.html"
                                ], context)
                    messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-changeops', kwargs={'pk': prd}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                return HttpResponseRedirect(
                    reverse('console:product-changeops', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST,]))
@Decorate(check_permission('shop.console_change_product'))
class ChangeProductVariantView(DetailView):
    template_name = 'console/shop/change_productvariant.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(
            ChangeProductVariantView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if not product.type_product == 2:
            raise Http404
        
        return super(
            ChangeProductVariantView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(
                ChangeProductVariantView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(
            ChangeProductVariantView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        pk_parent = kwargs.get('parent',None)
        parent = self.get_object().get_parent()
        
        main_change_form = ChangeProductVariantForm(parent=parent,
            user=self.request.user, instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form,
            'parent': parent.pk if parent else None
            })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                parent = int(self.kwargs.get('parent', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if not obj.type_product == 2:
                        messages.error(
                        self.request,
                        "Product is not a child variation")
                        return HttpResponseRedirect(reverse('console:product-change',kwargs={'pk': obj.pk}))
                    
                    if slug == 'variant':
                        parent = self.get_object().get_parent()
                        form = ChangeProductVariantForm(
                            request.POST, request.FILES,
                            parent=parent,
                            user=self.request.user,
                            instance=obj)

                        if form.is_valid():
                            product = form.save()
                            messages.success(
                                self.request,
                                "Product Changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:productvariant-change',
                                    kwargs={'pk': obj.pk, 'parent': parent.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Product Variant Add Failed, Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productvariant.html"
                                ], context)
                        messages.error(
                        self.request,
                        "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productvariant-change', kwargs={'pk': prd, 'parent': parent}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                return HttpResponseRedirect(
                    reverse('console:productvariant-change', kwargs={'pk': prd, 'parent': parent}))
        return HttpResponseBadRequest()


@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_category'))
class ActionCategoryView(View, CategoryValidation):

    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            action = form_data.get('action', None)
            pk_obj = form_data.get('category', None)
            allowed_action = []
            if has_group(user=self.request.user,
                grp_list=settings.PRODUCT_GROUP_LIST):
                allowed_action = ['active', 'inactive', 'skill',
                'noskill', 'service', 'noservice',
                'university', 'nouniversity']
            else:
                allowed_action = []

            if action and action in allowed_action:
                try:
                    category = Category.objects.get(pk=pk_obj)
                    if action == "active":
                        if self.validate_before_active(
                            request=self.request, category=category):    
                            category.active = True
                            category.save()
                            messages.success(
                                self.request,
                                    "Category is made active!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "inactive":
                        if self.validate_before_inactive(
                            request=self.request,category=category):
                            category.active = False
                            category.save()    
                            messages.success(
                                self.request,
                                    "Category is made inactive!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "skill":
                        if self.validate_before_skill(
                            request=self.request,category=category):
                            category.is_skill = True
                            category.save()    
                            messages.success(
                                self.request,
                                    "Category is made skill!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "noskill":
                            category.is_skill = False
                            category.save()    
                            messages.success(
                                self.request,
                                    "Category is removed as skill!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                    
                    elif action == "service":
                        category.is_service = True
                        category.save()    
                        messages.success(
                            self.request,
                                "Category is made service!") 
                        data = {'success': 'True',
                            'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                        # else:
                        #     data = {'error': 'True'}
                    elif action == "noservice":
                            category.is_service = False
                            category.save()    
                            messages.success(
                                self.request,
                                    "Category is removed as service!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }

                    elif action == "university":
                        if self.validate_before_university(
                            request=self.request, category=category):
                            category.is_university = True
                            category.save()
                            messages.success(
                                self.request,
                                    "Category is made university!")
                            data = {'success': 'True',
                                'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "nouniversity":
                        category.is_university = False
                        category.save()
                        messages.success(
                            self.request,
                                "Category is removed as university!")
                        data = {'success': 'True',
                            'next_url': reverse('console:category-change', kwargs={'pk': category.pk}) }

                except Exception as e:
                    logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                    messages.error(request, (
                        ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                    data = {'error': 'True'}
            else:
                data = {'error': 'True'}
                messages.error(
                    self.request,
                    "Invalid Action, Do not have permission!")
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

        data = {'error': 'True'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ActionProductView(View, ProductValidation):

    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            action = form_data.get('action', None)
            pk_obj = form_data.get('product', None)
            allowed_action = []

            if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                allowed_action = ['active', 'inactive','index', 'unindex',"show-on-crm","hide-on-crm"]
            else:
                allowed_action = []

            if action and action in allowed_action:
                try:
                    product = Product.objects.get(pk=pk_obj)
                    
                    if action == "show-on-crm" and not product.is_indexable:
                        data = {'error': 'True'}
                        messages.error(self.request,"Only indexable products can be visible on CRM.")
                        return HttpResponse(json.dumps(data), content_type="application/json")

                    if action == "active":
                        if self.validate_before_active(request=self.request,product=product):    
                            product.active = True
                            product.save()
                            if product.type_product == 1:
                                childs = product.mainproduct.filter(active=True)
                                for child in childs:
                                    sibling = child.sibling
                                    sibling.type_flow = product.type_flow
                                    sibling.active = True
                                    sibling.save()
                            messages.success(
                                self.request,
                                    "Product is made active!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "inactive":
                            product.active = False
                            product.is_indexable = False
                            product.save() 
                            if product.type_product == 1:
                                childs = product.mainproduct.all()
                                for child in childs:
                                    sibling = child.sibling
                                    sibling.is_indexable = False
                                    sibling.active = False
                                    sibling.save()
                            messages.success(
                                self.request,
                                    "Product is made inactive!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }
                    elif action == "index":
                        if self.validate_before_index(request=self.request,product=product):
                            product.is_indexable = True
                            product.save()    
                            if product.type_product == 1:
                                childs = product.mainproduct.filter(active=True)
                                for child in childs:
                                    sibling = child.sibling
                                    sibling.type_flow = product.type_flow
                                    sibling.is_indexable = True
                                    sibling.save()
                            messages.success(
                                self.request,
                                    "Product will now be indexed.") 
                            data = {'success': 'True',
                                'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }
                        else:
                            data = {'error': 'True'}
                    elif action == "unindex":
                        product.is_indexable = False
                        product.save()
                        if product.type_product == 1:
                            childs = product.mainproduct.all()
                            for child in childs:
                                sibling = child.sibling
                                sibling.is_indexable = False
                                sibling.save()
                        messages.success(
                            self.request,
                                "Product is removed from indexing!") 
                        data = {'success': 'True',
                            'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }

                    elif action in ["show-on-crm","hide-on-crm"]:
                        action_bool_mapping = {"show-on-crm":True,
                                            "hide-on-crm":False}

                        setattr(product,"visible_on_crm",action_bool_mapping.get(action))
                        product.save()
                        
                        if product.type_product == 1:
                            childs = product.mainproduct.filter(active=True)
                            for child in childs:
                                sibling = child.sibling
                                setattr(sibling,"visible_on_crm",action_bool_mapping.get(action))
                                sibling.save()
                        
                        messages.success(self.request,"CRM visibility updated.") 
                        data = {'success': 'True',
                            'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }
                        

                except Exception as e:
                    logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                    messages.error(request, (
                        ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                    data = {'error': 'True'}
            else:
                data = {'error': 'True'}
                messages.error(
                    self.request,
                    "Invalid Action, Do not have permission!")
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
        data = {'error': 'True'}
        return HttpResponse(json.dumps(data), content_type="application/json")


class ProductAuditHistoryView(UserGroupMixin, ListView, PaginationMixin):
    model = ProductAuditHistory
    template_name = 'console/tasks/product-audit-history.html'
    context_object_name = 'product_audit_list'
    page = 1
    paginated_by = 20
    query = ''
    group_names = ['FINANCE', 'PRODUCT']

    def get_queryset(self):
        self.page = self.request.GET.get('page', 1)
        product_id = self.request.GET.get('product_id', '')
        date_range = self.request.GET.get('date_range', '')
        queryset = self.model.objects.all().order_by('-created_at')
        filter_kwargs = {}
        if product_id:
            filter_kwargs['product_id'] = product_id
        if date_range:
            start_date, end_date = date_range.split(' - ')
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y") + relativedelta(days=1)
            start_id = bson.ObjectId.from_datetime(start_date)
            end_id = bson.ObjectId.from_datetime(end_date)
            filter_kwargs['id__gte'] = start_id
            filter_kwargs['id__lte'] = end_id

        return queryset.filter(**filter_kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductAuditHistoryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['product_audit_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        context['vendor_list'] = Vendor.objects.values_list('id', 'name')
        return context


class ProductHistoryLogDownloadView(UserGroupMixin, View):
    model = ProductAuditHistory
    date_range = None
    product_id = None
    group_names = ['FINANCE', 'PRODUCT']

    def get_queryset(self):
        self.page = self.request.GET.get('page', 1)
        queryset = self.model.objects.all().order_by('-created_at')
        if self.product_id:
            queryset = queryset.filter(product_id=self.product_id)
        if self.date_range:
            start_date, end_date = self.date_range.split(' - ')
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")
            end_date = end_date + relativedelta(days=1)
            start_id = bson.ObjectId.from_datetime(start_date)
            end_id = bson.ObjectId.from_datetime(end_date)
            queryset = queryset.filter(id__gte=start_id, id__lte=end_id)
        return queryset

    def post(self, request, *args, **kwargs):
        self.product_id = self.request.POST.get('product_id', '')
        self.date_range = self.request.POST.get('date_range', '')

        if self.date_range and self.product_id:
            queryset = self.get_queryset()
            return self.download_csv_file(queryset)
        else:
            messages.add_message(request, messages.ERROR, 'Please select Product and Date Range')
            return HttpResponseRedirect(reverse('console:product-audit-history'))

    def download_csv_file(self, queryset):
        product_name = 'no_log'
        try:
            csvfile = StringIO()
            csv_writer = csv.writer(
                csvfile, delimiter=',', quotechar="'",
                quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([
                'Product Id','Product Name', 'Variation Name', 'UPC',
                'Price', 'Duration', 'Vendor Name', 'Date', 'Time'
            ])

            for log in queryset:
                product_name = log.product_name
                try:
                    csv_writer.writerow([
                        str(log.product_id),
                        str(log.product_name),
                        str(log.variation_name),
                        str(log.upc),
                        str(log.price),
                        str(log.duration),
                        str(log.vendor_name),
                        str(log.created_at.strftime('%d-%b-%Y')),
                        str(log.created_at.strftime('%H:%M:%S'))
                    ])
                except Exception as e:
                    logging.getLogger('error_log').error("%s " % str(e))
                    continue
            file_name = product_name + timezone.now().date().strftime("%Y-%m-%d")
            response = HttpResponse(csvfile.getvalue(), content_type=mimetypes.guess_type('%s.csv' % file_name))
            response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
            return response

        except Exception as e:
            messages.add_message(self.request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('console:product-audit-history'))

class DownloadDiscountReportView(TemplateView):
    template_name = "console/order/discount_report.html"

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if 'order.can_download_discount_report' not in request.user.get_all_permissions():
            return HttpResponseForbidden()
        return super(DownloadDiscountReportView,self).dispatch(request,*args,**kwargs)

    def get_response_for_file_download(self):
        report_type = self.request.POST.get('report_type')
        report_date = self.request.POST.get('report_date')
        file_found = False
        file_path = "reports/discount_report_" + report_date + \
             "_" + report_type + ".csv"
        filename = file_path.split('/')[-1]

        if not settings.IS_GCP:
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            try:
                fsock = FileWrapper(open(file_path, 'rb'))
                file_found = True
            except:
                pass
        else:
            try:
                fsock = GCPPrivateMediaStorage().open(file_path)
                file_found = True
            except:
                pass
        
        if file_found:
            logging.getLogger('info_log').info("Discount Report Downloaded | {},{},{},{}".\
                format(self.request.user.id,self.request.user.get_full_name(),datetime.now(),report_date))
            response = HttpResponse(
                fsock,content_type=mimetypes.guess_type(filename)[0])
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response
        
        else:
            messages.add_message(self.request, messages.ERROR, "No record found.")
            return render(self.request,template_name=self.template_name)

    def get_response_for_file_generation(self):
        start_date_str = self.request.POST.get('gen_start_date')
        end_date_str = self.request.POST.get('gen_end_date')
        filter_type = self.request.POST.get('filter_type')

        if not start_date_str or not end_date_str:
            messages.add_message(self.request, messages.ERROR, "Please provide start and end date")
            return render(self.request,template_name=self.template_name)

        try:
            start_date = datetime.strptime(start_date_str,'%Y_%m_%d')
            end_date = datetime.strptime(end_date_str,'%Y_%m_%d')
        except Exception as e:
            logging.getLogger('error_log').error("Unable to parse date {}".format(e))
            messages.add_message(self.request, messages.ERROR, "Please provide start and end date") 
            return render(self.request,template_name=self.template_name)

        if start_date > end_date:
            messages.add_message(self.request, messages.ERROR, "Start Date must be smaller than End Date")
            return render(self.request,template_name=self.template_name)

        scheduler_obj = Scheduler()
        scheduler_obj.task_type = 8
        scheduler_obj.status = 3
        scheduler_obj.created_by = self.request.user
        scheduler_obj.save()

        generate_discount_report.delay(scheduler_obj.id,start_date,end_date,filter_type)
        return HttpResponseRedirect("/console/tasks/tasklist/")


    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if 'order.can_download_discount_report' not in request.user.get_all_permissions():
            return HttpResponseForbidden()

        action = request.POST.get('action')
        if action == "1":
            return self.get_response_for_file_download()
        return self.get_response_for_file_generation()
        
        
class DownloadUpsellReportView(TemplateView):
    template_name = "console/order/upsell_report.html"

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if 'order.can_download_upsell_report' not in request.user.get_all_permissions():
            return HttpResponseForbidden()
        return super(DownloadUpsellReportView,self).dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if 'order.can_download_upsell_report' not in request.user.get_all_permissions():
            return HttpResponseForbidden()

        report_type = request.POST.get('report_type','')
        report_date = request.POST.get('report_date','')
        report_year,report_month,report_day = map(int,report_date.split("_"))
        file_found = False
        file_path = "reports/{}/{}/lead_upsell_report_{}_{}.csv".format(\
            report_year,report_month,report_day,report_type)
        filename = file_path.split('/')[-1]

        if not settings.IS_GCP:
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            try:
                fsock = FileWrapper(open(file_path, 'rb'))
                file_found = True
            except:
                pass
        else:
            try:
                fsock = GCPPrivateMediaStorage(bucket_name=\
                    settings.CRM_PRIVATE_MEDIA_BUCKET).open(file_path)
                file_found = True
            except:
                pass
        
        if file_found:
            logging.getLogger('info_log').info("Upsell Report Downloaded | {},{},{},{}".\
                format(request.user.id,request.user.get_full_name(),datetime.now(),report_date))
            response = HttpResponse(
                fsock,content_type=mimetypes.guess_type(filename)[0])
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response
        
        else:
            messages.add_message(request, messages.ERROR, "No record found.")
            return render(request,template_name=self.template_name)        
    
# @Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
# @Decorate(check_permission('shop.console_change_attribute'))
# class AddAttributeOptionView(FormView):
#     form_class = AddAttributeOptionForm
#     template_name = 'console/shop/add_attributeoption.html'
#     http_method_names = ['get', 'post']
#     success_url = reverse_lazy('console:attributeoption-add')

#     def get(self, request, *args, **kwargs):
#         return super(AddAttributeOptionView, self).get(
#             request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(AddAttributeOptionView, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
#         context.update({'messages': alert})
#         return context

#     def form_valid(self, form):
#         form.save()
#         messages.success(
#             self.request,
#             "You have successfully added a attribute option group"
#         )
#         self.success_url = reverse_lazy('console:attributeoption-list')
#         return super(AddAttributeOptionView, self).form_valid(form)

#     def form_invalid(self, form):
#         messages.error(
#             self.request,
#             "Your submission has not been saved. Try again."
#         )
#         return super(AddAttributeOptionView, self).form_invalid(form)


# @Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
# @Decorate(check_permission('shop.console_change_attribute'))
# class ListAttributeOptionGroupView(ListView, PaginationMixin):
#     model = AttributeOptionGroup
#     context_object_name = 'optgrp_list'
#     template_name = 'console/shop/list_attributeoption.html'
#     http_method_names = [u'get', ]

#     def dispatch(self, request, *args, **kwargs):
#         self.page = 1
#         self.paginated_by = 50
#         self.query = ''
#         return super(ListAttributeOptionGroupView, self).dispatch(
#             request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         self.page = request.GET.get('page', 1)
#         self.query = request.GET.get('query', '')
#         return super(ListAttributeOptionGroupView, self).get(request, args, **kwargs)

#     def get_queryset(self):
#         queryset = super(ListAttributeOptionGroupView, self).get_queryset()
#         try:
#             if self.query:
#                 queryset = queryset.filter(Q(name__icontains=self.query))
#         except:
#             pass
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(ListAttributeOptionGroupView, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
#         context.update({'messages': alert})
#         paginator = Paginator(context['optgrp_list'], self.paginated_by)
#         context.update(self.pagination(paginator, self.page))
#         alert = messages.get_messages(self.request)
#         context.update({
#             "query": self.query,
#             "messages": alert,
#         })
#         return context


# @Decorate(check_permission('faq.console_moderate_faq'))
# class ListModerationFaqView(ListView, PaginationMixin):
#     model = FAQuestion
#     context_object_name = 'faq_list'
#     template_name = 'console/shop/list_faq.html'
#     http_method_names = [u'get', ]

#     def dispatch(self, request, *args, **kwargs):
#         self.page = 1
#         self.paginated_by = 50
#         self.query = ''
#         return super(ListModerationFaqView, self).dispatch(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         self.page = request.GET.get('page', 1)
#         self.query = request.GET.get('query', '')
#         return super(ListModerationFaqView, self).get(request, args, **kwargs)

#     def get_queryset(self):
#         queryset = super(ListModerationFaqView, self).get_queryset()
#         queryset = queryset.filter(status=0)
#         try:
#             if self.query:
#                 queryset = queryset.filter(Q(text__icontains=self.query))
#         except:
#             pass
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(ListModerationFaqView, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
#         context.update({'messages': alert})
#         paginator = Paginator(context['faq_list'], self.paginated_by)
#         context.update(self.pagination(paginator, self.page))
#         alert = messages.get_messages(self.request)
#         context.update({
#             "query": self.query,
#             "messages": alert,
#         })
#         return context



# @Decorate(check_permission('faq.console_moderate_faq'))
# class ModerateFaqView(DetailView):
#     template_name = 'console/shop/change_faq.html'
#     model = FAQuestion

#     def dispatch(self, request, *args, **kwargs):
#         return super(ModerateFaqView, self).dispatch(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         return super(ModerateFaqView, self).get(request, args, **kwargs)

#     def get_object(self, queryset=None):
#         if hasattr(self, 'object'):
#             return self.object
#         else:
#             return super(ModerateFaqView, self).get_object(queryset)

#     def get_context_data(self, **kwargs):
#         context = super(ModerateFaqView, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
#         main_change_form = ModerateFaqForm(
#             instance=self.get_object())
#         context.update({
#             'messages': alert,
#             'form': main_change_form})
#         return context

#     def post(self, request, *args, **kwargs):
#         if self.request.POST:
#             try:
#                 obj = int(self.kwargs.get('pk', None))
#                 faq = int(request.POST.get('faq'))
#                 if obj == faq:
#                     obj = self.object = self.get_object()
#                     form = None
#                     form = ModerateFaqForm(
#                         request.POST, instance=obj)
#                     if form.is_valid():
#                         form.save()
#                         messages.success(
#                             self.request,
#                             "FAQ Changed Successfully")
#                         return HttpResponseRedirect(reverse('console:mfaquestion-list',))
#                     else:
#                         context = self.get_context_data()
#                         if form:
#                             context.update({'form': form})
#                         messages.error(
#                             self.request,
#                             "FAQ Object Change Failed, Changes not Saved")
#                         return TemplateResponse(
#                             request, [
#                                 "console/shop/change_faq.html"
#                             ], context)
#                 messages.error(
#                     self.request,
#                     "Object Does Not Exists")
#                 return HttpResponseRedirect(
#                     reverse('console:faquestion-moderate', kwargs={'pk': faq}))
#             except:
#                 messages.error(
#                     self.request,
#                     "Object Does Not Exists")
#                 return HttpResponseRedirect(
#                     reverse('console:faquestion-moderate', kwargs={'pk': faq}))
#         return HttpResponseBadRequest()

@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_category'))
class ListSubCategoryView(ListView, PaginationMixin):
    model = SubCategory
    context_object_name = 'category_list'
    template_name = 'console/shop/list_subcategory.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListSubCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListSubCategoryView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListSubCategoryView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query set%s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListSubCategoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['category_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_add_category'))
class AddSubCategoryView(FormView):
    form_class = AddSubCategoryForm
    template_name = 'console/shop/add_subcategory.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:subcategory-add')

    def get(self, request, *args, **kwargs):
        return super(AddSubCategoryView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddSubCategoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a SubCatagory"
        )
        self.success_url = reverse_lazy('console:subcategory-list')
        return super(AddSubCategoryView, self).form_valid(form)

    def form_invalid(self, form):
        super(AddSubCategoryView, self).form_invalid(form)
        context = self.get_context_data()
        context.update({'form':form})
        messages.error(self.request,"Form not saved please check the fields")
        return TemplateResponse(self.request, self.template_name, context)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class SubCategoryChangeView(UpdateView):
    model = SubCategory
    template_name = 'console/shop/change_subcategory.html'
    success_url = reverse_lazy('console:subcategory-list')
    http_method_names = [u'get', u'post']
    form_class = ChangeSubCategoryForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(SubCategoryChangeView, self).get(request, *args, **kwargs)
        return context

    # def get_initial(self):
    #     self.object = self.get_object()
    #     initial = super(SubCategoryChangeView, self).get_initial()
    #     initial['title'] = self.object.title if self.object.title else self.object.get_title()
    #     initial['heading'] = self.object.heading if self.object.heading else self.object.get_heading()
    #     initial['meta_desc'] = self.object.meta_desc if self.object.meta_desc else ""
    #     initial['description'] =self.object.description if self.object.description else self.object.get_description()
    #
    #     return initial

    def get_context_data(self, **kwargs):
        context = super(SubCategoryChangeView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        obj = self.get_object()
        form = ChangeSubCategoryForm(instance=self.get_object())
        context.update({'form':form})
        if obj and obj.products_id_mapped():
            prod_ids = obj.products_id_mapped()
            prod = list(Product.objects.filter(id__in=prod_ids).values('id', 'name'))
            context.update({'selected_products': json.dumps(prod)})

        return context

    def post(self, request, *args, **kwargs):
        obj=self.object = self.get_object()
        form = ChangeSubCategoryForm(request.POST,request.FILES,instance=obj)
        context = self.get_context_data()
        if form.is_valid():
            try:
                form.save()
                valid_form = self.form_valid(form)
                messages.add_message(
                    request, messages.SUCCESS,
                    'Skill %s - %s Updated Successfully.' % (
                        self.object.category.name, self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Form %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        context.update({'form': form})
        messages.add_message(request, messages.ERROR, 'Form Not Updated.Check the fields')

        return TemplateResponse(request,self.template_name, context)


