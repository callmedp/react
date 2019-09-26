from django import forms
# from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Tag, Category, Blog, Comment, Author, SITE_TYPE
from blog.config import STATUS
from .decorators import (
    has_group,)


User = get_user_model()


class ArticleAddForm(forms.ModelForm):

    name = forms.CharField(
        label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    visibility = forms.ChoiceField(
        label=("Visibility*:"),
        choices=SITE_TYPE, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.ImageField(
        label=("Image*:"), max_length=200,
        help_text='max size 100kb.',
        widget=forms.FileInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image_alt = forms.CharField(
        label=("Image Alt*:"), max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    content = forms.CharField(
        label=("Content*:"),
        widget=CKEditorUploadingWidget())

    p_cat = forms.ModelChoiceField(
        label=("Primary Category*:"),
        queryset=Category.objects.filter(is_active=True),
        empty_label="Select Category", required=True,
        to_field_name='pk', widget=forms.Select(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    sec_cat = forms.ModelMultipleChoiceField(
        label=("Secondary Category:"),
        queryset=Category.objects.filter(is_active=True),
        to_field_name='name', widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    tags = forms.ModelMultipleChoiceField(
        label=("Tags:"),
        queryset=Tag.objects.filter(is_active=True),
        to_field_name='name', widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    # sites = forms.ModelMultipleChoiceField(label=("Sites:"),
    #     queryset=Site.objects.all(), widget=forms.SelectMultiple(
    #     attrs={'class': 'form-control col-md-7 col-xs-12'}))

    allow_comment = forms.BooleanField(
        label=("Allow Comment:"),
        required=False, widget=forms.CheckboxInput())

    author = forms.ModelChoiceField(
        label=("Writer*:"),
        queryset=Author.objects.filter(is_active=True),
        empty_label="Select Writer", required=True,
        to_field_name='pk', widget=forms.Select(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['name', 'visibility', 'image', 'image_alt', 'p_cat', 'content', 'sec_cat', 'tags', 'allow_comment','author']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ArticleAddForm, self).__init__(*args, **kwargs)
        visibility = []
        site_type = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
            site_type.append((1, "ShineLearning"))
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
            site_type.append((2, "TalentEconomy"))
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)
            site_type.append((3, "HR Blogger"))
            site_type.append((4, 'HR-Conclave'))
            site_type.append((5, 'HR-Jobfair'))
        self.fields['p_cat'].queryset = Category.objects.filter(
            is_active=True,
            visibility__in=visibility)
        self.fields['sec_cat'].queryset = Category.objects.filter(
            is_active=True,
            visibility__in=visibility)
        self.fields['tags'].queryset = Tag.objects.filter(
            is_active=True)
        self.fields['author'].queryset = Author.objects.filter(
            is_active=True)
        self.fields['visibility'].choices = site_type
        self.fields['tags'].required = False
        self.fields['sec_cat'].required = False
        self.fields['content'].required = True

    def clean_image(self):
        img_obj = self.cleaned_data.get('image')
        if img_obj:
            img_size = img_obj._size
            if img_size > 100 * 1024:
                raise forms.ValidationError("Image file too large ( > 100 kb )")
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
        return img_obj


class ArticleChangeForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    status = forms.ChoiceField(
        choices=STATUS, initial=0, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))

    image = forms.ImageField(
        help_text='max size 100kb.',
        label=("Image*:"), max_length=200)

    image_alt = forms.CharField(label=("Image Alt*:"), max_length=100,
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

    # user = forms.ModelChoiceField(label=("Writer:"),
    #     queryset=User.objects.filter(is_active=True, is_staff=True),
    #     empty_label="Select Writer", required=True,
    #     to_field_name='pk', widget=forms.Select(
    #     attrs={'class': 'form-control col-md-7 col-xs-12'}))

    allow_comment = forms.BooleanField(label=("Allow Comment:"),
        required=False, widget=forms.CheckboxInput())

    slug = forms.SlugField(label=("Slug*:"), max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    summary = forms.CharField(label=("Summary:"),
        required=False, widget=forms.Textarea(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    author = forms.ModelChoiceField(label=("Writer:"),
         queryset=Author.objects.filter(is_active=True),
         empty_label="Change Writer", required=True,
         to_field_name='pk', widget=forms.Select(
         attrs={'class': 'form-control col-md-7 col-xs-12'}))

    speakers = forms.ModelMultipleChoiceField(
        label=("Speakers:"),
        queryset=Author.objects.filter(is_active=True),
        to_field_name='name', widget=forms.SelectMultiple(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['name', 'visibility', 'status', 'image', 'image_alt',
            'p_cat', 'content', 'sec_cat', 'tags', 'allow_comment', 'summary',
            'url', 'heading', 'title', 'slug', 'meta_desc', 'meta_keywords',
            'author', 'speakers', 'start_date', 'end_date', 'venue', 'city', 'address', 'sponsor_img']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'heading': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
            'address': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ArticleChangeForm, self).__init__(*args, **kwargs)

        self.required_field = False  # used in clean methods

        visibility = []
        site_type = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
            site_type.append((1, "ShineLearning"))
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
            site_type.append((2, "TalentEconomy"))
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)
            site_type.append((3, "HR Blogger"))
            site_type.append((4, 'HR-Conclave'))
            site_type.append((5, 'HR-Jobfair'))
        self.fields['p_cat'].queryset = Category.objects.filter(
            is_active=True,
            visibility__in=visibility)
        self.fields['sec_cat'].queryset = Category.objects.filter(
            is_active=True,
            visibility__in=visibility)
        self.fields['tags'].queryset = Tag.objects.filter(
            is_active=True)
        self.fields['author'].queryset = Author.objects.filter(
            is_active=True)

        self.fields['speakers'].queryset = Author.objects.filter(
            is_active=True)

        self.fields['visibility'].choices = site_type
        
        self.fields['tags'].required = False
        self.fields['speakers'].required = False
        self.fields['sec_cat'].required = False
        # self.fields['sites'].required = False

        self.fields['heading'].label = 'Heading*'
        self.fields['heading'].required = True

        self.fields['content'].required = True

        self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['image'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        # self.fields['start_date'].widget.attrs['readonly'] = True
        self.fields['start_date'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12 date form_datetime'
        self.fields['start_date'].help_text = 'conclave or jobfair start date'
        # self.fields['end_date'].widget.attrs['readonly'] = True
        self.fields['end_date'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12 date form_datetime'
        self.fields['end_date'].help_text = 'conclave or jobfair end date'
        self.fields['venue'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['city'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['sponsor_img'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

        self.fields['url'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        blog = super(ArticleChangeForm, self).save(commit=False)
        if self.cleaned_data.get('status') == '1' and int(self.cleaned_data.get('status')) != self.initial.get('status'):
            blog.publish_date = timezone.now()
        if commit:
            blog.save()
        return blog

    def clean_image(self):
        img_obj = self.cleaned_data.get('image')
        if img_obj:
            if self.instance.image != img_obj:
                img_size = img_obj._size
                if img_size > 100 * 1024:
                    raise forms.ValidationError("Image file too large ( > 100 kb )")
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
        return img_obj

    def clean_speakers(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        speakers = self.cleaned_data.get('speakers', None)
        if visibility == 4 and not speakers:
            messages.add_message(
                self.request, messages.ERROR, 'Speakers are required.')
            raise forms.ValidationError("Speakers are required.")
        return speakers

    def clean_start_date(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        start_date = self.cleaned_data.get('start_date', None)
        if visibility in [4, 5] and not start_date:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("Start date is required.")
        return start_date

    def clean_end_date(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)
        if visibility in [4, 5] and not end_date:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("end date is required.")
        elif visibility in [4, 5] and start_date and end_date and end_date <= start_date:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("select end date greater than start date")
        return end_date

    def clean_venue(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        venue = self.cleaned_data.get('venue', '').strip()
        if visibility in [4, 5] and not venue:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("Venue is required.")
        return venue

    def clean_city(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        city = self.cleaned_data.get('city', '').strip()
        if visibility in [4, 5] and not city:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("City is required.")
        return city

    def clean_address(self):
        visibility = self.cleaned_data.get('visibility', '0')
        visibility = int(visibility)
        address = self.cleaned_data.get('address', '').strip()
        if visibility in [4, 5] and not address:
            if not self.required_field:
                self.required_field = True
                messages.add_message(
                    self.request, messages.ERROR, 'Please fill the required fields.')
            raise forms.ValidationError("Address is required.")
        return address


class TagAddForm(forms.ModelForm):
    name = forms.CharField(label=("Tag*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    # visibility = forms.ChoiceField(label=("Visibility*:"),
    #         choices=SITE_TYPE, widget=forms.Select(attrs={
    #             'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TagAddForm, self).__init__(*args, **kwargs)
        # visibility = []
        # site_type = []
        # if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(1)
        #     site_type.append((1, "ShineLearning"))
        # if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(2)
        #     site_type.append((2, "TalentEconomy"))
        # if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(3)
        #     visibility.append(4)
        #     visibility.append(5)
        #     site_type.append((3, "HR Blogger"))
        #     site_type.append((4, 'HR-Conclave'))
        #     site_type.append((5, 'HR-Jobfair'))

        # self.fields['visibility'].choices = site_type

        # self.fields['visibility'].choices = site_type
        
        self.fields['name'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 2-70 characters.")

        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class TagChangeForm(forms.ModelForm):
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

    # visibility = forms.ChoiceField(label=("Visibility*:"),
    #         choices=SITE_TYPE, widget=forms.Select(attrs={
    #             'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name', 'is_active', 'priority',
            'title', 'slug', 'url', 'meta_desc', 'meta_keywords']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TagChangeForm, self).__init__(*args, **kwargs)
        # visibility = []
        # site_type = []
        # if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(1)
        #     site_type.append((1, "ShineLearning"))
        # if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(2)
        #     site_type.append((2, "TalentEconomy"))
        # if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(3)
        #     visibility.append(4)
        #     visibility.append(5)
        #     site_type.append((3, "HR Blogger"))
        #     site_type.append((4, 'HR-Conclave'))
        #     site_type.append((5, 'HR-Jobfair'))

        # self.fields['visibility'].choices = site_type

        self.fields['slug'].required = False
        self.fields['slug'].widget.attrs['readonly'] = True

        self.fields['title'].required = True
        self.fields['title'].widget.attrs['maxlength'] = 70

        self.fields['url'].widget.attrs['readonly'] = True

        self.fields['is_active'].required = False
        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 2-70 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class CategoryChangeForm(forms.ModelForm):
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

    image = forms.ImageField(
        help_text='max size 50kb.',
        label=("Image:"), max_length=200, required=False)

    image_alt = forms.CharField(label=("Image Alt:"), max_length=100,
        required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Category
        fields = ['name', 'is_active', 'priority', 'image', 'image_alt', 'visibility',
            'title', 'slug', 'url', 'meta_desc', 'meta_keywords']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryChangeForm, self).__init__(*args, **kwargs)
        visibility = []
        site_type = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
            site_type.append((1, "ShineLearning"))
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
            site_type.append((2, "TalentEconomy"))
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)
            site_type.append((3, "HR Blogger"))
            site_type.append((4, 'HR-Conclave'))
            site_type.append((5, 'HR-Jobfair'))
        self.fields['visibility'].choices = site_type
        
        self.fields['slug'].required = False
        self.fields['slug'].widget.attrs['readonly'] = True
        
        self.fields['url'].widget.attrs['readonly'] = True

        self.fields['title'].required = True
        self.fields['title'].widget.attrs['maxlength'] = 70

        self.fields['image'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

        self.fields['is_active'].required = False
        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 2-70 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_image(self):
        img_obj = self.cleaned_data.get('image')
        if img_obj:
            if self.instance.image != img_obj:
                img_size = img_obj._size
                if img_size > 50 * 1024:
                    raise forms.ValidationError("Image file too large ( > 50 kb )")
        return img_obj


class CategoryAddForm(forms.ModelForm):
    name = forms.CharField(label=("Category*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.ImageField(
        help_text='max size 100kb.',
        label=("Image:"), max_length=200, required= False,
        widget=forms.FileInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image_alt = forms.CharField(label=("Image Alt:"), max_length=100, required= False,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Category
        fields = ['name', 'visibility', 'image', 'image_alt']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        visibility = []
        site_type = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
            site_type.append((1, "ShineLearning"))
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
            site_type.append((2, "TalentEconomy"))
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)
            site_type.append((3, "HR Blogger"))
            site_type.append((4, 'HR-Conclave'))
            site_type.append((5, 'HR-Jobfair'))
        self.fields['visibility'].choices = site_type
        
        self.fields['name'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 2-70 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_image(self):
        img_obj = self.cleaned_data.get('image')
        if img_obj:
            img_size = img_obj._size
            if img_size > 50 * 1024:
                raise forms.ValidationError("Image file too large ( > 50 kb )")
            return img_obj
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
            return img_obj


class ArticleFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ArticleFilterForm, self).__init__(*args, **kwargs)
        visibility = [3]
        site_type = [(-1,"----")]
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
            site_type.append((1, "ShineLearning"))
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
            site_type.append((2, "TalentEconomy"))
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)
            site_type.append((3, "HR Blogger"))
            site_type.append((4, 'HR-Conclave'))
            site_type.append((5, 'HR-Jobfair'))
        NEWSTATUS = ((-1, 'Select Status'),) + STATUS

        self.fields['author'] = forms.ModelChoiceField(label=("Writer:"),
            queryset=Author.objects.filter(is_active=True),
            to_field_name='pk',
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))

        self.fields['status'] = forms.ChoiceField(label=("Status:"),
            choices=NEWSTATUS, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

        self.fields['p_cat'] = forms.ModelChoiceField(label=("Category"),
            queryset=Category.objects.filter(is_active=True, visibility__in=visibility),
            to_field_name='pk',
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))
        self.fields['visibility'] = forms.ChoiceField(label=("Visibility"), choices=site_type, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['author', 'status', 'p_cat', 'visibility']


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
            try:
                value = self.cleaned_data.get(field).strip()
                self.cleaned_data[field] = value
            except:
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


class AuthorAddForm(forms.ModelForm):
    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.ImageField(
        help_text='max size 100kb.',
        label=("Image*:"), max_length=200,
        widget=forms.FileInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image_alt = forms.CharField(label=("Image Alt*:"), max_length=100,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    about = forms.CharField(label=("Description*:"),
        widget=CKEditorUploadingWidget())

    designation = forms.CharField(label=("Designation*:"), widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    company = forms.CharField(label=("Company:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    fb_url = forms.CharField(label=("Fb URL:"), required=False,widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    twitter_url = forms.CharField(label=("Twitter URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    linkedin_url = forms.CharField(label=("Linked-In URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    user = forms.ModelChoiceField(label=("Select User*:"),
        queryset=User.objects.filter(is_active=True),
        empty_label="Select User", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    # visibility = forms.ChoiceField(label=("Visibility*:"),
    #     choices=SITE_TYPE, widget=forms.Select(attrs={
    #         'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Author
        fields = ['name', 'image', 'image_alt', 'about', 'designation', 'company', 'fb_url', 'twitter_url','linkedin_url', 'user']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthorAddForm, self).__init__(*args, **kwargs)
        # visibility = []
        # site_type = []
        # if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(1)
        #     site_type.append((1, "ShineLearning"))
        # if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(2)
        #     site_type.append((2, "TalentEconomy"))
        # if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(3)
        #     visibility.append(4)
        #     visibility.append(5)
        #     site_type.append((3, "HR Blogger"))
        #     site_type.append((4, 'HR-Conclave'))
        #     site_type.append((5, 'HR-Jobfair'))
        # self.fields['visibility'].choices = site_type
        

class AuthorChangeForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    is_active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())

    image = forms.ImageField(
        help_text='max size 100kb.',
        label=("Image*:"), max_length=200)

    image_alt = forms.CharField(label=("Image Alt*:"), max_length=100,
        required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))


    # user = forms.ModelChoiceField(label=("Writer:"),
    #     queryset=User.objects.filter(is_active=True, is_staff=True),
    #     empty_label="Select Writer", required=True,
    #     to_field_name='pk', widget=forms.Select(
    #     attrs={'class': 'form-control col-md-7 col-xs-12'}))

    slug = forms.SlugField(label=("Slug*:"), max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    # visibility = forms.ChoiceField(label=("Visibility*:"),
    #         choices=SITE_TYPE, widget=forms.Select(attrs={
    #             'class': 'form-control col-md-7 col-xs-12'}))

    about = forms.CharField(label=("Description*:"),
        widget=CKEditorUploadingWidget())

    designation = forms.CharField(label=("Designation*:"), widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    company = forms.CharField(label=("Company:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    fb_url = forms.CharField(label=("Fb URL:"), required=False,widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    twitter_url = forms.CharField(label=("Twitter URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    linkedin_url = forms.CharField(label=("Linked-In URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    user = forms.ModelChoiceField(label=("Select User*:"),
        queryset=User.objects.filter(is_active=True),
        empty_label="Select User", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Author
        fields = ['name', 'is_active', 'about', 'image', 'image_alt', 'url','slug', 'fb_url','linkedin_url','twitter_url','designation',
                'company', 'meta_desc', 'meta_keywords', 'user']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthorChangeForm, self).__init__(*args, **kwargs)
        # visibility = []
        # site_type = []
        # if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(1)
        #     site_type.append((1, "ShineLearning"))
        # if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(2)
        #     site_type.append((2, "TalentEconomy"))
        # if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(3)
        #     visibility.append(4)
        #     visibility.append(5)
        #     site_type.append((3, "HR Blogger"))
        #     site_type.append((4, 'HR-Conclave'))
        #     site_type.append((5, 'HR-Jobfair'))
        # self.fields['visibility'].choices = site_type
        
        self.fields['slug'].widget.attrs['readonly'] = True

        self.fields['image'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

        self.fields['url'].widget.attrs['readonly'] = True

        self.fields['is_active'].required = False
        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'
