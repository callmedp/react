from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

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
        return super(self.__class__, self).get(
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
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_queryset(self):
        qs = super(self.__class__, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context


class ChangeCategoryForm(forms.ModelForm):

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
        return category


class ChangeCategoryView(DetailView):
    template_name = 'console/shop/change_category.html'
    model = Category

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(self.__class__, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context




class AddCategoryRelationView(TemplateView):
    pass


class ChangeCategoryRelationView(TemplateView):
    pass


class RemoveCategoryRelationView(TemplateView):
    pass


class ListCategoryRelationView(TemplateView):
    pass
