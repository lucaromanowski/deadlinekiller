from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView, DeleteView

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
		# Setting up loggedin user as an team creator
		form.instance.creator = self.request.user
		# Setting up slug field
		form.instance.slug = slugify(form.instance.name)
		return super(TeamCreateView, self).form_valid(form)


class TeamDetailView(LoginRequiredMixin, DetailView):
	model = Team
	template_name = 'teams/team_detail.html'


class TeamDeleteView(LoginRequiredMixin, DeleteView):
	model = Team
	template_name = 'teams/team_delete.html'
	success_url = reverse_lazy('teams:team_list')
