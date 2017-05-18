from django import forms
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from shop.models import Keyword, AttributeOptionGroup, AttributeOption, Attribute, Product
from partner.models import Vendor
from shop.choices import BG_CHOICES
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
            if attribute.type_attribute != 6:
                attribute.option_group = None
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


class DataColorSelect(forms.widgets.Select):

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        datacolor = option_label
        return format_html('<option value="{0}"{1} data-color="{3}">{2}</option>', option_value, selected_html, force_text(option_label), datacolor)


class DataColorChoiceField(forms.ChoiceField):
    
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = DataColorSelect(attrs={'class': 'form-control col-md-7 col-xs-12 image_bg'})
        super(DataColorChoiceField, self).__init__(*args, **kwargs)



class AddProductForm(forms.ModelForm):

    image_bg = DataColorChoiceField(choices=BG_CHOICES)

    class Meta:
        model = Product
        fields = [
            'name', 'type_service',
            'type_product', 'type_flow',
            'upc', 'image', 'image_bg', 'video_url',
            'about', 'description',
            'buy_shine', 'vendor']

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['type_flow'].widget.attrs['class'] = form_class
        self.fields['type_flow'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['type_service'].widget.attrs['class'] = form_class
        self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''

        self.fields['type_product'].widget.attrs['class'] = form_class
               
        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].empty_label = 'Select Vendor'
        self.fields['vendor'].required = True
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add product name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        self.fields['image'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        

        self.fields['upc'].widget.attrs['class'] = form_class
        
        self.fields['upc'].widget.attrs['maxlength'] = 80
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        
        self.fields['video_url'].widget.attrs['class'] = form_class
        self.fields['video_url'].widget.attrs['maxlength'] = 80
        self.fields['video_url'].widget.attrs['placeholder'] = 'Add video url'
        self.fields['video_url'].widget.attrs['data-parsley-type'] = 'url'
    
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
    
    def clean_type_flow(self):
        flow = self.cleaned_data.get('type_flow', '')
        if flow:
            if int(flow) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return flow

    def clean_upc(self):
        upc = self.cleaned_data.get('upc', '')
        if upc:
            if len(upc) < 4 or len(upc) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    def clean_image_bg(self):
        image_bg = self.cleaned_data.get('image_bg', '')
        if image_bg:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return image_bg

    def clean_video_url(self):
        link = self.cleaned_data.get('video_url', '')
        if link:
            from django.core.validators import URLValidator
            val = URLValidator()
            val('https://' + link.strip())
        else:
            raise forms.ValidationError(
                "This is required.")
        return link

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

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return desc

    def clean_about(self):
        about = self.cleaned_data.get('about', '')
        if about:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return about

    def clean_buy_shine(self):
        buy_shine = self.cleaned_data.get('buy_shine', '')
        if buy_shine:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return buy_shine

    def save(self, commit=True, *args, **kwargs):
        product = super(AddProductForm, self).save(
            commit=True, *args, **kwargs)
        product.create_icon()
        return product



class ChangeProductForm(forms.ModelForm):

    image_bg = DataColorChoiceField(choices=BG_CHOICES)

    class Meta:
        model = Product
        fields = [
            'name', 'type_service',
            'type_product', 'type_flow',
            'upc', 'image', 'image_bg', 'icon', 'banner', 'video_url',
            'about', 'description',
            'buy_shine', 'vendor', 'active']

    def __init__(self, *args, **kwargs):
        super(ChangeProductForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['type_flow'].widget.attrs['class'] = form_class
        self.fields['type_flow'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['type_service'].widget.attrs['class'] = form_class
        self.fields['type_service'].widget.attrs['data-parsley-notdefault'] = ''

        self.fields['type_product'].widget.attrs['class'] = form_class
               
        self.fields['vendor'].widget.attrs['class'] = form_class
        self.fields['vendor'].empty_label = 'Select Vendor'
        self.fields['vendor'].required = True
        
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 80
        self.fields['name'].widget.attrs['placeholder'] = 'Add product name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'

        self.fields['upc'].widget.attrs['class'] = form_class
        
        self.fields['upc'].widget.attrs['maxlength'] = 80
        self.fields['upc'].widget.attrs['placeholder'] = 'Add Universal Product Code'
        self.fields['upc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['upc'].widget.attrs['data-parsley-length'] = "[4, 60]"
        self.fields['upc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-60 characters.'
        
        self.fields['banner'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 300
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'


        self.fields['icon'].widget.attrs['class'] = form_class + ' clearimg'
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['icon'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        # self.fields['image_bg'].widget = DataColorSelect()
        # self.fields['image_bg'].widget.attrs['class'] = form_class
        self.fields['video_url'].widget.attrs['class'] = form_class
        self.fields['video_url'].widget.attrs['maxlength'] = 80
        self.fields['video_url'].widget.attrs['placeholder'] = 'Add video url'
        self.fields['video_url'].widget.attrs['data-parsley-type'] = 'url'
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
    
    def clean_type_flow(self):
        flow = self.cleaned_data.get('type_flow', '')
        if flow:
            if int(flow) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return flow

    def clean_upc(self):
        upc = self.cleaned_data.get('upc', '')
        if upc:
            if len(upc) < 4 or len(upc) > 60:
                raise forms.ValidationError(
                    "Name should be between 4-60 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return upc

    def clean_image_bg(self):
        image_bg = self.cleaned_data.get('image_bg', '')
        if image_bg:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return image_bg

    def clean_video_url(self):
        link = self.cleaned_data.get('video_url', '')
        if link:
            from django.core.validators import URLValidator
            val = URLValidator()
            val('https://' + link.strip())
        else:
            raise forms.ValidationError(
                "This is required.")
        return link

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return desc

    def clean_about(self):
        about = self.cleaned_data.get('about', '')
        if about:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return about

    def clean_buy_shine(self):
        buy_shine = self.cleaned_data.get('buy_shine', '')
        if buy_shine:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return buy_shine

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
        product = super(ChangeProductForm, self).save(
            commit=True, *args, **kwargs)
        if product.image:
            if not product.icon:
                product.create_icon()
        return product


class ChangeProductSEOForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProductSEOForm, self).__init__(*args, **kwargs)
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
        model = Product
        fields = ('title', 'meta_desc', 'meta_keywords', 'heading', 'image_alt')

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
        product = super(ChangeProductSEOForm, self).save(
            commit=True, *args, **kwargs)
        return product


class ChangeProductAttributeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProductAttributeForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['duration_months'].widget.attrs['class'] = form_class
        self.fields['duration_days'].widget.attrs['class'] = form_class
        self.fields['certification'].widget.attrs['class'] = 'js-switch'
        self.fields['certification'].widget.attrs['data-switchery'] = 'true'
        self.fields['requires_delivery'].widget.attrs['class'] = 'js-switch'
        self.fields['requires_delivery'].widget.attrs['data-switchery'] = 'true'
        
        self.fields['course_type'].widget.attrs['class'] = form_class
        self.fields['course_type'].widget.attrs['data-parsley-notdefault'] = ''

        self.fields['study_mode'].widget.attrs['class'] = form_class
        self.fields['study_mode'].widget.attrs['data-parsley-notdefault'] = ''

        self.fields['experience'].widget.attrs['class'] = form_class
        self.fields['study_mode'].widget.attrs['data-parsley-notdefault'] = ''

    class Meta:
        model = Product
        fields = ('duration_months', 'duration_days', 'certification', 'course_type', 'study_mode', 'experience', 'requires_delivery')

    
    def save(self, commit=True, *args, **kwargs):
        product = super(ChangeProductAttributeForm, self).save(
            commit=True, *args, **kwargs)
        return product


class ChangeProductOperationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProductOperationForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['mail_desc'].widget.attrs['class'] = form_class
        self.fields['call_desc'].widget.attrs['class'] = form_class
        self.fields['avg_rating'].widget.attrs['class'] = form_class
        self.fields['no_review'].widget.attrs['class'] = form_class
        self.fields['buy_count'].widget.attrs['class'] = form_class
        self.fields['num_jobs'].widget.attrs['class'] = form_class

    class Meta:
        model = Product
        fields = ('mail_desc', 'call_desc', 'avg_rating', 'no_review', 'buy_count', 'num_jobs',)

    
    def save(self, commit=True, *args, **kwargs):
        product = super(ChangeProductOperationForm, self).save(
            commit=True, *args, **kwargs)
        return product
