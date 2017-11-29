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
		return Team.objects.filter(profile=self.request.user.profile) 


class TeamCreateView(LoginRequiredMixin, CreateView):
	form_class = TeamCreationForm
	template_name = 'teams/team_create.html'


	def form_valid(self, form):
		return super(TeamCreateView, self).form_valid