# python imports
import logging

# django imports
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import MultipleChoiceField
# local imports

# inter app imports
from shop.models import (
    Category, CategoryRelationship, Skill, ProductSkill,
    Faculty, SubHeaderCategory, FacultyProduct,
    Product, UniversityCourseDetail,
    UniversityCoursePayment, SubCategory, FunctionalArea, 
    ProductFA, ProductJobTitle,Section,Offer)

from shop.choices import (
    APPLICATION_PROCESS_CHOICES, APPLICATION_PROCESS,
    BENEFITS_CHOICES, BENEFITS, FACULTY_PRINCIPAL,
)
from homepage.models import Testimonial, NavigationSpecialTag
from shop.models import Category

# third party imports
from dal import autocomplete
from core.library.haystack.query import SQS



class TestimonialModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestimonialModelForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['user_name'].widget.attrs['class'] = form_class
        self.fields['user_name'].widget.attrs['required'] = True
        self.fields['user_name'].widget.attrs['maxlength'] = 40
        self.fields['user_name'].label = "Name"
        self.fields['user_name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['user_name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['user_name'].widget.attrs['data-parsley-length'] = "[1, 40]"
        self.fields['user_name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-40 characters.'

        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

        self.fields['designation'].widget.attrs['class'] = form_class
        self.fields['designation'].widget.attrs['maxlength'] = 30
        self.fields['designation'].required = False
        self.fields['designation'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['designation'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['designation'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['company'].widget.attrs['class'] = form_class
        self.fields['company'].widget.attrs['maxlength'] = 30
        self.fields['company'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['company'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['company'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].label = "Review Title"
        self.fields['title'].widget.attrs['maxlength'] = 50
        self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['title'].widget.attrs['data-parsley-length'] = "[1, 50]"
        self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-50 characters.'

        self.fields['review'].widget.attrs['class'] = form_class
        self.fields['review'].widget.attrs['required'] = True
        self.fields['review'].widget.attrs['maxlength'] = 500
        self.fields['review'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['review'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['review'].widget.attrs['data-parsley-length'] = "[1, 500]"
        self.fields['review'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-500 characters.'

        self.fields['is_active'].widget.attrs['class'] = 'js-switch'
        self.fields['is_active'].widget.attrs['data-switchery'] = 'true'
        self.fields['is_active'].label = 'Active'

        self.fields['page'].widget.attrs['class'] = form_class

    class Meta:
        model = Testimonial
        fields = (
            'user_name', 'image',
            'designation', 'company', 'title', 'review',
            'is_active','page')


    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name', '')
        user_name = user_name.strip() if user_name else ''  #remove extra spaces

        if not user_name:
            raise forms.ValidationError(
                "This field is required.")

        if len(user_name) < 1 or len(user_name) > 40:
            raise forms.ValidationError(
                "Name should be between 1-40 characters.")

        return user_name

    def clean_image(self):
        file = self.cleaned_data.get('image', '')
        if file:
            if file.size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.name.split('.')[-1].upper() not in ('BMP', 'PNG', 'JPEG', 'JPG', 'SVG'):
                raise forms.ValidationError(
                    "Unsupported image type. Please upload svg, bmp, png or jpeg")
        return file

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '')
        designation = designation.strip() if designation else '' #remove extra spaces
        if designation and (len(designation) < 1 or len(designation) > 30):
            raise forms.ValidationError(
                "Designation should be between 1-30 characters.")
        return designation

    def clean_company(self):
        company = self.cleaned_data.get('company', '')
        company = company.strip() if company else ''
        if company and (len(company) < 1 or len(company) > 30):
            raise forms.ValidationError(
                "Company should be between 1-30 characters.")
        return company

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        title = title.strip() if title else ''

        if len(title) > 50:
            raise forms.ValidationError(
                "Title should be between 1-50 characters.")
        return title

    def clean_review(self):
        review = self.cleaned_data.get('review', '')
        review = review.strip() if review else ''

        if not review:
            raise forms.ValidationError(
                "This field is required.")
        if len(review) < 1 or len(review) > 400:
            raise forms.ValidationError(
                "Review should be between 1-400 characters.")
        return review

    def clean_page(self):
        level = self.cleaned_data.get('page', '')
        if level:
            if int(level) == 0:
                raise forms.ValidationError(
                    "This should not be default.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return level



class FacultyCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(FacultyCourseForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        # for university product add filter type_flow university product
        queryset = Product.objects.filter(
            type_flow=14, active=True,
            type_product__in=[0, 1, 3, 5])
        excludes = obj.facultyproducts.all()
        if self.instance and self.instance.pk:
            excludes = excludes.exclude(pk=self.instance.pk)
        courses = list(excludes.values_list(
            'product_id', flat=True))
        queryset = queryset.exclude(pk__in=courses)

        self.fields['product'].queryset = queryset
        self.fields['product'].label = 'Course'
        self.fields['product'].widget.attrs['class'] = form_class
        self.fields['product'].required = True

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

        self.fields['display_order'].widget.attrs['class'] = form_class

    class Meta:
        model = FacultyProduct
        fields = ('product', 'display_order', 'active')

    def clean_product(self):
        product = self.cleaned_data.get('product', None)
        if not product:
            raise forms.ValidationError(
                "This field is required.")
        return product


class FacultyCourseInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(FacultyCourseInlineFormSet, self).clean()
        if any(self.errors):
            return
        products = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                product = form.cleaned_data.get('product', None)
                if product in products:
                    duplicates = True
                products.append(product)

                if duplicates:
                    raise forms.ValidationError(
                        'Product must be unique.',
                        code='duplicate_product'
                    )
        return


class SubHeaderCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubHeaderCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['required'] = True
        self.fields['heading'].widget.attrs['maxlength'] = 100
        self.fields['heading'].widget.attrs['placeholder'] = 'Add Sub header'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[1, 100]"
        self.fields['heading'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['heading_choices'].widget.attrs['class'] = form_class
        # self.fields['heading_choices'].widget.attrs['data-parsley-notdefault'] = ''

        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['description'].widget.attrs['data-parsley-trigger'] = 'change'

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['display_order'].widget.attrs['class'] = form_class


    class Meta:
        model = SubHeaderCategory
        fields = (
            'heading', 'description', 'active', 'display_order','heading_choices')

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '').strip()
        if not heading:
            raise forms.ValidationError(
                "This field is required.")
        if len(heading) > 100:
            raise forms.ValidationError(
                "Description should be at most 100 characters.")
        return heading

    # def clean_description(self):
    #     description = self.cleaned_data.get('description', '').strip()
    #     if not description:
    #         raise forms.ValidationError(
    #             "This field is required.")
    #     if len(description) < 1 or len(description) > 100:
    #         raise forms.ValidationError(
    #             "Description should be between 1-100 characters.")
    #     return description



class SubHeaderInlineFormSet(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(SubHeaderInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True

    def clean(self):
        super(SubHeaderInlineFormSet, self).clean()


class ChangeFacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ('name', 'active', 'image',
            'designation', 'description', 'short_desc',
            'faculty_speak', 'institute', 'role', 'url', 'heading',
            'title', 'slug', 'meta_desc', 'meta_keywords',)

    def __init__(self, *args, **kwargs):
        super(ChangeFacultyForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 40
        self.fields['name'].widget.attrs['placeholder'] = 'Add Faculty Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[1, 40]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-40 characters.'

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

        self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['slug'].widget.attrs['class'] = form_class

        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['image'].widget.attrs['data-parsley-imagedimension'] = '209x209'

        self.fields['designation'].widget.attrs['class'] = form_class
        self.fields['designation'].widget.attrs['maxlength'] = 30
        self.fields['designation'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['designation'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['designation'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['designation'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['description'].widget.attrs['maxlength'] = 600
        self.fields['description'].required = True
        self.fields['description'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['description'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['description'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['description'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        self.fields['short_desc'].widget.attrs['class'] = form_class
        self.fields['short_desc'].label = "Short Description"
        self.fields['short_desc'].widget.attrs['maxlength'] = 200
        self.fields['short_desc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['short_desc'].widget.attrs['data-parsley-length'] = "[1, 200]"
        self.fields['short_desc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-200 characters.'

        self.fields['faculty_speak'].widget.attrs['class'] = form_class
        self.fields['faculty_speak'].label = "Faculty Speak"
        self.fields['faculty_speak'].widget.attrs['maxlength'] = 600
        self.fields['faculty_speak'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['faculty_speak'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['faculty_speak'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        queryset = Category.objects.filter(
            active=True, is_university=True)
        self.fields['institute'].widget.attrs['class'] = form_class
        self.fields['institute'].required = True
        self.fields['institute'].queryset = queryset

        self.fields['role'].widget.attrs['class'] = form_class
        self.fields['role'].required = True
        self.fields['role'].widget.attrs['data-parsley-min'] = '1'
        self.fields['role'].widget.attrs['data-parsley-min-message'] = 'This field is required.'
        self.fields['role'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

        self.fields['url'].widget.attrs['class'] = form_class
        self.fields['url'].widget.attrs['readonly'] = True

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].label = 'Heading'
        self.fields['heading'].required = True

        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].required = True

        self.fields['meta_desc'].widget.attrs['class'] = form_class

        self.fields['meta_keywords'].widget.attrs['class'] = form_class

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError(
                "This field is required.")
        if len(name) < 1 or len(name) > 40:
            raise forms.ValidationError(
                "Name should be between 1-40 characters.")
        return name

    def clean_image(self):
        file = self.files.get('image', '')
        if file and file.size > 30 * 1024:
            raise forms.ValidationError(
                "Image file is too large ( > 30kb ).")
        elif file and file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
            raise forms.ValidationError(
                "Unsupported image type. Please upload svg, bmp, png or jpeg")
        elif not file:
            file = self.cleaned_data.get('image')
        return file

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '').strip()
        if not designation:
            raise forms.ValidationError(
                "This field is required.")
        if len(designation) < 1 or len(designation) > 30:
            raise forms.ValidationError(
                "Designation should be between 1-30 characters.")
        return designation

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError(
                "This field is required.")
        if len(description) < 1 or len(description) > 600:
            raise forms.ValidationError(
                "Description should be between 1-600 characters.")
        return description

    def clean_short_desc(self):
        short_desc = self.cleaned_data.get('short_desc', '').strip()
        if short_desc and len(short_desc) < 1 or len(short_desc) > 200:
            raise forms.ValidationError(
                "Short Description should be between 1-200 characters.")
        return short_desc

    def clean_faculty_speak(self):
        faculty_speak = self.cleaned_data.get('faculty_speak', '').strip()
        if faculty_speak and len(faculty_speak) < 1 or len(faculty_speak) > 600:
            raise forms.ValidationError(
                "Faculty Speak should be between 1-600 characters.")
        return faculty_speak

    def clean_institute(self):
        institute = self.cleaned_data.get('institute', None)
        if not institute:
            raise forms.ValidationError(
                "This field is required.")
        return institute

    def clean_role(self):
        role = int(self.cleaned_data.get('role', '0'))
        if not role:
            raise forms.ValidationError(
                "This field is required.")
        elif role == FACULTY_PRINCIPAL:
            principals = Faculty.objects.filter(
                role=FACULTY_PRINCIPAL,
                institute=self.clean_institute())
            principals = principals.exclude(pk=self.instance.pk)
            if principals.exists():
                raise forms.ValidationError(
                    "This University has already one principal.")
        return role

    def clean_url(self):
        url = self.cleaned_data.get('url', None)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.url

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '').strip()
        if not heading:
            raise forms.ValidationError(
                "This field is required.")
        if len(heading) < 1 or len(heading) > 40:
            raise forms.ValidationError(
                "Heading should be between 1-40 characters.")
        return heading

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError(
                "This field is required.")
        if len(title) < 1 or len(title) > 100:
            raise forms.ValidationError(
                "Title should be between 1-100 characters.")
        return title


class AddFacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ('name', 'image',
            'designation', 'description', 'short_desc',
            'faculty_speak', 'institute', 'role')

    def __init__(self, *args, **kwargs):
        super(AddFacultyForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 40
        self.fields['name'].required = True
        self.fields['name'].widget.attrs['placeholder'] = 'Add Faculty Name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[1, 40]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-40 characters.'

        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['image'].widget.attrs['data-parsley-imagedimension'] = '209x209'

        self.fields['designation'].widget.attrs['class'] = form_class
        self.fields['designation'].widget.attrs['maxlength'] = 30
        self.fields['designation'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['designation'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['designation'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['designation'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['description'].widget.attrs['maxlength'] = 600
        self.fields['description'].required = True
        self.fields['description'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['description'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['description'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['description'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        self.fields['short_desc'].widget.attrs['class'] = form_class
        self.fields['short_desc'].label = "Short Description"
        self.fields['short_desc'].widget.attrs['maxlength'] = 200
        self.fields['short_desc'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['short_desc'].widget.attrs['data-parsley-length'] = "[1, 200]"
        self.fields['short_desc'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-200 characters.'

        self.fields['faculty_speak'].widget.attrs['class'] = form_class
        self.fields['faculty_speak'].label = "Faculty Speak"
        self.fields['faculty_speak'].widget.attrs['maxlength'] = 600
        self.fields['faculty_speak'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['faculty_speak'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['faculty_speak'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        queryset = Category.objects.filter(
            active=True, is_university=True)
        self.fields['institute'].widget.attrs['class'] = form_class
        self.fields['institute'].required = True
        self.fields['institute'].queryset = queryset

        self.fields['role'].widget.attrs['class'] = form_class
        self.fields['role'].required = True
        self.fields['role'].widget.attrs['data-parsley-min'] = '1'
        self.fields['role'].widget.attrs['data-parsley-min-message'] = 'This field is required.'
        self.fields['role'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError(
                "This field is required.")
        if len(name) < 1 or len(name) > 40:
            raise forms.ValidationError(
                "Name should be between 1-40 characters.")
        return name

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '').strip()
        if not designation:
            raise forms.ValidationError(
                "This field is required.")
        if len(designation) < 1 or len(designation) > 30:
            raise forms.ValidationError(
                "Designation should be between 1-30 characters.")
        return designation

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError(
                "This field is required.")
        if len(description) < 1 or len(description) > 600:
            raise forms.ValidationError(
                "Description should be between 1-600 characters.")
        return description

    def clean_short_desc(self):
        short_desc = self.cleaned_data.get('short_desc', '').strip()
        if short_desc and len(short_desc) < 1 or len(short_desc) > 200:
            raise forms.ValidationError(
                "Short Description should be between 1-200 characters.")
        return short_desc

    def clean_faculty_speak(self):
        faculty_speak = self.cleaned_data.get('faculty_speak', '').strip()
        if faculty_speak and len(faculty_speak) < 1 or len(faculty_speak) > 600:
            raise forms.ValidationError(
                "Faculty Speak should be between 1-600 characters.")
        return faculty_speak

    def clean_institute(self):
        institute = self.cleaned_data.get('institute', None)
        if not institute:
            raise forms.ValidationError(
                "This field is required.")
        return institute

    def clean_role(self):
        role = int(self.cleaned_data.get('role', '0'))
        if not role:
            raise forms.ValidationError(
                "This field is required.")
        elif role == FACULTY_PRINCIPAL:
            principals = Faculty.objects.filter(
                role=FACULTY_PRINCIPAL,
                institute=self.clean_institute())
            if principals.exists():
                raise forms.ValidationError(
                    "This University has already one principal.")
        return role

    def clean_image(self):
        file = self.files.get('image', '')
        if file and file.size > 30 * 1024:
            raise forms.ValidationError(
                "Image file is too large ( > 30kb ).")
        if file and file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
            raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        return file


class ProductSkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('object', None)
        super(ProductSkillForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        queryset = Skill.objects.filter(active=True)
        # if self.instance.pk:
        #     self.fields['skill'].queryset = queryset
        # else:
        #     skills = obj.productskills.all().values_list(
        #         'skill_id', flat=True)
        #     queryset = queryset.exclude(pk__in=skills)
        self.fields['skill'].queryset = queryset

        self.fields['skill'].widget.attrs['class'] = form_class
        self.fields['skill'].required = True

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['priority'].widget.attrs['class'] = form_class

    class Meta:
        model = ProductSkill
        fields = (
            'skill', 'active', 'priority')
        widgets = {
            'skill': autocomplete.ModelSelect2(
                url='console:skill-autocomplete')
        }

    def clean(self):
        super(ProductSkillForm, self).clean()

    def clean_skill(self):
        skill = self.cleaned_data.get('skill', None)
        if skill:
            pass
        else:
            raise forms.ValidationError(
                "This field is required.")
        return skill


class SkillInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(SkillInlineFormSet, self).clean()
        # if any(self.errors):
        #     return
        skills = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                skill = form.cleaned_data.get('skill', None)
                if skill in skills:
                    duplicates = True
                skills.append(skill)

                if duplicates:
                    raise forms.ValidationError(
                        'Skill must be unique.',
                        code='duplicate_skill'
                    )
        return


class SkillAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillAddForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique skill name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[1, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-100 characters.'

    class Meta:
        model = Skill
        fields = ('name', )

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            if len(name) < 1 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 1-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class SkillChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillChangeForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique skill name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[1, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-100 characters.'

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = Skill
        fields = ('name', 'active')

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            if len(name) < 1 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 1-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name


class AddCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['name'].widget.attrs['class'] = form_class
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique category name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['type_level'].widget.attrs['class'] = form_class
        self.fields['type_level'].widget.attrs['data-parsley-notdefault'] = ''
        
        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

    class Meta:
        model = Category
        fields = ('name', 'type_level',
            'banner', 'image')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

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
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
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
        self.fields['name'].widget.attrs['maxlength'] = 100
        self.fields['name'].widget.attrs['placeholder'] = 'Add unique category name'
        self.fields['name'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['name'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['name'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['name'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['type_level'].widget.attrs['class'] = form_class
        self.fields['type_level'].widget.attrs['data-parsley-notdefault'] = ''
        
        # self.fields['description'].widget.attrs['class'] = form_class

        self.fields['image'].widget.attrs['class'] = form_class 
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class 
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

        self.fields['icon'].widget.attrs['class'] = form_class 
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['icon'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
    
        self.fields['display_order'].widget.attrs['class'] = form_class
        
        # self.fields['active'].widget.attrs['class'] = 'js-switch'
        # self.fields['active'].widget.attrs['data-switchery'] = 'true'
        
    class Meta:
        model = Category
        fields = ('name', 'type_level',
            'banner', 'image', 'icon', 'display_order')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name:
            if len(name) < 2 or len(name) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

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
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            file = self.cleaned_data.get('image')
        return file

    def clean_banner(self):
        file = self.files.get('banner')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            file = self.cleaned_data.get('banner')
        return file

    def clean_icon(self):
        file = self.files.get('icon')
        if file:
            if file.size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
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
        self.fields['image_alt'].widget.attrs['maxlength'] = 100
        self.fields['image_alt'].widget.attrs['placeholder'] = 'Add Alt'
        self.fields['image_alt'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['image_alt'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['image_alt'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['image_alt'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].widget.attrs['maxlength'] = 100
        self.fields['title'].widget.attrs['placeholder'] = 'Add unique title'
        self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['title'].widget.attrs['required'] = "required"

        self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['title'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['maxlength'] = 100
        self.fields['heading'].widget.attrs['required'] = "required"
        self.fields['heading'].widget.attrs['placeholder'] = 'Add H1'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['heading'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        self.fields['meta_desc'].widget.attrs['class'] = form_class
        self.fields['meta_keywords'].widget.attrs['class'] = form_class

    class Meta:
        model = Category
        fields = ('title', 'meta_desc', 'meta_keywords',
            'heading', 'image_alt')

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title:
            if len(title) < 2 or len(title) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return title

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '')
        if heading:
            if len(heading) < 2 or len(heading) > 100:
                raise forms.ValidationError(
                    "Name should be between 2-100 characters.")
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

        # self.fields['is_skill'].widget.attrs['class'] = 'js-switch'
        # self.fields['is_skill'].widget.attrs['data-switchery'] = 'true'
        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['graph_image'].widget.attrs['class'] = form_class 
        self.fields['graph_image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['graph_image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['career_outcomes'].widget.attrs['class'] = 'tagsinput tags form-control'
        self.fields['video_link'].widget.attrs['class'] = form_class
        self.fields['video_link'].widget.attrs['maxlength'] = 128
        self.fields['video_link'].widget.attrs['placeholder'] = 'Add video url'
        self.fields['video_link'].widget.attrs['data-parsley-type'] = 'url'
        self.fields['video_link'].help_text = "Please add Video url without https/http"
        
        # self.fields['video_link'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['video_link'].widget.attrs['data-parsley-length'] = "[2, 128]"
        self.fields['video_link'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-128 characters.'



    class Meta:
        model = Category
        fields = (
            'description', 'video_link',
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
            if len(outcome) < 2 or len(outcome) > 400:
                raise forms.ValidationError(
                    "Career Outcomes should be between 2-400 characters.")
        else:
            #Don't raise error for services. Return empty.
            if self.instance and self.instance.is_service: 
                return outcome
            raise forms.ValidationError(
                "This field is required.")
        return outcome

    def clean_graph_image(self):
        file = self.files.get('graph_image', '')
        if file:
            if file.size > 100 * 1024:
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
                qs = qs.filter(type_level=1)
            elif obj.type_level == 3:
                qs = qs.filter(type_level=2)
            elif obj.type_level == 4:
                qs = qs.filter(type_level=3)
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
                
                # if parent.type_service != child.type_service:
                #     raise forms.ValidationError(
                #         'Parent and child should have to same entity',
                #         code='diff entity'
                #     )

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


class UniversityCoursesPaymentInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(UniversityCoursesPaymentInlineFormset, self).clean()
        if any(self.errors):
            return


class UniversityCourseForm(forms.ModelForm):

    batch_launch_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control batch_launch_date',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )
    apply_last_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control apply_last_date',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )

    payment_deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control payment_deadline',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']
    )

    application_process_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=APPLICATION_PROCESS_CHOICES
    )
    selected_process_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )
    benefits_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=BENEFITS_CHOICES
    )
    benefits = forms.CharField(
        required=False
    )
    selected_benefits_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )
    eligibility_criteria = forms.CharField(
        label=("Eligibility Criteria"),
        help_text='semi-colon(;) separated criteria, e.g. Line Managers; Decision Maker; ...', 
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'})
    )
    attendees_criteria_choices = MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    class Meta:
        model = UniversityCourseDetail
        fields = [
            'batch_launch_date', 'apply_last_date',
            'sample_certificate', 'application_process', 'assesment',
            'benefits', 'eligibility_criteria', 'attendees_criteria',
            "payment_deadline", "highlighted_benefits"
        ]

    def __init__(self, *args, **kwargs):
        super(UniversityCourseForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['batch_launch_date'].widget.attrs['required'] = True
        self.fields['apply_last_date'].widget.attrs['required'] = True
        self.fields['sample_certificate'].widget.attrs['required'] = True
        self.fields['assesment'].widget.attrs['required'] = True
        self.fields['assesment'].widget.attrs['class'] = form_class
        self.fields['sample_certificate'].widget.attrs['class'] = form_class
        self.fields['eligibility_criteria'].widget.attrs['class'] = form_class + ' tagsinput tags form-control'
        self.fields['highlighted_benefits'].widget.attrs['required'] = True
        self.fields['highlighted_benefits'].widget.attrs['class'] = form_class +  ' tagsinput tags form-control'
      
        if self.instance.get_application_process:
            self.fields['application_process_choices'].initial = [
                int(k) for k in self.instance.get_application_process
            ]
            self.fields['selected_process_choices'].choices = [
                (int(k), APPLICATION_PROCESS.get(k)[1], APPLICATION_PROCESS.get(k)[0]) for k in self.instance.get_application_process
            ]

        attendees_criteria = self.instance.get_attendees_criteria
        if attendees_criteria and len(attendees_criteria) < 4:
            extra_form = 4 - len(attendees_criteria)
            attendees_criteria.extend([('', '')] * extra_form)
        elif attendees_criteria and len(attendees_criteria) >= 4:
            attendees_criteria.extend([('', '')])
        else:
            attendees_criteria = [('', '')] * 4

        self.fields['attendees_criteria_choices'].choices = attendees_criteria
        self.fields['application_process_choices'].widget.attrs['class'] = form_class
        self.fields['application_process_choices'].widget.attrs['required'] = True
        self.fields['application_process_choices'].widget.attrs['class'] = form_class + ' process_item'

        if self.instance.benefits:
            self.fields['benefits_choices'].initial = [
                int(k) for k in self.instance.get_benefits
            ]
            self.fields['selected_benefits_choices'].choices = [
                (int(k), BENEFITS.get(k)[1], BENEFITS.get(k)[0]) for k in self.instance.get_benefits
            ]

        self.fields['benefits_choices'].widget.attrs['class'] = form_class
        self.fields['benefits_choices'].widget.attrs['required'] = True
        self.fields['benefits_choices'].widget.attrs['class'] = form_class + ' benefit_item'

    def clean_batch_launch_date(self):
        batch_launch_date = self.cleaned_data.get('batch_launch_date', '')
        if batch_launch_date is None:
            raise forms.ValidationError(
                "This value is requred.")
        return batch_launch_date

    def clean_apply_last_date(self):
        apply_last_date = self.cleaned_data.get('apply_last_date', '')
        if apply_last_date is None:
            raise forms.ValidationError(
                "This value is requred.")
        return apply_last_date

    def clean_sample_certificate(self):
        file = self.cleaned_data.get('sample_certificate')
        if file:
            filename = file.name
            if not (filename.endswith('.mp3') or filename.endswith('.jpg') or
                    filename.endswith('.jpeg') or filename.endswith('.pdf') or
                    filename.endswith('.png')):
                raise forms.ValidationError("File is not supported. Please upload jpg, png or pdf file only,")

        return file

    def clean_eligibility_criteria(self):
        eligibility_criteria = self.cleaned_data.get('eligibility_criteria', '')
        if eligibility_criteria is None:
            raise forms.ValidationError(
                "This value is requred.")
        return eligibility_criteria

    def clean_attendees_criteria(self):
        attendees_criteria = self.cleaned_data.get('attendees_criteria', '')

        if not eval(attendees_criteria):
            raise forms.ValidationError(
                "Provide atleast one 'Who should attend?'.")
        return attendees_criteria

    def clean_highlighted_benefits(self):
        highlighted_benefits = self.cleaned_data.get('highlighted_benefits', '')
        if not highlighted_benefits:
            raise forms.ValidationError(
                "Provide Highlighted benefits.")
        return highlighted_benefits


class UniversityCoursePaymentForm(forms.ModelForm):

    last_date_of_payment = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control col-md-7 col-xs-12 last_date_of_payment',
                "readonly": True,
            }, format='%d-%m-%Y'
        ),
        input_formats=['%d-%m-%Y']

    )

    def __init__(self, *args, **kwargs):
        super(UniversityCoursePaymentForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['installment_fee'].widget.attrs['class'] = form_class
        self.fields['installment_fee'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['installment_fee'].widget.attrs['required'] = True
        self.fields['installment_fee'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['last_date_of_payment'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['last_date_of_payment'].widget.attrs['required'] = True

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'

    class Meta:
        model = UniversityCoursePayment
        fields = (
            'installment_fee',
            'last_date_of_payment',
            'active'
        )

    def clean(self):
        super(UniversityCoursePaymentForm, self).clean()

    def clean_installment_fee(self):
        from django.db.models import Sum
        installment_fee = self.cleaned_data.get('installment_fee', '')
        sum_already_present = 0
        if getattr(self.instance.product, 'university_course_payment', None):
            sum_already_present = self.instance.product.university_course_payment.all().aggregate(Sum('installment_fee'))['installment_fee__sum']
        sum_already_present = sum_already_present if sum_already_present else 0
        if not self.instance.id and (installment_fee + sum_already_present > self.instance.product.inr_price):
            raise forms.ValidationError(
                "Total installment cannot be greater than product price.".format(sum_already_present))
        elif self.instance.id:
            if installment_fee + (sum_already_present - self.instance.installment_fee) > self.instance.product.inr_price:
                raise forms.ValidationError(
                    "Total installment cannot be greater than product price.")
        if installment_fee is None:
            raise forms.ValidationError(
                "This value is requred.")
        return installment_fee

    def clean_last_date_of_payment(self):
        last_date_of_payment = self.cleaned_data.get('last_date_of_payment', '')
        if last_date_of_payment is None:
            raise forms.ValidationError(
                "This value is requred.")
        return last_date_of_payment


class AddSubCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSubCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['location'].widget.attrs['class'] = form_class
        query_set = Category.objects.filter(type_level=3,is_skill=True).values_list('id','name')
        self.fields['category'] = forms.TypedChoiceField(choices=query_set)
        self.fields['category'].widget.attrs['class'] = form_class
        self.fields['slug'].widget.attrs['class'] = form_class
        self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['slug'].required = True
        self.fields['slug'].label = "Slug*"
        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        # self.fields['image_alt'].widget.attrs['class'] = form_class
        # self.fields['image_alt'].widget.attrs['maxlength'] = 100
        # self.fields['image_alt'].widget.attrs['placeholder'] = 'Add Alt'
        # self.fields['image_alt'].widget.attrs['data-parsley-trigger'] = 'change'
        # self.fields['image_alt'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        # self.fields['image_alt'].widget.attrs['data-parsley-length'] = "[2, 100]"
        # self.fields['image_alt'].widget.attrs[
        #     'data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        # self.fields['title'].widget.attrs['class'] = form_class
        # self.fields['title'].widget.attrs['maxlength'] = 100
        # self.fields['title'].widget.attrs['placeholder'] = 'Add unique title'
        # self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        # self.fields['title'].widget.attrs['required'] = "required"

        # self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        # self.fields['title'].widget.attrs['data-parsley-length'] = "[2, 100]"
        # self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'

        # self.fields['heading'].widget.attrs['class'] = form_class
        # self.fields['heading'].label = "Heading"
        # self.fields['heading'].widget.attrs['maxlength'] = 100
        # self.fields['heading'].widget.attrs['required'] = "required"
        # self.fields['heading'].widget.attrs['placeholder'] = 'Add Heading'
        # self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        # self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        # self.fields['heading'].widget.attrs['data-parsley-length'] = "[2, 100]"
        # self.fields['heading'].widget.attrs[
        #     'data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        #
        self.fields['products_mapped'].widget.attrs['class'] = form_class
        self.fields['products_mapped'].label = "Products"
        # self.fields['products_mapped'].widget.attrs['placeholder'] = 'Add Products For Mapping'
        prod_objs = Product.objects.filter(is_indexed=True).only('id','name','heading')
        choices = [(p.id, '{0}-{1}'.format(p.heading, p.name),) if p.heading else (p.id,'{}'.format(p.name),) for p in prod_objs]
        self.fields['products_mapped'] = forms.MultipleChoiceField(choices=choices)
        self.fields['products_mapped'].required = False
        self.fields['video_link'].widget.attrs['class'] = form_class
        # self.fields['career_outcomes'].widget.attrs['class'] = form_class
        #
        # self.fields['meta_desc'].widget.attrs['class'] = form_class
        # self.fields['meta_keywords'].widget.attrs['class'] = form_class

    class Meta:
        model = SubCategory
        fields = ('location','category','slug','products_mapped','image','banner','video_link')

    def clean_banner(self):
        file = self.files.get('banner', '')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        if not slug:
            raise forms.ValidationError('Check the slug')
        slug_obj = SubCategory.objects.filter(slug=slug)
        if slug_obj:
            raise forms.ValidationError('Slug Already exist')
        return slug

    def clean_category(self):

        cat_id = self.cleaned_data.get('category','')
        if not cat_id:
            raise forms.ValidationError('Check the Category')
        cat_obj = Category.objects.filter(id=cat_id).first()
        if not cat_obj:
            raise forms.ValidationError('Check the Category')
        return cat_obj

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        return file

    def clean_products_mapped(self):
        prod = self.cleaned_data.get('products_mapped','')
        return prod

    def save(self, commit=True, *args, **kwargs):
        subcategory = super(AddSubCategoryForm, self).save(
            commit=True, *args, **kwargs)
        subcategory.create_icon()
        return subcategory


class ChangeSubCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeSubCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['location'].widget.attrs['class'] = form_class
        query_set = Category.objects.filter(type_level=3,is_skill=True).values_list('id','name')
        self.fields['category'] = forms.TypedChoiceField(choices=query_set)
        self.fields['category'].widget.attrs['class'] = form_class
        self.fields['slug'].widget.attrs['class'] = form_class
        # self.fields['slug'].widget.attrs['readonly'] = True
        self.fields['slug'].required = True
        self.fields['slug'].label = "Slug*"
        self.fields['image'].widget.attrs['class'] = form_class
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 500
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        self.fields['title'].widget.attrs['class'] = form_class
        self.fields['title'].widget.attrs['maxlength'] = 100
        self.fields['title'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['title'].widget.attrs['required'] = "required"
        self.fields['title'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['title'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['title'].widget.attrs['data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].label = "Heading"
        self.fields['heading'].widget.attrs['maxlength'] = 100
        self.fields['heading'].widget.attrs['required'] = "required"
        self.fields['heading'].widget.attrs['placeholder'] = 'Add Heading'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[2, 100]"
        self.fields['heading'].widget.attrs[
            'data-parsley-length-message'] = 'Length should be between 2-100 characters.'
        self.fields['products_mapped'].widget.attrs['class'] = form_class
        self.fields['products_mapped'].label = "Products"
        # self.fields['products_mapped'].widget.attrs['placeholder'] = 'Add Products For Mapping'
        prod_objs = Product.objects.filter(is_indexed=True).only('id','name','heading')
        choices = [(p.id, '{0}-{1}'.format(p.heading, p.name),) if p.heading else (p.id,'{}'.format(p.name),) for p in prod_objs]
        self.fields['products_mapped'] = forms.MultipleChoiceField(choices=choices)
        self.fields['products_mapped'].required = False
        # self.fields['products_mapped'].queryset = prod_obj
        self.fields['video_link'].widget.attrs['class'] = form_class
        self.fields['career_outcomes'].widget.attrs['class'] = 'tagsinput tags form-control'
        self.fields['career_outcomes'].required = True
        self.fields['career_outcomes'].label = "Career Outcome*"
        self.fields['meta_desc'].widget.attrs['class'] = form_class
        self.fields['meta_keywords'].widget.attrs['class'] = form_class

    class Meta:
        model = SubCategory
        exclude = ('url',)

    def clean_banner(self):
        file = self.files.get('banner', '')
        if file:
            if file.size > 500 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 500kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        if not slug:
            raise forms.ValidationError('Check the slug')
        return slug



    def clean_category(self):
        cat_id = self.cleaned_data.get('category','')
        if not cat_id:
            raise forms.ValidationError('Check the Category')
        cat_obj = Category.objects.filter(id=cat_id).first()
        if not cat_obj:
            raise forms.ValidationError('Check the Category')
        return cat_obj

    def clean_products_mapped(self):
        prod = self.cleaned_data.get('products_mapped', '')
        return prod

    def clean_image(self):

        file = self.files.get('image', '')
        if not file:
            return file
        if file.size > 500 * 1024:
            raise forms.ValidationError(
                "Image file is too large ( > 500kb ).")
        if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
            raise forms.ValidationError("Unsupported image type. Please upload svg, bmp, png or jpeg")
        return file

    def save(self, commit=True, *args, **kwargs):
        subcategory = super(ChangeSubCategoryForm, self).save(
            commit=True, *args, **kwargs)
        subcategory.create_icon()
        return subcategory


class FunctionalAreaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FunctionalAreaForm, self).__init__(*args, **kwargs)
        prod_objs = SQS().all().only('id','pNm')
        choices = [
            (p.id, '{}'.format(p.pNm),) for p in prod_objs]
        self.fields['faproducts'] = forms.MultipleChoiceField(choices=choices)

    class Meta:
        model = FunctionalArea
        fields = '__all__'


class FunctionalAreaCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FunctionalAreaCreateForm, self).__init__(*args, **kwargs)
        prod_objs = SQS().all().only('id','pNm')
        choices = [
            (p.id, '{}'.format(p.pNm),) for p in prod_objs]
        self.fields['faproducts'] = forms.MultipleChoiceField(choices=choices)
        self.fields['name'].required=False

    class Meta:
        model = FunctionalArea
        fields = '__all__'


    def clean_active(self):
        return self.cleaned_data.get('active',False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Please Enter the FA name')
        if FunctionalArea.objects.filter(name__iexact=name):
            raise forms.ValidationError('Functional Area with same name {} '
                                        'already exist'.format(name))
        return name

    def save(self, commit=True, *args, **kwargs):
        fa_ids = kwargs.pop('fa_ids')
        f = super(FunctionalAreaCreateForm, self).save(commit=True, *args, **kwargs)
        for fa_id in fa_ids:
            ProductFA.objects.create(fa=f,product_id=fa_id,active=True)
        return f


class ProductJobTitleCreateForm(forms.ModelForm):

    class Meta:
        model = ProductJobTitle
        fields = ['name','product']

    def __init__(self, *args, **kwargs):
        super(ProductJobTitleCreateForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        prod_objs = SQS().all().only('id', 'pNm')
        choices = [
            (p.id, '{}({})'.format(p.pNm,p.id),) for p in prod_objs]
        self.fields['product'] = forms.MultipleChoiceField(choices=choices)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Please Enter the Job Title name')
        if ProductJobTitle.objects.filter(name__iexact=name):
            raise forms.ValidationError('Duplicate Job Title Name {}'.format(
                name))
        return name


class ProductJobTitleChangeForm(forms.ModelForm):

    class Meta:
        model = ProductJobTitle
        fields = ['name','product']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(ProductJobTitleChangeForm,self).__init__(*args,**kwargs)
        if instance:
            self.initial['product'] = list(instance.product.values_list('id',
                                                                          flat=True))
        form_class = 'form-control col-md-7 col-xs-12'
        prod_objs = SQS().all().only('id', 'pNm')
        choices = [
            (p.id, '{}({})'.format(p.pNm,p.id),) for p in prod_objs]
        self.fields['product'] = forms.MultipleChoiceField(choices=choices)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Please Enter the Job Title name')
        prodjt = ProductJobTitle.objects.filter(name__iexact=name).first()
        if prodjt and prodjt.id:
            attr = getattr(self,'instance')
            if not attr:
                raise forms.ValidationError('Duplicate Job Title Name {}'.format(
                name))
            if attr.id != prodjt.id:
                raise forms.ValidationError(
                    'Duplicate Job Title Name {}'.format(
                        name))
        return name



class SectionChangeForm(forms.ModelForm):

    class Meta:
        model = Section
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(SectionChangeForm,self).__init__(*args,**kwargs)
        if instance:
            self.initial['product'] = list(instance.product.values_list('id',
                                                                          flat=True))
        form_class = 'form-control col-md-7 col-xs-12'
        prod_objs = SQS().all().only('id', 'pNm')
        choices = [
            (p.id, '{}({})'.format(p.pNm,p.id),) for p in prod_objs]
        self.fields['product'] = forms.MultipleChoiceField(choices=choices)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Please Enter the Job Title name')
        prodjt = Section.objects.filter(name__iexact=name).first()
        if prodjt and prodjt.id:
            attr = getattr(self,'instance')
            if not attr:
                raise forms.ValidationError('Duplicate Job Title Name {}'.format(
                name))
            if attr.id != prodjt.id:
                raise forms.ValidationError(
                    'Duplicate Job Title Name {}'.format(
                        name))
        return name

class OfferChangeForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(OfferChangeForm, self).__init__(*args,**kwargs)
        if instance:
            self.initial['product'] = list(instance.product.values_list('id',
                                                                          flat=True))
        form_class = 'form-control col-md-7 col-xs-12'
        prod_objs = SQS().all().only('id', 'pNm')
        choices = [
            (p.id, '{}({})'.format(p.pNm,p.id),) for p in prod_objs]
        self.fields['product'] = forms.MultipleChoiceField(choices=choices)

class SpecialTagsForm(forms.ModelForm):

    class Meta:
        model = NavigationSpecialTag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(SpecialTagsForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        skill_page_objs = Category.objects.filter(is_skill=True, active=True)
        choices = [
            (p.url, '{}({})'.format(p.name,p.id),) for p in skill_page_objs]

        self.fields['skill_page_url'] = forms.ChoiceField(choices=choices)