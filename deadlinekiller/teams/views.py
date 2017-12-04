from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .forms import TeamCreationForm
from .models import Team


class TeamListView(LoginRequiredMixin, ListView):
	model = Team
	context_object_name = 'teams'
	template_name = 'teams/team_list.html'


	def get_queryset(self):
		return Team.objects.filter(creator=self.request.user) 


class TeamCreateView(LoginRequiredMixin, CreateView):
	form_class = TeamCreationForm
	template_name = 'teams/team_create.html'


	def form_valid(self, form):
		print('form instance: ', str(form.instance))
		form.instance.creator = self.request.user


		#print('form valid ivoked')
		#self.object = form.save(commit=False)
		#print('Self.object: ', str(self.object))
		
		#self.object.user = self.request.user.profile
		#print('Self object user: ', str(self.object.user))
		#form.user = self.request.user.profile
		#self.object.save()
		return super(TeamCreateView, self).form_valid(form)