from django import forms
from django.forms import widgets

class WeatherForm(forms.Form):
	city = forms.CharField(required=True, widget=widgets.TextInput(
		attrs={
			"class":"form-control transparent-control",
			"placeholder": "City (e.g. London)"
		}
	))
	period = forms.ChoiceField(
		required=True,
		choices=(
			('today',"Today's Forcast"),
			('week','Five Day Forcast')
		),
		widget=widgets.Select(
			attrs={"class":"form-control transparent-control"}
		)
	)