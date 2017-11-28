from django import forms

from .models import Deadline


class DeadlineForm(forms.ModelForm):
	class Meta:
		model = Deadline
		fields = ('name', 'description', 'project', 'deadline_date', 'priority',)