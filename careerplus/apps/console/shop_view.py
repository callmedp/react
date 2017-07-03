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
    Attribute, AttributeOptionGroup,
    Product)

from .shop_form import (
    AddCategoryForm, ChangeCategoryForm,
    ChangeCategorySEOForm,
    CategoryRelationshipForm,
    RelationshipInlineFormSet,
    ChangeCategorySkillForm,)

from shop.forms import (
    AddKeywordForm,
    AddAttributeOptionForm,
    AddAttributeForm, AddProductForm,
    ChangeProductForm,
    ChangeProductSEOForm,
    ChangeProductAttributeForm,
    ChangeProductOperationForm,
    ProductCategoryForm,
    ProductStructureForm,
    ProductFAQForm,
    ProductPriceForm,
    CategoryInlineFormSet,
    ChapterInlineFormSet,
    FAQInlineFormSet,
    PriceInlineFormSet,
    ProductCountryForm,
    ProductChildForm,
    ProductRelatedForm,
    ProductVariationForm,
    VariationInlineFormSet,
    ChildInlineFormSet,
    RelatedInlineFormSet)

from faq.forms import (
    AddFaqForm,
    AddChapterForm,
    ChangeFaqForm,
    ModerateFaqForm,
    ChangeChapterForm,
    ModerateChapterForm,)
from faq.models import FAQuestion, Chapter


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
            can_delete = False,
            formset=RelationshipInlineFormSet, extra=1,
            max_num=20, validate_max=True)

        alert = messages.get_messages(self.request)
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
            vendor = user.get_vendor()
            if not vendor:
                messages.error(
                    self.request,
                    "You are not associated to any vendor.")
                return super(AddFaqView, self).form_invalid(form)
            faq = form.save()
            faq.vendor = vendor
            faq.save()
            messages.success(
                self.request,
                "You have successfully added a faq"
            )    
            self.success_url = reverse_lazy('console:faquestion-list')
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


@Decorate(check_permission('faq.console_add_chapter'))
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
        user = self.request.user
        if user.has_perm('faq.console_add_chapter'):
            vendor = user.get_vendor()
            if not vendor:
                messages.error(
                    self.request,
                    "You are not associated to any vendor.")
                return super(AddChapterView, self).form_invalid(form)
            faq = form.save()
            faq.vendor = vendor
            faq.save()
            messages.success(
                self.request,
                "You have successfully added a chapter"
            )    
            self.success_url = reverse_lazy('console:chapter-list')
            return super(AddChapterView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "You don't have permission to add chapter.")          
            return super(AddChapterView, self).form_invalid(form)
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
        self.success_url = reverse_lazy('console:keyword-list')
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
            "You have successfully added a attribute option group"
        )
        self.success_url = reverse_lazy('console:attributeoption-list')
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
        vendor = self.request.user.get_vendor()
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(vendor=vendor)
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


@Decorate(check_permission('faq.console_moderate_faq'))
class ListModerationFaqView(ListView, PaginationMixin):
    model = FAQuestion
    context_object_name = 'faq_list'
    template_name = 'console/shop/list_faq.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListModerationFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListModerationFaqView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListModerationFaqView, self).get_queryset()
        queryset = queryset.filter(status=0)
        try:
            if self.query:
                queryset = queryset.filter(Q(text__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListModerationFaqView, self).get_context_data(**kwargs)
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


@Decorate(check_permission('faq.console_change_chapter'))
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
        vendor = self.request.user.get_vendor()
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(vendor=vendor)
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



@Decorate(check_permission('faq.console_moderate_chapter'))
class ListModerationChapterView(ListView, PaginationMixin):
    model = Chapter
    context_object_name = 'chapter_list'
    template_name = 'console/shop/list_chapter.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListModerationChapterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListModerationChapterView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListModerationChapterView, self).get_queryset()
        queryset = queryset.filter(parent__isnull=True)
        queryset = queryset.filter(status=0)
        try:
            if self.query:
                queryset = queryset.filter(Q(heading__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListModerationChapterView, self).get_context_data(**kwargs)
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
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:attribute-change', kwargs={'pk': attr}))
        return HttpResponseBadRequest()


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
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                faq = int(request.POST.get('faq'))
                if obj == faq:
                    obj = self.object = self.get_object()
                    form = None
                    form = ChangeFaqForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "FAQ Changed Successfully")
                        return HttpResponseRedirect(reverse('console:faquestion-list',))
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
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faquestion-change', kwargs={'pk': faq}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faquestion-change', kwargs={'pk': faq}))
        return HttpResponseBadRequest()


