from django import forms
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from shop.models import (
    Category, CategoryRelationship, Skill, ProductSkill,
    UniversityCourseDetail, UniversityCoursePayment,
    Faculty, Category, SubHeaderCategory
)
from homepage.models import Testimonial
from homepage.config import (
    PAGECHOICES, university_page)


class TestimonialCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TestimonialCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        choice_dict = dict(PAGECHOICES)
        choices = [
            (university_page, choice_dict.get(
            university_page, 'University Page'))]
        self.fields['page'].widget.attrs['class'] = form_class
        self.fields['page'].label = "Page type"
        self.fields['page'].choices = choices
        self.fields['page'].widget.attrs['required'] = True
        self.fields['page'].widget.attrs['maxlength'] = 30
        self.fields['page'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['page'].widget.attrs['data-parsley-required-message'] = 'This field is required.'

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
        self.fields['designation'].widget.attrs['required'] = True
        self.fields['designation'].widget.attrs['maxlength'] = 30
        self.fields['designation'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['designation'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['designation'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['designation'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['company'].widget.attrs['class'] = form_class
        self.fields['company'].widget.attrs['required'] = True
        self.fields['company'].widget.attrs['maxlength'] = 30
        self.fields['company'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['company'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
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
        self.fields['priority'].widget.attrs['class'] = form_class


    class Meta:
        model = Testimonial
        fields = (
            'page', 'user_name', 'image',
            'designation', 'company', 'title', 'review',
            'priority', 'is_active')

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name', '').strip()
        if user_name:
            if len(user_name) < 1 or len(user_name) > 40:
                raise forms.ValidationError(
                    "Name should be between 1-40 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return user_name

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file._size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError(
                    "Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '').strip()
        if designation:
            if len(designation) < 1 or len(designation) > 30:
                raise forms.ValidationError(
                    "Designation should be between 1-30 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return designation

    def clean_company(self):
        company = self.cleaned_data.get('company', '').strip()
        if company:
            if len(company) < 1 or len(company) > 30:
                raise forms.ValidationError(
                    "Company should be between 1-30 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return company

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if title:
            if len(title) < 1 or len(title) > 50:
                raise forms.ValidationError(
                    "Title should be between 1-50 characters.")
        return title

    def clean_review(self):
        review = self.cleaned_data.get('review', '').strip()
        if review:
            if len(review) < 1 or len(review) > 500:
                raise forms.ValidationError(
                    "Review should be between 1-500 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return review


class TestimonialInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(TestimonialInlineFormSet, self).clean()


class SubHeaderCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubHeaderCategoryForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'

        self.fields['heading'].widget.attrs['class'] = form_class
        self.fields['heading'].widget.attrs['required'] = True
        self.fields['heading'].widget.attrs['maxlength'] = 30
        self.fields['heading'].widget.attrs['placeholder'] = 'Add Sub header'
        self.fields['heading'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['heading'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['heading'].widget.attrs['data-parsley-length'] = "[1, 30]"
        self.fields['heading'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-30 characters.'

        self.fields['description'].widget.attrs['class'] = form_class
        self.fields['description'].widget.attrs['required'] = True
        self.fields['description'].widget.attrs['maxlength'] = 100
        self.fields['description'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['description'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['description'].widget.attrs['data-parsley-length'] = "[1, 100]"
        self.fields['description'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-100 characters.'

        self.fields['active'].widget.attrs['class'] = 'js-switch'
        self.fields['active'].widget.attrs['data-switchery'] = 'true'
        self.fields['display_order'].widget.attrs['class'] = form_class


    class Meta:
        model = SubHeaderCategory
        fields = (
            'heading', 'description', 'active', 'display_order')

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if description:
            if len(description) < 1 or len(description) > 100:
                raise forms.ValidationError(
                    "Description should be between 1-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return description



class SubHeaderInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(SubHeaderInlineFormSet, self).clean()


class ChangeFacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ('name', 'active', 'image',
            'designation', 'description', 'short_desc',
            'faculty_speak', 'institute', 'url', 'heading',
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
        self.fields['faculty_speak'].required = True
        self.fields['faculty_speak'].widget.attrs['maxlength'] = 600
        self.fields['faculty_speak'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['faculty_speak'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['faculty_speak'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['faculty_speak'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        queryset = Category.objects.filter(
            active=True, is_skill=True)
        self.fields['institute'].widget.attrs['class'] = form_class
        self.fields['institute'].required = True
        self.fields['institute'].queryset = queryset

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
        if name:
            if len(name) < 1 or len(name) > 40:
                raise forms.ValidationError(
                    "Name should be between 1-40 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_image(self):
        file = self.files.get('image', '')
        if file:
            if file._size > 30 * 1024:
                raise forms.ValidationError(
                    "Image file is too large ( > 30kb ).")
            if file.image.format not in ('BMP', 'PNG', 'JPEG', 'SVG'):
                raise forms.ValidationError(
                    "Unsupported image type. Please upload svg, bmp, png or jpeg")
        else:
            pass
        return file

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '').strip()
        if designation:
            if len(designation) < 1 or len(designation) > 30:
                raise forms.ValidationError(
                    "Designation should be between 1-30 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return designation

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if description:
            if len(description) < 1 or len(description) > 600:
                raise forms.ValidationError(
                    "Description should be between 1-600 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return description

    def clean_short_desc(self):
        short_desc = self.cleaned_data.get('short_desc', '').strip()
        if short_desc:
            if len(short_desc) < 1 or len(short_desc) > 200:
                raise forms.ValidationError(
                    "Short Description should be between 1-200 characters.")
        return short_desc

    def clean_faculty_speak(self):
        faculty_speak = self.cleaned_data.get('faculty_speak', '').strip()
        if faculty_speak:
            if len(faculty_speak) < 1 or len(faculty_speak) > 600:
                raise forms.ValidationError(
                    "Faculty Speak should be between 1-600 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return faculty_speak

    def clean_institute(self):
        institute = self.cleaned_data.get('institute', None)
        if not institute:
            raise forms.ValidationError(
                "This field is required.")
        return institute

    def clean_url(self):
        url = self.cleaned_data.get('url', None)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.url

    def clean_heading(self):
        heading = self.cleaned_data.get('heading', '').strip()
        if heading:
            if len(heading) < 1 or len(heading) > 40:
                raise forms.ValidationError(
                    "Heading should be between 1-40 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return heading

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if title:
            if len(title) < 1 or len(title) > 100:
                raise forms.ValidationError(
                    "Title should be between 1-100 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return title


class AddFacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ('name', 'image',
            'designation', 'description', 'short_desc',
            'faculty_speak', 'institute')

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
        self.fields['faculty_speak'].required = True
        self.fields['faculty_speak'].widget.attrs['maxlength'] = 600
        self.fields['faculty_speak'].widget.attrs['data-parsley-trigger'] = 'change'
        self.fields['faculty_speak'].widget.attrs['data-parsley-required-message'] = 'This field is required.'
        self.fields['faculty_speak'].widget.attrs['data-parsley-length'] = "[1, 600]"
        self.fields['faculty_speak'].widget.attrs['data-parsley-length-message'] = 'Length should be between 1-600 characters.'

        queryset = Category.objects.filter(
            active=True, is_skill=True)
        self.fields['institute'].widget.attrs['class'] = form_class
        self.fields['institute'].required = True
        self.fields['institute'].queryset = queryset

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            if len(name) < 1 or len(name) > 40:
                raise forms.ValidationError(
                    "Name should be between 1-40 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return name

    def clean_designation(self):
        designation = self.cleaned_data.get('designation', '').strip()
        if designation:
            if len(designation) < 1 or len(designation) > 30:
                raise forms.ValidationError(
                    "Designation should be between 1-30 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return designation

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if description:
            if len(description) < 1 or len(description) > 600:
                raise forms.ValidationError(
                    "Description should be between 1-600 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return description

    def clean_short_desc(self):
        short_desc = self.cleaned_data.get('short_desc', '').strip()
        if short_desc:
            if len(short_desc) < 1 or len(short_desc) > 200:
                raise forms.ValidationError(
                    "Short Description should be between 1-200 characters.")
        return short_desc

    def clean_faculty_speak(self):
        faculty_speak = self.cleaned_data.get('faculty_speak', '').strip()
        if faculty_speak:
            if len(faculty_speak) < 1 or len(faculty_speak) > 600:
                raise forms.ValidationError(
                    "Faculty Speak should be between 1-600 characters.")
        else:
            raise forms.ValidationError(
                "This field is required.")
        return faculty_speak

    def clean_institute(self):
        institute = self.cleaned_data.get('institute', None)
        if not institute:
            raise forms.ValidationError(
                "This field is required.")
        return institute

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
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 100
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
        self.fields['image'].widget.attrs['data-parsley-max-file-size'] = 30
        self.fields['image'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'
        
        self.fields['banner'].widget.attrs['class'] = form_class 
        self.fields['banner'].widget.attrs['data-parsley-max-file-size'] = 100
        self.fields['banner'].widget.attrs['data-parsley-filemimetypes'] = 'image/jpeg, image/png, image/jpg, image/svg'

        self.fields['icon'].widget.attrs['class'] = form_class 
        self.fields['icon'].widget.attrs['data-parsley-max-file-size'] = 10
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
            }, format='%m/%d/%Y'
        )
    )
    apply_last_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control apply_last_date',
                "readonly": True,
            }, format='%m/%d/%Y'
        )
    )

    class Meta:
        model = UniversityCourseDetail
        fields = [
            'batch_launch_date', 'apply_last_date',
            'sample_certificate', 'our_importance', 'assesment'
        ]

    def __init__(self, *args, **kwargs):
        super(UniversityCourseForm, self).__init__(*args, **kwargs)
        form_class = 'form-control col-md-7 col-xs-12'
        self.fields['batch_launch_date'].widget.attrs['required'] = True
        self.fields['apply_last_date'].widget.attrs['required'] = True
        self.fields['sample_certificate'].widget.attrs['required'] = True
        self.fields['our_importance'].widget.attrs['required'] = True
        self.fields['assesment'].widget.attrs['required'] = True
        self.fields['sample_certificate'].widget.attrs['class'] = form_class
        self.fields['our_importance'].widget.attrs['class'] = form_class
        self.fields['assesment'].widget.attrs['class'] = form_class

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


class UniversityCoursePaymentForm(forms.ModelForm):

    last_date_of_payment = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control col-md-7 col-xs-12 last_date_of_payment',
                "readonly": True,
            }, format='%m/%d/%Y'
        )
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
        installment_fee = self.cleaned_data.get('installment_fee', '')
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
