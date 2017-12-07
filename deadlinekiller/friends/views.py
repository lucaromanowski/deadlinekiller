from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from .models import Connection 


class Connections(ListView):
	model = Connection
	template_name = 'friends/connections_list.html'
	context_object_name = 'connections'

	def get_context_data(self, **kwargs):
		context = super(Connections, self).get_context_data()
		query = self.request.GET.get("q")
		if query:
			users = User.objects.filter(
										Q(username__icontains=query) | 
										Q(email__icontains=query) |
										Q(first_name__icontains=query) |
										Q(last_name__icontains=query) | 
										Q(profile__date_of_birth__icontains=query) 
										).distinct().exclude(pk=self.request.user.pk) # add profile bio lookup in future
			


			context['users'] = users		
		return context
