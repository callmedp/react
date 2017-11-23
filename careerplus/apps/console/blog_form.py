from django import forms
# from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Tag, Category, Blog, Comment, Author, SITE_TYPE
from blog.config import STATUS


User = get_user_model()


class ArticleAddForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.ImageField(label=("Image*:"), max_length=200,
        widget=forms.FileInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image_alt = forms.CharField(label=("Image Alt*:"), max_length=100,
        widget=forms.TextInput(
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

    allow_comment = forms.BooleanField(label=("Allow Comment:"),
        required=False, widget=forms.CheckboxInput())

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    author = forms.ModelChoiceField(label=("Writer*:"),
         queryset=Author.objects.filter(is_active=True),
         empty_label="Select Writer", required=True,
         to_field_name='pk', widget=forms.Select(
         attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['name', 'image', 'image_alt', 'p_cat', 'content', 'sec_cat', 'tags', 'allow_comment','author','visibility']
    
    def __init__(self, *args, **kwargs):
        super(ArticleAddForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.fields['sec_cat'].required = False
        # self.fields['sites'].required = False
        self.fields['content'].required = True


class ArticleChangeForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    status = forms.ChoiceField(
        choices=STATUS, initial=0, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))

    image = forms.ImageField(label=("Image*:"), max_length=200)

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

    class Meta:
        model = Blog
        fields = ['name', 'status', 'image', 'image_alt', 'p_cat', 'content', 'sec_cat', 'tags', 'allow_comment','summary',
            'url', 'heading', 'title', 'slug', 'meta_desc', 'meta_keywords','author','visibility']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'heading': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ArticleChangeForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.fields['sec_cat'].required = False
        # self.fields['sites'].required = False

        self.fields['heading'].label = 'Heading*'
        self.fields['heading'].required = True

        self.fields['content'].required = True

        self.fields['slug'].widget.attrs['readonly'] = True

        self.fields['image'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

        self.fields['url'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        blog = super(ArticleChangeForm, self).save(commit=False)
        if self.cleaned_data.get('status') == '1' and int(self.cleaned_data.get('status')) != self.initial.get('status'):
            blog.publish_date = timezone.now()
        if commit:
            blog.save()
        return blog


class TagAddForm(forms.ModelForm):
    name = forms.CharField(label=("Tag*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))
    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name','visibility' ]

    def __init__(self, *args, **kwargs):
        super(TagAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")

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

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name', 'is_active', 'priority','visibility',
            'title', 'slug', 'url', 'meta_desc', 'meta_keywords']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }

    def __init__(self, *args, **kwargs):
        super(TagChangeForm, self).__init__(*args, **kwargs)
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
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")
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

    image = forms.ImageField(label=("Image:"), max_length=200 , required= False)

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
        super(CategoryChangeForm, self).__init__(*args, **kwargs)
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
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class CategoryAddForm(forms.ModelForm):
    name = forms.CharField(label=("Category*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    image = forms.ImageField(label=("Image:"), max_length=200, required= False,
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
        fields = ['name', 'visibility','image','image_alt']

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


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
        self.fields['visibility'] = forms.ChoiceField(label=("Visibility"), choices=SITE_TYPE, widget=forms.Select(attrs={'class':'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Blog
        fields = ['user', 'status', 'p_cat','visibility']


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

    image = forms.ImageField(label=("Image*:"), max_length=200,
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

    linkedin_url =  forms.CharField(label=("Linked-In URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    user = forms.ModelChoiceField(label=("Select User:"),
        queryset=User.objects.filter(is_active=True),
        empty_label="Select User", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))


    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Author
        fields = ['name', 'image', 'image_alt', 'about','designation','company','fb_url','twitter_url','linkedin_url','visibility']
    
    def __init__(self, *args, **kwargs):
        super(AuthorAddForm, self).__init__(*args, **kwargs)

class AuthorChangeForm(forms.ModelForm):

    name = forms.CharField(label=("Name*:"), required=True, max_length=85,
        help_text='enter name for slug generation.',
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    is_active = forms.BooleanField(label=("Active:"),
        widget=forms.CheckboxInput())

    image = forms.ImageField(label=("Image*:"), max_length=200)

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

    visibility = forms.ChoiceField(label=("Visibility*:"),
            choices=SITE_TYPE, widget=forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12'}))

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

    linkedin_url =  forms.CharField(label=("Linked-In URL:"), required=False, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    user = forms.ModelChoiceField(label=("Select User:"),
        queryset=User.objects.filter(is_active=True),
        empty_label="Select User", required=True,
        to_field_name='pk', widget=forms.Select(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Author
        fields = ['name', 'is_active', 'about','image', 'image_alt', 'url','slug', 'fb_url','linkedin_url','twitter_url','designation',
                'company','meta_desc', 'meta_keywords','visibility']

        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'title': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '100'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '300'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'max_length': '150'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AuthorChangeForm, self).__init__(*args, **kwargs)

        self.fields['slug'].widget.attrs['readonly'] = True

        self.fields['image'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

        self.fields['url'].widget.attrs['readonly'] = True

        self.fields['is_active'].required = False
        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'
