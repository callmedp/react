from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings

from order.models import OrderItem, Message,Order
from order.choices import STATUS_CHOICES
from shop.models import DeliveryService, JobsLinks, ProductUserProfile
from shop.choices import LINK_STATUS_CHOICES
# from cart.choices import DELIVERY_TYPE
from order.choices import OI_OPS_STATUS
from review.models import Review, STATUS_CHOICES
from django.core.validators import validate_email,validate_integer
from django.core.exceptions import ValidationError

User = get_user_model()


class ResumeUploadForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['oi_resume', ]

    def __init__(self, *args, **kwargs):
        super(ResumeUploadForm, self).__init__(*args, **kwargs)
        self.fields['oi_resume'].required = True

    def clean_oi_resume(self):
        resume = self.files.get('oi_resume', '')
        if not resume:
            raise forms.ValidationError(
                "resume is required.")
        elif resume:
            name = resume.name
            extn = name.split('.')[-1]
            if extn not in ['pdf', 'doc', 'docx','ppt','pptx']:
                raise forms.ValidationError(
                    "only pdf, doc,docx, ppt and pptx formats are allowed.")
            elif resume.size > 5 * 1024 * 10000:
                raise forms.ValidationError(
                    "resume is too large ( > 5 MB ).")
        return resume


