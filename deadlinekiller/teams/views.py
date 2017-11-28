from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from .models import Team


class TeamList(LoginRequiredMixin, ListView):
	model = Team
	queryset = Team.objects.all()
	context_object_name = 'teams'
	template_name = 'teams/team_list.html'