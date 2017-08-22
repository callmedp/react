from django import forms
from django.conf import settings
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model
from cart.choices import DELIVERY_TYPE
from order.choices import OI_OPS_STATUS
from shop.models import DeliveryService


User = get_user_model()

from linkedin.models import Draft, Organization, Education

LEVEL = (('', '---------'),(0, 'School'),(1,'College'),)


class DraftForm(forms.ModelForm):
    candidate_name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    headline = forms.CharField(
        label=("Headline*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    summary = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'ckeditor'}))

    profile_photo = forms.CharField(label=("Profile Photo"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    recommendation = forms.CharField(label=("Recommendations"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    follow_company = forms.CharField(label=("Follow companies"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    join_group = forms.CharField(label=("Join Group"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    public_url = forms.CharField(label=("Public Url"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    key_skills = forms.CharField(label=("Key Skills"),
        help_text='comma separated skills, e.g. java, python; ...', 
        max_length=500,
        widget=forms.TextInput(
        attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Draft
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(DraftForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['candidate_name'].required = True
        self.fields['headline'].required = True
        self.fields['summary'].required = True
        self.fields['profile_photo'].required = True
        self.fields['recommendation'].required = True
        self.fields['follow_company'].required = True
        self.fields['join_group'].required = True
        self.fields['public_url'].required = True
        self.fields['key_skills'].required = True

    def clean_candidate_name(self):
        name = self.cleaned_data.get('candidate_name', '')
        if name == '':
            raise forms.ValidationError("This field is required.")
        return name

    def clean_headline(self):
        name = self.cleaned_data.get('headline', '')
        if name == '':
            raise forms.ValidationError("This field1 is required.")
        return name

    def clean_summary(self):
        summary = self.cleaned_data.get('summary', '')
        if summary == '':
            raise forms.ValidationError("This field1 is required.")
        return summary

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo', '')
        if profile_photo == '':
            raise forms.ValidationError("This field1 is required.")
        return profile_photo

    def clean_recommendation(self):
        recommendation = self.cleaned_data.get('recommendation', '')
        if recommendation == '':
            raise forms.ValidationError("This field1 is required.")
        return recommendation

    def clean_follow_company(self):
        follow_company = self.cleaned_data.get('follow_company', '')
        if follow_company == '':
            raise forms.ValidationError("This field1 is required.")
        return follow_company

    def clean_join_group(self):
        join_group = self.cleaned_data.get('join_group', '')
        if join_group == '':
            raise forms.ValidationError("This field1 is required.")
        return join_group

    def clean_public_url(self):
        public_url = self.cleaned_data.get('public_url', '')
        if public_url == '':
            raise forms.ValidationError("This field1 is required.")
        return public_url

    def clean_key_skills(self):
        key_skills = self.cleaned_data.get('key_skills', '')
        if key_skills == '':
            raise forms.ValidationError("This field1 is required.")
        return key_skills

    def save(self, commit=True):
        draft = super(DraftForm, self).save(commit=False)
        if commit:
            draft.save()
        return draft


class OrganizationForm(forms.ModelForm):
    org_name = forms.CharField(label=("Company Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    title = forms.CharField(label=("Title*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    org_desc = forms.CharField(widget=forms.Textarea(attrs={'class':'ckeditor'}))
    
    work_from = forms.DateField(
          widget=forms.DateInput(attrs={'class': 'form-control work_from'}))

    work_to = forms.DateField(
          widget=forms.DateInput(attrs={'class': 'form-control work_to'}))

    org_current = forms.BooleanField(label=("Current Organization"),
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'}),
        initial=False, required=False)

    class Meta:
        model = Organization
        fields = ['org_name', 'title', 'org_desc', 'work_from', 'work_to', 'org_current']

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['org_name'].widget.attrs.update({'required':'required'})
        self.fields['title'].widget.attrs.update({'required':'required'})
        self.fields['org_desc'].widget.attrs.update({'required':'required'})
        self.fields['work_from'].widget.attrs.update({'required':'required'})
        self.fields['work_to'].widget.attrs.update({'required':'required'})
        # self.fields['org_current'].widget.attrs.update({'required':'required'})

    def clean_org_name(self):
        org_name = self.cleaned_data.get('org_name', '')
        if org_name == '':
            raise forms.ValidationError("This field is required.")
        return org_name

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title == '':
            raise forms.ValidationError("This field is required.")
        return title

    def clean_org_desc(self):
        org_desc = self.cleaned_data.get('org_desc', '')
        if org_desc == '':
            raise forms.ValidationError("This field is required.")
        return org_desc

    def clean_work_from(self):
        work_from = self.cleaned_data.get('work_from', '')
        if work_from is None:
            raise forms.ValidationError("This field is required.")
        return work_from

    def clean_work_to(self):
        work_from = self.cleaned_data.get("work_from", '')
        work_to = self.cleaned_data.get('work_to', '')
        if work_to is None:
            raise forms.ValidationError("This field is required.")
        elif work_to < work_from:
            raise forms.ValidationError("End date should be greater than from date.")
        return work_to

    # def clean_org_current(self):
    #     org_current = self.cleaned_data.get('org_current', '')
    #     if org_current is False:
    #         raise forms.ValidationError("This field is required.")
    #     return org_current

    def save(self, commit=True):
        org = super(OrganizationForm, self).save(commit=False)
        if commit:
            org.save()
        return org


class EducationForm(forms.ModelForm):
    school_name = forms.CharField(label=("Name*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    degree = forms.CharField(label=("Degree*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    field = forms.CharField(label=("Field Of Study*:"), max_length=85,
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    level = forms.ChoiceField(choices = LEVEL, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    edu_desc = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'ckeditor'}))
    
    study_from = forms.DateField(
          widget=forms.DateInput(attrs={'class': 'form-control study_from'}))

    study_to = forms.DateField(
          widget=forms.DateInput(attrs={'class': 'form-control study_to'}))

    edu_current = forms.BooleanField(label=("Current Education"),
        widget=forms.CheckboxInput(attrs={'class':'checkbox'}),
        initial=False, required=False)

    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'field', 'level', 'edu_desc', 'study_from', 'study_to', 'edu_current']
        
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['school_name'].widget.attrs.update({'required':'required'})
        self.fields['degree'].widget.attrs.update({'required':'required'})
        self.fields['field'].widget.attrs.update({'required':'required'})
        self.fields['level'].widget.attrs.update({'required':'required'})
        self.fields['edu_desc'].widget.attrs.update({'required':'required'})
        self.fields['study_from'].widget.attrs.update({'required':'required'})
        self.fields['study_to'].widget.attrs.update({'required':'required'})
        # self.fields['edu_current'].widget.attrs.update({'required':'required'})

    def clean_school_name(self):
        school_name = self.cleaned_data.get('school_name', '')
        if school_name == '':
            raise forms.ValidationError("This field is required.")
        return school_name

    def clean_degree(self):
        degree = self.cleaned_data.get('degree', '')
        if degree == '':
            raise forms.ValidationError("This field is required.")
        return degree

    def clean_field(self):
        field = self.cleaned_data.get('field', '')
        if field == '':
            raise forms.ValidationError("This field is required.")
        return field

    def clean_level(self):
        level = self.cleaned_data.get('level', '')
        if level == 'NA':
            raise forms.ValidationError("This field is required.")
        return level

    def clean_edu_desc(self):
        edu_desc = self.cleaned_data.get('edu_desc', '')
        if edu_desc == '':
            raise forms.ValidationError("This field is required.")
        return edu_desc

    def clean_study_from(self):
        study_from = self.cleaned_data.get('study_from', '')
        if study_from is None:
            raise forms.ValidationError("This field is required.")
        return study_from

    def clean_study_to(self):
        study_from = self.cleaned_data.get("study_from", '')
        study_to = self.cleaned_data.get('study_to', '')
        if study_to is None:
            raise forms.ValidationError("This field is required.")
        elif study_to < study_from:
            raise forms.ValidationError("End date should be greater than start date.")
        return study_to

    # def clean_edu_current(self):
    #     edu_current = self.cleaned_data.get('edu_current', '')
    #     if edu_current is False:
    #         raise forms.ValidationError("This field is required.")
    #     return edu_current

    def save(self, commit=True):
        edu = super(EducationForm, self).save(commit=False)
        if commit:
            edu.save()
        return edu


class LinkedinInboxActionForm(forms.Form):
    action = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select Writer",
        to_field_name='pk',
        required=True, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(LinkedinInboxActionForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q
        perm = Permission.objects.get(codename='writer_assignment_linkedin_action')
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        self.fields['action'].required = True
        self.fields['action'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['action'].queryset = users


class LinkedinOIFilterForm(forms.Form):

    writer = forms.ModelChoiceField(
        label=("By Expert:"), required=False,
        queryset=User.objects.none(),
        empty_label="Select Expert",
        to_field_name='pk',
        widget=forms.Select())

    created = forms.CharField(
        label=("Added On:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

    payment_date = forms.CharField(
        label=("Payment Date:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

    # delivery_type = forms.ChoiceField(
    #     label=("Delivery Type:"), choices=[],
    #     required=False,
    #     initial=-1,
    #     widget=forms.Select(
    #         attrs={'class': 'form-control'}))

    delivery_type = forms.ModelChoiceField(
        label=("Delivery Type:"), required=False,
        queryset=DeliveryService.objects.none(),
        empty_label="Select Delivery",
        to_field_name='pk',
        widget=forms.Select())

    modified = forms.CharField(
        label=("Modified On:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

    draft_level = forms.ChoiceField(
        label=("Draft Level:"), choices=[],
        required=False,
        initial=-1,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    oi_status = forms.ChoiceField(
        label=("Op Status:"), choices=[],
        required=False,
        initial=-1,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LinkedinOIFilterForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q

        perm = Permission.objects.get(codename='writer_assignment_linkedin_action')
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        self.fields['writer'].widget.attrs['class'] = 'form-control'
        self.fields['writer'].queryset = users

        delivery_objs = DeliveryService.objects.all()
        self.fields['delivery_type'].widget.attrs['class'] = 'form-control'
        self.fields['delivery_type'].queryset = delivery_objs

        # NEW_DELIVERY_TYPE = ((-1, 'Select Delivery'),) + DELIVERY_TYPE
        # self.fields['delivery_type'].choices = NEW_DELIVERY_TYPE

        NEW_OI_OPS_STATUS = ((-1, 'Select Status'),) + OI_OPS_STATUS
        self.fields['oi_status'].choices = NEW_OI_OPS_STATUS

        draft_choices = [(-1, "Select Draft Level")]
        for i in range(1, settings.DRAFT_MAX_LIMIT + 1):
            if i == settings.DRAFT_MAX_LIMIT:
                level = "Draft Level " + "Final"
            else:
                level = "Draft Level " + str(i)
            draft_choices.append((i, level))

        self.fields['draft_level'].choices = draft_choices

    class Meta:
        fields = ['writer', 'created', 'delivery_type', 'modified', 'draft_level']


class OrganizationInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(OrganizationInlineFormSet, self).clean()
        for form in self.forms:
            form.empty_permitted = False
        
        if any(self.errors):
            return
        return

class EducationInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(EducationInlineFormSet, self).clean()
        for form in self.forms:
            form.empty_permitted = False
        
        if any(self.errors):
            return
        return


class AssignmentInterNationalForm(forms.Form):
    assign_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select User",
        to_field_name='pk',
        required=True, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(AssignmentInterNationalForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q
        perm = Permission.objects.get(codename='international_profile_update_assignee')
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        self.fields['assign_to'].required = True
        self.fields['assign_to'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['assign_to'].queryset = users