class InboxActionForm(forms.Form):
    action = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select Writer",
        to_field_name='pk',
        required=True, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(InboxActionForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q
        perm = Permission.objects.get(codename='writer_inbox_assignee')
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        users = users.filter(is_active=True)
        self.fields['action'].required = True
        self.fields['action'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['action'].queryset = users


class FileUploadForm(forms.Form):
    file = forms.FileField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.files.get('file', '')
        if not file:
            raise forms.ValidationError(
                "file is required.")
        elif file:
            name = file.name
            extn = name.split('.')[-1]
            if extn not in ['pdf', 'doc', 'docx','ppt','pptx','rar','zip']:
                raise forms.ValidationError(
                    "only pdf, doc, docx, rar, zip ppt and pptx formats are allowed.")

            elif file.size > 15 * 1024 * 1000:
                raise forms.ValidationError(
                    "file is too large ( > 15 MB ).")
        return file


class VendorFileUploadForm(forms.Form):
    file = forms.FileField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(VendorFileUploadForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.files.get('file', '')
        if not file:
            raise forms.ValidationError(
                "file is required.")
        elif file:
            name = file.name
            extn = name.split('.')[-1]
            if extn not in ['pdf', 'doc', 'docx', 'png', 'jpg']:
                raise forms.ValidationError(
                    "only pdf, doc, docx, png and jpg formats are allowed.")
            elif file.size > 500 * 1024:
                raise forms.ValidationError(
                    "file is too large ( > 500kb ).")
        return file


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'is_internal']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['message'].required = True
        self.fields['message'].label = 'Message'
        self.fields['message'].widget.attrs['maxlength'] = 255
        self.fields['message'].widget.attrs['rows'] = 5
        self.fields['message'].widget.attrs['cols'] = 50
        self.fields['message'].widget.attrs['width'] = "285px"
        self.fields['message'].widget.attrs['placeholder'] = 'write message here....'

        self.fields['is_internal'].label = 'For Internal Only'
        self.fields['is_internal'].initial = True
        self.fields['is_internal'].help_text = 'For Internal Users Only'


class WaitingForInputForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['waiting_for_input']

    def __init__(self, *args, **kwargs):
        super(WaitingForInputForm, self).__init__(*args, **kwargs)


class OrderFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrderFilterForm, self).__init__(*args, **kwargs)

        NEWSTATUS = ((-1, 'All'),) + STATUS_CHOICES

        writer_choice = [(-1, 'ALL'), (-2, "Assigned"), (-3, 'Not Assigned')]
        writers = User.objects.filter(groups__name__in=settings.WELCOMECALL_GROUP_LIST)
        writer_list = list(writers.all().values_list('pk', 'email'))
        writer_choice += writer_list

        self.fields['status'] = forms.ChoiceField(
            label=("Status:"), choices=NEWSTATUS,
            initial=-1,
            widget=forms.Select(
                attrs={'class': 'form-control'}))

        self.fields['payment_date'] = forms.CharField(
            label=("Payment Date:"),
            initial='',
            widget=forms.TextInput(attrs={
                'class': 'form-control date-range-picker',
                "placeholder": 'from date - to date',
                "readonly": True, }))

        self.fields['created'] = forms.CharField(
            label=("Added On:"),
            initial='',
            widget=forms.TextInput(attrs={
                'class': 'form-control date-range-picker',
                'placeholder': "from date - to date",
                "readonly": True, }))

        self.fields['assigned'] = forms.ChoiceField(
            label=("Assigned"), choices=writer_choice,
            initial=-1,
            widget=forms.Select(
                attrs={'class': 'form-control'}))

    class Meta:
        fields = ['status', 'payment_date', 'created', 'assigned']


class OIFilterForm(forms.Form):

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

    date_placed = forms.CharField(
        label=("Placed Date:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))

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
        queue_name = kwargs.pop('queue_name', None)
        super(OIFilterForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q

        perm = Permission.objects.get(codename='writer_inbox_assignee')
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        users = users.filter(is_active=True)
        self.fields['writer'].widget.attrs['class'] = 'form-control'
        self.fields['writer'].queryset = users
        delivery_objs = DeliveryService.objects.all()
        self.fields['delivery_type'].widget.attrs['class'] = 'form-control'
        self.fields['delivery_type'].queryset = delivery_objs

        # NEW_DELIVERY_TYPE = ((-1, 'Select Delivery'),) + DELIVERY_TYPE
        # self.fields['delivery_type'].choices = NEW_DELIVERY_TYPE

        NEW_OI_OPS_STATUS = ((-1, 'Select Status'),) + OI_OPS_STATUS
        if queue_name == 'queue-whatsappjoblist':
            NEW_OI_OPS_STATUS = (
                (-1, 'Select Status'), (31, 'Pending Links'),
                (32, 'Sent Links'), (4, 'Closed')
            )

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
        fields = ['writer', 'payment_date', 'created', 'delivery_type', 'modified', 'draft_level']


class OIActionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        queue_name = kwargs.pop('queue_name', None)
        super(OIActionForm, self).__init__(*args, **kwargs)

        ACTION_CHOICES = (
            (0, "Select Action"),
        )

        if queue_name == 'midout':
            ACTION_CHOICES += ((-2, "Send Midout Mail"),)
        elif queue_name == 'booster':
            ACTION_CHOICES += (
                (-1, "Export As Csv"),
                (-3, "Send Booster Mail"),
            )
        elif queue_name == 'domesticprofileupdate':
            ACTION_CHOICES += (
                (-4, "Send for approval to ops"),  # send domestic Profile Update for approval
            )
        elif queue_name == 'domesticprofileapproval':
            ACTION_CHOICES += (
                (-5, "Approve Domestic Profile Update"),  # domestic Profile Update approved
                (-6, "Reject Domestic Profile Update"),
            )

        elif queue_name == 'partnerinbox':
            ACTION_CHOICES += (
                (-7, "Keep On Hold"),  # item on hold by vendor
            )

        elif queue_name == 'partnerholdqueue':
            ACTION_CHOICES += (
                (-8, "Unhold"),  # unhold orderitem
            )

        elif queue_name == 'internationalprofileupdate':
            ACTION_CHOICES += (
                (-9, "Send for approval to ops"),  # send international Profile Update for approval
            )

        elif queue_name == 'internationalapproval':
            ACTION_CHOICES += (
                (-10, "Approve International Profile Update"),  # domestic Profile Update approved
                (-11, "Reject International Profile Update"),
            )
        elif queue_name == "queue-whatsappjoblist":
            ACTION_CHOICES += ((-15, "mark closed")), # mark whatsapp jobs inactive

        else:
            ACTION_CHOICES += ((-1, "Export As Csv"),)

        self.fields['action'] = forms.ChoiceField(
            label=("Action:"), choices=ACTION_CHOICES,
            required=True,
            initial=0,
            widget=forms.Select(
                attrs={'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        fields = ['action', ]


class AssignmentActionForm(forms.Form):
    assign_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select User",
        to_field_name='pk',
        required=True, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        queue_name = kwargs.pop('queue_name', None)
        super(AssignmentActionForm, self).__init__(*args, **kwargs)
        from django.contrib.auth.models import Permission
        from django.db.models import Q
        if queue_name == 'allocatedqueue':
            perm = Permission.objects.get(codename='writer_inbox_assignee')
            users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        else:
            perm = Permission.objects.get(codename='domestic_profile_update_assignee')
            users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        users = users.filter(is_active=True)
        self.fields['assign_to'].required = True
        self.fields['assign_to'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['assign_to'].queryset = users


class ReviewActionForm(forms.Form):
    ACTION_STATUS = (
        (-1, "Select Action"),
        (0, "Mark Required Moderation"),
        (1, "Mark Approved"),
        (2, "Mark Rejected"),
    )

    action = forms.ChoiceField(
        choices=ACTION_STATUS, initial=-1, required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))


class ReviewFilterForm(forms.Form):
    FILTER_STATUS = (
        (-1, "Select Action"),
        (0, "Required Moderation"),
        (1, "Approved"),
        (2, "Rejected"),
    )
    filter_status = forms.ChoiceField(
        choices=FILTER_STATUS, initial=-1, required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))

    created = forms.CharField(
        label=("Added On:"), required=False,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control date-range-picker',
            'placeholder': "from date - to date",
            "readonly": True, }))


class ReviewUpdateForm(forms.ModelForm):

    content = forms.CharField(
        label=("Review Content*:"), max_length=1500,
        required=True, widget=forms.Textarea(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=True, widget=forms.Select(attrs={
            'class': 'form-control col-md-7 col-xs-12',
            'required': True}))

    reviewed_item = forms.CharField(
        label=("Product Name*:"), max_length=200,
        required=True, widget=forms.TextInput(
            attrs={'class': 'form-control col-md-7 col-xs-12'}))

    created = forms.CharField(
        label=("Created Date:"), required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-7 col-xs-12'}))

    class Meta:
        model = Review
        exclude = ['extra_content_type', 'extra_object_id', 'extra_item', 'object_id', 'user_name', 'user_id']

    def __init__(self, *args, **kwargs):
        super(ReviewUpdateForm, self).__init__(*args, **kwargs)
        from django.utils.html import strip_tags
        obj = kwargs.get('instance')
        self.initial['content'] = strip_tags(obj.content)
        self.fields['content_type'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.initial['reviewed_item'] = '{}'.format(obj.reviewed_item)
        self.fields['reviewed_item'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.fields['user_email'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'
        self.initial['created'] = obj.created.astimezone().strftime("%b %e %Y %I:%M %p")
        self.fields['average_rating'].widget.attrs['class'] = 'form-control col-md-7 col-xs-12'

class emailupdateform(forms.ModelForm):
        class Meta:
            model = Order
            fields = ('alt_email',)

        def __init__(self, *args, **kwargs):
            super(emailupdateform, self).__init__(*args, **kwargs)
            self.fields['alt_email'].required = True

        def clean(self):
            alt_email = self.cleaned_data['alt_email']
            if alt_email == "":
                raise ValidationError('please Enter the email address')
            else:
                validate_email(alt_email)



class mobileupdateform(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('alt_mobile',)

    def __init__(self, *args, **kwargs):
        super(mobileupdateform, self).__init__(*args, **kwargs)
        self.fields['alt_mobile'].required = True

    def clean(self):
        alt_number = self.cleaned_data['alt_mobile']
        if alt_number == "":
            raise ValidationError("please enter the correct mobile number")
        else:
            validate_integer(alt_number)


class JobLinkForm(forms.ModelForm):

    class Meta:
            model = JobsLinks
            fields = ('company_name', 'location', 'link', 'job_title', 'oi',)

    company_name = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-7 col-xs-12'})
    )
    location = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-7 col-xs-12'})
    )

    link = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-7 col-xs-12'})
    )
    job_title = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-7 col-xs-12'})
    )

    def __init__(self, *args, **kwargs):
        super(JobLinkForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if not self.instance.id:
            self.initial['status'] = ''


class ProductUserProfileForm(forms.ModelForm):

    class Meta:
        model = ProductUserProfile
        fields = (
            'contact_number', 'desired_industry', 'desired_location',
            'desired_position', 'desired_salary', 'current_salary'
        )
    contact_number = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )
    desired_industry = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )
    desired_location = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )
    desired_position = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )
    desired_salary = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )
    current_salary = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-3 col-xs-12'}),
        required=False
    )








