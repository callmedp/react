from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from collections import OrderedDict
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from shop.models import Category, CategoryRelationship
from .decorators import Decorate, check_permission
from django import forms
from django.utils.translation import ugettext_lazy as _


class AddCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique category name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'


        self.fields['type_service'].widget.attrs['class'] = form_class
        self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''
        

        self.fields['type_level'].widget.attrs['class'] = form_class
        self.fields['type_level'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['description'].widget.attrs['class'] = form_class

        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['image'].widget.attrs['required'] = 'required'
        self.fields['image'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 300
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

    class Meta:
        model = Category
        fields = ('name', 'type_service', 'type_level',
            'description', 'banner', 'image')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_type_service(self):
        service = self.cleaned_data.get('type_service', '')
        if service:
            if int(service) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return service

    def clean_type_level(self):
        level = self.cleaned_data.get('type_level', '')
        if level:
            if int(level) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return level

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file._size > 200 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 200kb ).")
        else:
            raise forms.ValidationError(
                "Could not read the uploaded image.")
        return file

    def save(self, commit=True, *args, **kwargs):
        category = super(AddCategoryForm, self).save(
            commit=True, *args, **kwargs)
        category.create_icon()
        return category


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


@Decorate(check_permission('shop.change_category'))
class ListCategoryView(ListView):
    model = Category
    template_name = 'console/shop/list_category.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ListCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ListCategoryView, self).get(request, args, **kwargs)

    def get_queryset(self):
        qs = super(ListCategoryView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListCategoryView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context


class ChangeCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique category name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'


        self.fields['type_service'].widget.attrs['class'] = form_class
        self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''
        

        self.fields['type_level'].widget.attrs['class'] = form_class
        self.fields['type_level'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['description'].widget.attrs['class'] = form_class

        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 300
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'


        self.fields['icon'].widget.attrs['class'] = form_class
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['icon'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
    
        self.fields['display_order'].widget.attrs['class'] = form_class
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        

    class Meta:
        model = Category
        fields = ('name', 'type_service', 'type_level',
            'description', 'banner', 'image', 'icon', 'active', 'display_order')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_type_service(self):
        service = self.cleaned_data.get('type_service', '')
        if service:
            if int(service) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return service

    def clean_type_level(self):
        level = self.cleaned_data.get('type_level', '')
        if level:
            if int(level) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return level

    def clean_image(self):
        file = self.cleaned_data.get('image')
        if file:
            if file.size > 200 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 200kb ).")
        return file

    def clean_banner(self):
        file = self.cleaned_data.get('banner')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Banner file is too large ( > 500kb ).")
        return file

    def clean_icon(self):
        file = self.cleaned_data.get('icon')
        if file:
            if file.size > 100 * 1024:
                raise forms.ValidationError(
                    "Icon file is too large ( > 100kb ).")
        return file

    def save(self, commit=True, *args, **kwargs):
        category = super(ChangeCategoryForm, self).save(
            commit=True, *args, **kwargs)
        if category.image:
            if not category.icon:
                category.create_icon()
        return category


class ChangeCategorySEOForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeCategorySEOForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['image_alt'].widget.attrs['class'] = form_class
        self.fields['image_alt'].widget.attrs['maxlength'] = 80
        self.fields['image_alt'].widget.attrs['placeholder'] = 'Add Alt'
        self.fields['image_alt'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['image_alt'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['image_alt'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['image_alt'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].widget.attrs['maxlength'] = 80
        self.fields['title'].widget.attrs['placeholder'] = 'Add unique title'
        self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['title'].widget.attrs['required'] = "required"
        
        self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['title'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['maxlength'] = 80
        self.fields['heading'].widget.attrs['required'] = "required"
        self.fields['heading'].widget.attrs['placeholder'] = 'Add H1'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['heading'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'


        self.fields['meta_desc'].widget.attrs['class'] = form_class
        self.fields['meta_keywords'].widget.attrs['class'] = form_class

    class Meta:
        model = Category
        fields = ('title', 'meta_desc', 'meta_keywords',
            'heading', 'image_alt')

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title:
            if len(title) < 4 or len(title) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return title

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '')
        if heading:
            if len(heading) < 4 or len(heading) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

    def save(self, commit=True, *args, **kwargs):
        category = super(ChangeCategorySEOForm, self).save(
            commit=True, *args, **kwargs)
        return category


class CategoryRelationshipForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(CategoryRelationshipForm, self).__init__(*args, **kwargs)
        if obj:
            qs = Category.objects.all()
            if obj.type_level == 0 or obj.type_level == 1:
                qs = qs.none()
            elif obj.type_level == 2:
                qs = qs.filter(type_level=1)
            elif obj.type_level == 3:
                qs = qs.filter(type_level=2)
            elif obj.type_level == 4:
                qs = qs.filter(type_level=3)
            self.fields['related_to'].queryset = qs
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['related_to'].widget.attrs['class'] = form_class
        self.fields['relation'].widget.attrs['class'] = form_class
        self.fields['sort_order'].widget.attrs['class'] = form_class

        self.fields['is_main_parent'].widget.attrs['class'] = 'js-switch'
        self.fields['is_main_parent'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = CategoryRelationship
        fields = (
            'related_from', 'related_to', 'relation', 'sort_order',
            'is_main_parent')

    def clean(self):
        super(CategoryRelationshipForm, self).clean()


    def clean_related_to(self):
        related_to = self.cleaned_data.get('related_to', None)
        if related_to:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return related_to


class RelationshipInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(RelationshipInlineFormSet, self).clean()
        if any(self.errors):
            return 
        parents = []
        main_parent = []
        duplicates = False
        duplicates_main = False

        for form in self.forms:
            if form.cleaned_data:
                parent = form.cleaned_data['related_to']
                is_main = form.cleaned_data['is_main_parent']
                child = form.cleaned_data['related_from']
                if child.type_level == 0 or child.type_level == 1:
                    raise forms.ValidationError(
                        'You cannot make parent of level 1.',
                    )
                elif child.type_level == 2:
                    if parent.type_level == 1:
                        pass
                    else:
                        raise forms.ValidationError(
                            'You can only make level1 parent of level 2.',
                        )
                elif child.type_level == 3:
                    if parent.type_level == 2:
                        pass
                    else:
                        raise forms.ValidationError(
                            'You can only make level2 parent of level 3.',
                        )
                elif child.type_level == 4:
                    if parent.type_level == 3:
                        pass
                    else:
                        raise forms.ValidationError(
                            'You can only make level3 parent of level 4.',
                        )
                if parent in parents:
                    duplicates = True
                parents.append(parent)

                if is_main:
                    if main_parent:
                        duplicates_main = True
                    main_parent.append(parent)

                if duplicates:
                    raise forms.ValidationError(
                        'Relationships must be unique.',
                        code='duplicate_parent'
                    )

                if duplicates_main:
                    raise forms.ValidationError(
                        'Main parent must be Unique',
                        code='double_main'
                    )
        return



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
        if self.object.type_level in [2, 3, 4]:
            relationship_formset = CategoryRelationshipFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'relationship_formset': relationship_formset})
        context.update({
            'messages': alert,
            'form': main_change_form,
            'seo_form': seo_change_form})
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
