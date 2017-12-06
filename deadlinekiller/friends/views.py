from django.shortcuts import render
from django.views.generic import ListView

from .models import Connection


class Connections(ListView):
	model = Connection
	template_name = 'friends/connections_list.html'
	context_object_name = 'connections'
