from django import forms

from .models import Deadline


class DeadlineForm(forms.ModelForm):

#	def __init__(self, *args, **kwargs):
#		self.user = kwargs.pop('user', None)
#		super(DeadlineForm, self).__init__(*args, **kwargs)
#		print('Form init methd')


	class Meta:
		model = Deadline
		fields = ('name', 'description', 'project', 'deadline_date', 'priority', 'author')