@Decorate(check_permission('faq.console_moderate_faq'))
class ModerateFaqView(DetailView):
    template_name = 'console/shop/change_faq.html'
    model = FAQuestion

    def dispatch(self, request, *args, **kwargs):
        return super(ModerateFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ModerateFaqView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ModerateFaqView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ModerateFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ModerateFaqForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                faq = int(request.POST.get('faq'))
                if obj == faq:
                    obj = self.object = self.get_object()
                    form = None
                    form = ModerateFaqForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "FAQ Changed Successfully")
                        return HttpResponseRedirect(reverse('console:mfaquestion-list',))
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
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faquestion-moderate', kwargs={'pk': faq}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faquestion-moderate', kwargs={'pk': faq}))
        return HttpResponseBadRequest()


@Decorate(check_permission('faq.console_change_chapter'))
class ChangeChapterView(DetailView):
    template_name = 'console/shop/change_chapter.html'
    model = Chapter

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeChapterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeChapterView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeChapterView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeChapterView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeChapterForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                chapter = int(request.POST.get('chapter'))
                if obj == chapter:
                    obj = self.object = self.get_object()
                    form = None
                    form = ChangeChapterForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "Chapter Changed Successfully")
                        return HttpResponseRedirect(reverse('console:chapter-list',))
                    else:
                        context = self.get_context_data()
                        if form:
                            context.update({'form': form})
                        messages.error(
                            self.request,
                            "Chapter Object Change Failed, Changes not Saved")
                        return TemplateResponse(
                            request, [
                                "console/shop/change_chapter.html"
                            ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:chapter-change', kwargs={'pk': chapter}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:chapter-change', kwargs={'pk': chapter}))
        return HttpResponseBadRequest()


@Decorate(check_permission('faq.console_moderate_chapter'))
class ModerateChapterView(DetailView):
    template_name = 'console/shop/change_chapter.html'
    model = Chapter

    def dispatch(self, request, *args, **kwargs):
        return super(ModerateChapterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ModerateChapterView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ModerateChapterView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ModerateChapterView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ModerateChapterForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                chapter = int(request.POST.get('chapter'))
                if obj == chapter:
                    obj = self.object = self.get_object()
                    form = None
                    form = ModerateChapterForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "Chapter Changed Successfully")
                        return HttpResponseRedirect(reverse('console:mchapter-list',))
                    else:
                        context = self.get_context_data()
                        if form:
                            context.update({'form': form})
                        messages.error(
                            self.request,
                            "Chapter Object Change Failed, Changes not Saved")
                        return TemplateResponse(
                            request, [
                                "console/shop/change_chapter.html"
                            ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:chapter-moderate', kwargs={'pk': chapter}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:chapter-moderate', kwargs={'pk': chapter}))
        return HttpResponseBadRequest()

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
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:keyword-change', kwargs={'pk': key}))
        return HttpResponseBadRequest()



@Decorate(check_permission('shop.change_product'))
class ListProductView(ListView, PaginationMixin):
    model = Product
    context_object_name = 'product_list'
    template_name = 'console/shop/list_product.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(ListProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListProductView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListProductView, self).get_queryset()
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except:
            pass
        return queryset

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
        })
        return context


