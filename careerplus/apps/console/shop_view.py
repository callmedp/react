from collections import OrderedDict

from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from .decorators import Decorate, check_permission
from django.core.paginator import Paginator
from django.db.models import Q


from blog.mixins import PaginationMixin
from shop.models import (
    Category, Keyword,
    Attribute, AttributeOptionGroup)

from .shop_form import (
    AddCategoryForm, ChangeCategoryForm,
    ChangeCategorySEOForm,
    CategoryRelationshipForm,
    RelationshipInlineFormSet,
    ChangeCategorySkillForm,)
from shop.forms import (
    AddKeywordForm, AddAttributeOptionForm,
    AddAttributeForm)
from faq.forms import AddFaqForm, AddChapterForm
from faq.models import FAQuestion, Chapter

@Decorate(check_permission('shop.add_category'))
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
        return super(AddCategoryView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddCategoryView, self).form_invalid(form)


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
            can_delete = False,
            formset=RelationshipInlineFormSet, extra=1,
            max_num=20, validate_max=True)

        alert = messages.get_messages(self.request)
        from django.forms.models import model_to_dict
        main_change_form = ChangeCategoryForm(
            instance=self.get_object())
        seo_change_form = ChangeCategorySEOForm(
            instance=self.get_object())
        skill_change_form = ChangeCategorySkillForm(
            instance=self.get_object())
        if self.object.type_level in [2, 3, 4]:
            relationship_formset = CategoryRelationshipFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'relationship_formset': relationship_formset})
        context.update({
            'messages': alert,
            'form': main_change_form,
            'seo_form': seo_change_form,
            'skill_form': skill_change_form})
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
                                "Category Object Changed Successfully")
                            return HttpResponseRedirect(reverse('console:category-change', kwargs={'pk': obj.pk}))
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
                            return HttpResponseRedirect(reverse('console:category-change', kwargs={'pk': obj.pk}))
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
                            return HttpResponseRedirect(reverse('console:category-change', kwargs={'pk': obj.pk}))
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
                            can_delete = False,
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
                                return HttpResponseRedirect(reverse('console:category-change', kwargs={'pk': obj.pk}))
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
                        
                    
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:category-change', kwargs={'pk': cat}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:category-change', kwargs={'pk': cat}))
        return HttpResponseBadRequest()


@Decorate(check_permission('shop.change_category'))
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
                                            'name': l4.name,
                                            'active': l4.active}))
                            level3.append(
                                OrderedDict({
                                    'name': l3.name,
                                    'active': l3.active,
                                    'childrens': level4}))
                    level2.append(
                        OrderedDict({
                            'name': l2.name,
                            'active': l2.active,
                            'childrens': level3}))
            level1.append(
                OrderedDict({
                    'name': l1.name,
                    'active': l1.active,
                    'childrens': level2}))
        context.update({
            'messages': alert,
            'level1': level1})
        return context


@Decorate(check_permission('shop.add_product'))
class AddProductView(FormView):
    form_class = AddCategoryForm
    template_name = 'console/shop/add_product.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:product-add')

    def get(self, request, *args, **kwargs):
        return super(AddProductView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    # def form_valid(self, form):
    #     form.save()
    #     messages.success(
    #         self.request,
    #         "You have successfully added a catagory"
    #     )
    #     return super(AddCategoryView, self).form_valid(form)

    # def form_invalid(self, form):
    #     messages.error(
    #         self.request,
    #         "Your submission has not been saved. Try again."
    #     )
    #     return super(AddCategoryView, self).form_invalid(form)


@Decorate(check_permission('faq.add_faquestion'))
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
        form.save()
        messages.success(
            self.request,
            "You have successfully added a faq"
        )
        return super(AddFaqView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddFaqView, self).form_invalid(form)


@Decorate(check_permission('faq.add_chapter'))
class AddChapterView(FormView):
    form_class = AddChapterForm
    template_name = 'console/shop/add_chapter.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:chapter-add')

    def get(self, request, *args, **kwargs):
        return super(AddChapterView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddChapterView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a Chapter"
        )
        return super(AddChapterView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddChapterView, self).form_invalid(form)


@Decorate(check_permission('shop.add_keyword'))
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
        return super(AddKeywordView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddKeywordView, self).form_invalid(form)


@Decorate(check_permission('shop.add_attributeoption'))
class AddAttributeOptionView(FormView):
    form_class = AddAttributeOptionForm
    template_name = 'console/shop/add_attributeoption.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:attributeoption-add')

    def get(self, request, *args, **kwargs):
        return super(AddAttributeOptionView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddAttributeOptionView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a Keyword"
        )
        return super(AddAttributeOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddAttributeOptionView, self).form_invalid(form)

@Decorate(check_permission('shop.add_attribute'))
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
            "You have successfully added a Keyword"
        )
        return super(AddAttributeView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddAttributeView, self).form_invalid(form)



@Decorate(check_permission('shop.change_category'))
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
        except:
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


@Decorate(check_permission('faq.change_faquestion'))
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
        except:
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


@Decorate(check_permission('shop.change_category'))
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
        except:
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


@Decorate(check_permission('faq.change_chapter'))
class ListChapterView(ListView, PaginationMixin):
    model = Chapter
    context_object_name = 'chapter_list'
    template_name = 'console/shop/list_chapter.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListChapterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListChapterView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListChapterView, self).get_queryset()
        queryset = queryset.filter(parent__isnull=True)
        try:
            if self.query:
                queryset = queryset.filter(Q(heading__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListChapterView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['chapter_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(check_permission('shop.change_keyword'))
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
        except:
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


@Decorate(check_permission('shop.change_attribute'))
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
        except:
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


@Decorate(check_permission('shop.change_attribute'))
class ListAttributeOptionGroupView(ListView, PaginationMixin):
    model = AttributeOptionGroup
    context_object_name = 'optgrp_list'
    template_name = 'console/shop/list_attributeoption.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListAttributeOptionGroupView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListAttributeOptionGroupView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListAttributeOptionGroupView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListAttributeOptionGroupView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['optgrp_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


