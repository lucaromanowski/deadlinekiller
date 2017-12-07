from django.contrib.auth.models import User
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
			users = User.objects.filter(username__icontains=query).exclude(pk=self.request.user.pk)
			context['users'] = users		
		return context
