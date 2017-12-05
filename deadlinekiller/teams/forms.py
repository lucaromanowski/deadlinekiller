from django import forms

from .models import Team

class TeamCreationForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('name',)
		