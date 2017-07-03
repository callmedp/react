from django import forms
from django.utils.translation import ugettext_lazy as _

from shop.models import Category, CategoryRelationship


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
        
        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        # self.fields['image'].widget.attrs['required'] = 'required'
        # self.fields['image'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

    class Meta:
        model = Category
        fields = ('name', 'type_service', 'type_level',
            'banner', 'image')

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
            inst = self.instance
            parent = inst.get_parent()
            childrens = inst.get_childrens()
            if parent:
                raise forms.ValidationError(
                    "You already have parent relation based on current level.")
            if childrens:
                raise forms.ValidationError(
                    "You already have child relation based on current level.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return level

    def clean_banner(self):
        file = self.files.get('banner', '')
        if file:
            if file._size > 100 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 100kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file._size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
            if file.image.height > 125 and file.image.height != file.image.width:
                raise forms.ValidationError("Image not valid. Please upload 125px X 125 px")
        else:
            pass
        return file

    def save(self, commit=True, *args, **kwargs):
        category = super(AddCategoryForm, self).save(
            commit=True, *args, **kwargs)
        category.create_icon()
        return category


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
        
        # self.fields['description'].widget.attrs['class'] = form_class

        self.fields['image'].widget.attrs['class'] = form_class 
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class 
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'


        self.fields['icon'].widget.attrs['class'] = form_class 
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 10
        self.fields['icon'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
    
        self.fields['display_order'].widget.attrs['class'] = form_class
        
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        

    class Meta:
        model = Category
        fields = ('name', 'type_service', 'type_level',
            'banner', 'image', 'icon', 'active', 'display_order')

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
            inst = self.instance
            if inst.type_service != service:
                parent = inst.get_parent()
                childrens = inst.get_childrens()
                if parent:
                    raise forms.ValidationError(
                        "You already have parent relation based on current entity.")
                if childrens:
                    raise forms.ValidationError(
                        "You already have child relation based on current entity.")
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
            inst = self.instance
            if inst.type_level != level: 
                parent = inst.get_parent()
                childrens = inst.get_childrens()
                if parent:
                    raise forms.ValidationError(
                        "You already have parent relation based on current level.")
                if childrens:
                    raise forms.ValidationError(
                        "You already have child relation based on current level.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return level

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file._size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
            if file.image.height > 125 and file.image.height != file.image.width:
                raise forms.ValidationError("Image not valid. Please upload 125px X 125 px")
        else:
            file = self.cleaned_data.get('image')
        return file

    def clean_banner(self):
        file = self.files.get('banner')
        if file:
            if file._size > 100 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 100kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
            if file.image.height > 125 and file.image.height != file.image.width:
                raise forms.ValidationError("Image not valid. Please upload 125px X 125 px")
        else:
            file = self.cleaned_data.get('banner')
        return file

    def clean_icon(self):
        file = self.files.get('icon')
        if file:
            if file._size > 10 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 10kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
            if file.image.height > 125 and file.image.height != file.image.width:
                raise forms.ValidationError("Image not valid. Please upload 125px X 125 px")
        else:
            file = self.cleaned_data.get('icon')
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


class ChangeCategorySkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeCategorySkillForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['is_skill'].widget.attrs['class'] = 'js-switch'
        self.fields['is_skill'].widget.attrs['data-switchery'] = 'true'
        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['graph_image'].widget.attrs['class'] = form_class 
        self.fields['graph_image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['graph_image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        

        self.fields['career_outcomes'].widget.attrs['class'] = 'tagsinput tags form-control'
        self.fields['video_link'].widget.attrs['class'] = form_class
        self.fields['video_link'].widget.attrs['maxlength'] = 80
        self.fields['video_link'].widget.attrs['placeholder'] = 'Add video url'
        self.fields['video_link'].widget.attrs['data-parsley-type'] = 'url'
        self.fields['video_link'].help_text = "Please add Video url without https/http"
        
        self.fields['video_link'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['video_link'].widget.attrs['data-parsley-length'] = "[4, 100]"
        self.fields['video_link'].widget.attrs['data-parsley-length-message'] = 'Length should be between 4-100 characters.'
        
    class Meta:
        model = Category
        fields = (
            'is_skill', 'description', 'video_link',
            'career_outcomes', 'graph_image')

    def clean(self):
        super(ChangeCategorySkillForm, self).clean()
    
    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return desc

    def clean_career_outcomes(self):
        outcome = self.cleaned_data.get('career_outcomes', '')
        if outcome:
            if len(outcome) < 4 or len(outcome) > 400:
                raise forms.ValidationError(
                    "Name should be between 4-400 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return outcome

    def clean_graph_image(self):
        file = self.files.get('graph_image', '')
        if file:
            if file._size > 100 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 100kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_video_link(self):
        link = self.cleaned_data.get('video_link', '')
        if link:
            from django.core.validators import URLValidator
            val = URLValidator()
            val('https://' + link.strip())
        return link

    def save(self, commit=True, *args, **kwargs):

        category = super(ChangeCategorySkillForm, self).save(
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
                qs = qs.filter(type_level=1, type_service=obj.type_service)
            elif obj.type_level == 3:
                qs = qs.filter(type_level=2, type_service=obj.type_service)
            elif obj.type_level == 4:
                qs = qs.filter(type_level=3, type_service=obj.type_service)
            self.fields['related_to'].queryset = qs
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['related_to'].widget.attrs['class'] = form_class
        self.fields['sort_order'].widget.attrs['class'] = form_class

        self.fields['is_main_parent'].widget.attrs['class'] = 'js-switch'
        self.fields['is_main_parent'].widget.attrs['data-switchery'] = 'true'
        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = CategoryRelationship
        fields = (
            'related_from', 'related_to', 'sort_order',
            'is_main_parent', 'active')

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
        parents = []
        main_parent = []
        duplicates = False
        duplicates_main = False

        for form in self.forms:
            if form.cleaned_data:
                parent = form.cleaned_data['related_to']
                is_main = form.cleaned_data['is_main_parent']
                child = form.cleaned_data['related_from']
                
                if parent.type_service != child.type_service:
                    raise forms.ValidationError(
                        'Parent and child should have to same entity',
                        code='diff entity'
                    )

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
        if any(self.errors):
            return
        return

