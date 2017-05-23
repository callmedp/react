from django import forms

from blog.models import Tag, Category


class TagAddForm(forms.ModelForm):
    name = forms.CharField(label=("Tag*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Tag
        fields = ['name', ]

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
            # elif Tag.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            #     raise forms.ValidationError(
            #         "%s already exist." % (name))
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

    class Meta:
        model = Category
        fields = ['name', 'is_active', 'priority',
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

        self.fields['is_active'].required = False
        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")
            # elif Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            #     raise forms.ValidationError(
            #         "%s already exist." % (name))
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class CategoryAddForm(forms.ModelForm):
    name = forms.CharField(label=("Category*:"), max_length=70,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Category
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 4 or len(name) > 70:
                raise forms.ValidationError(
                    "Name should be between 4-70 characters.")
            # elif Category.objects.filter(name=name).exists():
            #     raise forms.ValidationError(
            #         "This %s already exist." % (name))

        else:
            raise forms.ValidationError(
                "This field is required.")
        return name