@Decorate(check_permission('shop.add_product'))
class AddProductView(FormView):
    form_class = AddProductForm
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

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a product"
        )
        self.success_url = reverse_lazy('console:product-list')
        return super(AddProductView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddProductView, self).form_invalid(form)

@Decorate(check_permission('shop.change_product'))
class ChangeProductView(DetailView):
    template_name = 'console/shop/change_product.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeProductView, self).get(request, args, **kwargs)

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
        attr_change_form = ChangeProductAttributeForm(
            instance=self.get_object())
        op_change_form = ChangeProductOperationForm(
            instance=self.get_object())
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
        context.update({
            'messages': alert,
            'form': main_change_form,
            'seo_form': seo_change_form,
            'attr_form': attr_change_form,
            'op_form': op_change_form})
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
                    if slug == 'main':
                        form = ChangeProductForm(
                            request.POST, request.FILES, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Object Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-list',))
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
                            return HttpResponseRedirect(reverse('console:product-list',))
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
                            return HttpResponseRedirect(reverse('console:product-list',))
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
                    elif slug == 'attribute':
                        form = ChangeProductAttributeForm(
                            request.POST, instance=obj)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Attribute Changed Successfully")
                            return HttpResponseRedirect(reverse('console:product-list',))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'attr_form': form})
                            messages.error(
                                self.request,
                                "Product Attribute Change Failed, Changes not Saved")
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
                                formset.save_m2m()

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
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(check_permission('shop.add_productchapter'))
class ChangeProductStructureView(DetailView):
    template_name = 'console/shop/change_productstructure.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductStructureView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeProductStructureView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeProductStructureView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeProductStructureView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        ProductChapterFormSet = inlineformset_factory(
            Product, Product.chapters.through, fk_name='product',
            form=ProductStructureForm,
            can_delete=True,
            formset=ChapterInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdstruct_formset = ProductChapterFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdstruct_formset': prdstruct_formset})
        ProductFAQFormSet = inlineformset_factory(
            Product, Product.faqs.through, fk_name='product',
            form=ProductFAQForm,
            can_delete=True,
            formset=FAQInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdfaq_formset = ProductFAQFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdfaq_formset': prdfaq_formset})
        context.update({
            'messages': alert})
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
                    if slug == 'structure':
                        ProductChapterFormSet = inlineformset_factory(
                            Product, Product.chapters.through,
                            fk_name='product',
                            form=ProductStructureForm,
                            can_delete=True,
                            formset=ChapterInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductChapterFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Chapter changed Successfully")
                            return HttpResponseRedirect(reverse('console:productstructure-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdstruct_formset': formset})
                            messages.error(
                                self.request,
                                "Product Structure Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productstructure.html"
                                ], context)
                    elif slug == 'faqs':
                        ProductFAQFormSet = inlineformset_factory(
                            Product, Product.faqs.through, fk_name='product',
                            form=ProductFAQForm,
                            can_delete=True,
                            formset=FAQInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductFAQFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product FAQ changed Successfully")
                            return HttpResponseRedirect(reverse('console:productstructure-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdfaq_formset': formset})
                            messages.error(
                                self.request,
                                "Product FAQ Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productstructure.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:product-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(check_permission('shop.add_productprice'))
class ChangeProductPriceView(DetailView):
    template_name = 'console/shop/change_productprice.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductPriceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeProductPriceView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeProductPriceView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeProductPriceView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        ProductPriceFormSet = inlineformset_factory(
            Product, Product.prices.through, fk_name='product',
            form=ProductPriceForm,
            can_delete=False,
            formset=PriceInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        countryform = ProductCountryForm(instance=self.get_object())
        if self.object:
            prdprice_formset = ProductPriceFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdprice_formset': prdprice_formset})
        context.update({
            'messages': alert,
            'country_form': countryform})
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
                    if slug == 'price':
                        ProductPriceFormSet = inlineformset_factory(
                            Product, Product.prices.through, fk_name='product',
                            form=ProductPriceForm,
                            can_delete=False,
                            formset=PriceInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductPriceFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Price changed Successfully")
                            return HttpResponseRedirect(reverse('console:productprice-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdprice_formset': formset})
                            messages.error(
                                self.request,
                                "Product Price Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productprice.html"
                                ], context)

                    elif slug == 'country':
                        form = ProductCountryForm(request.POST, instance=obj)
                        if form.is_valid():
                            product = form.save(commit=True)
                            messages.success(
                                self.request,
                                "Product Countries changed Successfully")
                            return HttpResponseRedirect(reverse('console:productprice-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'country_form': form})
                            messages.error(
                                self.request,
                                "Product Country Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productprice.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productprice-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productprice-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(check_permission('shop.add_variationproduct'))
class ChangeProductChildView(DetailView):
    template_name = 'console/shop/change_productchild.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductChildView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeProductChildView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeProductChildView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeProductChildView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        ProductChildFormSet = inlineformset_factory(
            Product, Product.childs.through, fk_name='father',
            form=ProductChildForm,
            can_delete=True,
            formset=ChildInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdchild_formset = ProductChildFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdchild_formset': prdchild_formset})
        ProductRelatedFormSet = inlineformset_factory(
            Product, Product.related.through, fk_name='primary',
            form=ProductRelatedForm,
            can_delete=True,
            formset=RelatedInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdrelated_formset = ProductRelatedFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdrelated_formset': prdrelated_formset})
        context.update({
            'messages': alert})
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
                    if slug == 'child':
                        ProductChildFormSet = inlineformset_factory(
                            Product, Product.childs.through, fk_name='father',
                            form=ProductChildForm,
                            can_delete=True,
                            formset=ChildInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductChildFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Child changed Successfully")
                            return HttpResponseRedirect(reverse('console:productchild-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdchild_formset': formset})
                            messages.error(
                                self.request,
                                "Product Child Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productchild.html"
                                ], context)
                    elif slug == 'relation':
                        ProductRelatedFormSet = inlineformset_factory(
                            Product, Product.related.through, fk_name='primary',
                            form=ProductRelatedForm,
                            can_delete=True,
                            formset=RelatedInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductRelatedFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Related changed Successfully")
                            return HttpResponseRedirect(reverse('console:productchild-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdrelated_formset': formset})
                            messages.error(
                                self.request,
                                "Product Related Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productchild.html"
                                ], context)

                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productchild-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productchild-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(check_permission('shop.add_childproduct'))
class ChangeProductVariationView(DetailView):
    template_name = 'console/shop/change_productvariation.html'
    model = Product

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeProductVariationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ChangeProductVariationView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeProductVariationView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeProductVariationView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        ProductVariationFormSet = inlineformset_factory(
            Product, Product.variation.through, fk_name='main',
            form=ProductVariationForm,
            can_delete=True,
            formset=VariationInlineFormSet, extra=1,
            max_num=20, validate_max=True)
        if self.object:
            prdvar_formset = ProductVariationFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdvars_formset': prdvar_formset})
        
        context.update({
            'messages': alert,})
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
                    if slug == 'vars':
                        ProductVariationFormSet = inlineformset_factory(
                            Product, Product.variation.through, fk_name='main',
                            form=ProductVariationForm,
                            can_delete=True,
                            formset=VariationInlineFormSet, extra=1,
                            max_num=20, validate_max=True)
                        formset = ProductVariationFormSet(
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
                                formset.save_m2m()

                            messages.success(
                                self.request,
                                "Product Variation changed Successfully")
                            return HttpResponseRedirect(reverse('console:productvariation-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdvars_formset': formset})
                            messages.error(
                                self.request,
                                "Product Variaiton Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/shop/change_productvariation.html"
                                ], context)
                    
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productvariation-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:productvariation-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()