from django import forms
from geolocation.models import Country


class StateForm(forms.Form):
	state_choices = [(-1, "Please select your state")]
	try:
		india_obj = Country.objects.filter(name='India', phone='91')[0]
		states = india_obj.state_set.all().order_by('name')
		for st in states:
			state_choices.append((st.id, st.name))
	except:
		pass

	state = forms.ChoiceField(required=True, choices=state_choices, initial=-1,
		widget=forms.Select(attrs={'class': 'form-control'}))
	
	def __init__(self, *args, **kwargs):
		super(StateForm, self).__init__(*args, **kwargs)

	def clean_state(self):
		state = self.cleaned_data.get('state')
		try:
			india_obj = Country.objects.filter(name='India', phone='91')[0]
			india_obj.state_set.get(id=state)
		except:
			raise forms.ValidationError(
				"Please select valid state")
		return state