from django import forms
# from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import logging
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Tag, Category, Blog, Comment
from .config import STATUS

User = get_user_model()


class BlogAddForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug:"), max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.FileField(
        help_text='max size 100kb.',
        label=("Image:"), max_length=200, required=False)

    image_alt = forms.CharField(label=("Image Alt:"), max_length=100,
        required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    content = forms.CharField(label=("Content*:"),
        widget=CKEditorUploadingWidget())

    p_cat = forms.ModelChoiceField(label=("Primary Category*:"),
        queryset=Category.objects.filter(is_active=True),
        empty_label="Select Category", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    sec_cat = forms.ModelMultipleChoiceField(label=("Secondary Category:"),
        queryset=Category.objects.filter(is_active=True),
        to_field_name='name', widget=forms.SelectMultiple(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    tags = forms.ModelMultipleChoiceField(label=("Tags:"),
        queryset=Tag.objects.filter(is_active=True),
        to_field_name='name', widget=forms.SelectMultiple(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    # sites = forms.ModelMultipleChoiceField(label=("Sites:"),
    #     queryset=Site.objects.all(), widget=forms.SelectMultiple(
    #     attrs={'class': 'form-control col-md-7 col-xs-12'}))

    user = forms.ModelChoiceField(label=("Writer:"),
        queryset=User.objects.filter(is_active=True, is_staff=True),
        empty_label="Select Writer", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    status = forms.ChoiceField(
        choices=STATUS, initial=0, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))

    allow_comment = forms.BooleanField(label=("Allow Comment:"),
        required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Blog
        fields = ['name', 'slug', 'image', 'image_alt', 'p_cat', 'content', 'sec_cat', 'tags', 'user', 'allow_comment',
            'status', 'url', 'title', 'meta_desc', 'meta_keywords']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BlogAddForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['tags'].required = False
        self.fields['sec_cat'].required = False
        # self.fields['sites'].required = False
        self.fields['content'].required = True
        self.fields['slug'].widget.attrs['readonly'] = True
        # self.fields['slug'].widget.attrs['disabled'] = 'disabled'
        self.fields['url'].widget.attrs['readonly'] = True
        self.fields['image'].widget.attrs['class'] = "form-control col-md-7 col-xs-12"
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

    def clean(self):
        fields = ['name', 'slug']
        for field in fields:
                val = self.cleaned_data.get(field).strip()
                if not val:
                    raise forms.ValidationError("value is empty")
                self.cleaned_data[field] = val
                continue
        status = self.cleaned_data.get('status')

        if status == '1':
            if not self.cleaned_data.get('image'):
                raise forms.ValidationError('Image is reqired',
                    code='image-error', )
            if self.cleaned_data.get('image') and not self.cleaned_data.get('image_alt'):
                raise forms.ValidationError('Image alt is reqired',
                    code='image-alt error', )
        return super(BlogAddForm, self).clean()

    def save(self, commit=True):
        blog = super(BlogAddForm, self).save(commit=False)
        if self.cleaned_data.get('status') == '1' and int(self.cleaned_data.get('status')) != self.initial.get('status'):
            blog.publish_date = timezone.now()
        if commit:
            blog.save()
        return blog


class TagAddForm(forms.ModelForm):
    name = forms.CharField(label=("Tag*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug:"), max_length=80,
        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))

    is_active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())

    priority = forms.IntegerField(label=("Priority:"), initial=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name', 'slug', 'is_active', 'priority', 'url',
            'title', 'meta_desc', 'meta_keywords']

        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }

    def __init__(self, *args, **kwargs):
        super(TagAddForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['is_active'].required = False
        self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['url'].widget.attrs['readonly'] = True

    def clean(self):
        fields_to_clean = ['name', 'slug']
        for field in fields_to_clean:
                value = self.cleaned_data.get(field).strip()
                if not value:
                    raise forms.ValidationError("value is empty")
                self.cleaned_data[field] = value
                continue
        return super(TagAddForm, self).clean()


class CategoryAddForm(forms.ModelForm):
    name = forms.CharField(label=("Category*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug:"), max_length=80,
        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}))

    is_active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())

    priority = forms.IntegerField(label=("Priority:"), initial=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_active', 'priority', 'url',
            'title', 'meta_desc', 'meta_keywords']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['is_active'].required = False
        self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['url'].widget.attrs['readonly'] = True

    def clean(self):
        fields_to_clean = ['name', 'slug']
        for field in fields_to_clean:

                value = self.cleaned_data.get(field).strip()
                if not value:
                    raise forms.ValidationError("value is empty")
                self.cleaned_data[field] = value

                continue
        return super(CategoryAddForm, self).clean()


class ArticleFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleFilterForm, self).__init__(*args, **kwargs)

        qs = User.objects.filter(is_staff=True)
        NEWSTATUS = ((-1, 'Select Status'),) + STATUS

        self.fields['user'] = forms.ModelChoiceField(label=("Writer:"),
            queryset=qs,
            to_field_name='pk',
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))

        self.fields['status'] = forms.ChoiceField(label=("Status:"),
            choices=NEWSTATUS, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

        self.fields['p_cat'] = forms.ModelChoiceField(label=("Category"),
            queryset=Category.objects.all(),
            to_field_name='pk',
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['user', 'status', 'p_cat']


class CommentUpdateForm(forms.ModelForm):

    message = forms.CharField(label=("Message*:"), max_length=200,
        required=True, widget=forms.Textarea(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    is_published = forms.BooleanField(label=("Published:"),
        widget=forms.CheckboxInput())

    is_removed = forms.BooleanField(label=("Removed:"),
        widget=forms.CheckboxInput())

    class Meta:
        model = Comment
        fields = ['message', 'is_published', 'is_removed']

    def __init__(self, *args, **kwargs):
        super(CommentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['is_published'].required = False
        self.fields['is_removed'].required = False

    def clean(self):
        fields_to_clean = ['message', ]
        for field in fields_to_clean:
                value = self.cleaned_data.get(field).strip()
                if not value:
                    raise forms.ValidationError("value is empty")
                self.cleaned_data[field] = value
                continue
        return super(CommentUpdateForm, self).clean()


class CommentActionForm(forms.Form):
    ACTION_STATUS = (
        (0, "Select Action"),
        (1, "Mark Published"),
        (2, "Mark Removed"),
    )

    action = forms.ChoiceField(
        choices=ACTION_STATUS, initial=0, required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))