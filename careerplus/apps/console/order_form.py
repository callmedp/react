from django import forms
from django.contrib.auth import get_user_model

from order.models import OrderItem, Message

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
			if extn not in ['pdf', 'doc', 'docx']:
				raise forms.ValidationError(
					"only pdf, doc and docx formats are allowed.")
			elif resume.size > 500 * 1024:
				raise forms.ValidationError(
					"resume is too large ( > 500kb ).")
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
    	perm = Permission.objects.get(codename='can_assigned_to_writer')
    	users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
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
			if extn not in ['pdf', 'doc', 'docx']:
				raise forms.ValidationError(
					"only pdf, doc and docx formats are allowed.")
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
