from django import forms
from shop.models import Keyword, AttributeOptionGroup, AttributeOption, Attribute


class AddKeywordForm(forms.ModelForm):
    
    class Meta:
        model = Keyword
        fields = ['name', 'active']
        
    def __init__(self, *args, **kwargs):
        super(AddKeywordForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique keyword'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

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
    

    def save(self, commit=True):
        keyword = super(AddKeywordForm, self).save(commit=False)
        if commit:
            keyword.save()
        return keyword


class AddAttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = ['name', 'type_service', 'display_name', 'type_attribute', 'required', 'is_visible', 'is_sortable', 'is_multiple', 'is_searchable', 'is_comparable', 'is_filterable', 'is_indexable', 'active', 'option_group']

    def __init__(self, *args, **kwargs):
        super(AddAttributeForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['type_attribute'].widget.attrs['class'] = form_class

        self.fields['type_service'].widget.attrs['class'] = form_class
        self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['option_group'].widget.attrs['class'] = form_class
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['required'].widget.attrs['class'] = 'js-switch'
        self.fields['required'].widget.attrs['data-switchery'] = 'true'
        
        self.fields['is_sortable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_sortable'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_indexable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_indexable'].widget.attrs['data-switchery'] = 'true'
        self.fields['is_visible'].widget.attrs['class'] = 'js-switch'
        self.fields['is_visible'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_multiple'].widget.attrs['class'] = 'js-switch'
        self.fields['is_multiple'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_searchable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_searchable'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_filterable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_filterable'].widget.attrs['data-switchery'] = 'true'

        self.fields['is_comparable'].widget.attrs['class'] = 'js-switch'
        self.fields['is_comparable'].widget.attrs['data-switchery'] = 'true'


        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add attribute name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        self.fields['display_name'].widget.attrs['class'] = form_class
        self.fields['display_name'].widget.attrs['maxlength'] = 80
        self.fields['display_name'].widget.attrs['placeholder'] = 'Add display name'
        self.fields['display_name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['display_name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['display_name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['display_name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

    def clean(self):
        super(AddAttributeForm, self).clean()
        if any(self.errors):
            return
        value = self.cleaned_data['type_attribute']
        if value == 6:
            if not self.cleaned_data['option_group']:
                raise forms.ValidationError(
                    'Option Group is required.')
        return

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

    def clean_display_name(self):
        name = self.cleaned_data.get('display_name', '')
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

    def save(self, commit=True):
        attribute = super(AddAttributeForm, self).save(commit=False)
        if commit:
            attribute.save()
        return attribute


class AddAttributeOptionForm(forms.ModelForm):

    class Meta:
        model = AttributeOptionGroup
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddAttributeOptionForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add Option Group Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        


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

    def save(self, commit=True):
        opt_group = super(AddAttributeOptionForm, self).save(commit=False)
        if commit:
            opt_group.save()
        return opt_group
