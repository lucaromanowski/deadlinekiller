
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from .forms import TeamCreationForm
from .models import Team
from account.models import Profile


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

	def get_context_data(self, *args, **kwargs):
		context = super(TeamDetailView, self).get_context_data()
		
		# Get all team members
		team = self.get_object()
		team_members = team.profile_set.all()
		context['team_members'] = team_members

		# Search for users who will be added to the team
		query = self.request.GET.get('q')
		if query:
			#Search within connections (search for friends)
			con = self.request.user.profile.get_connections()
			foll = self.request.user.profile.get_followers()
			all_friends = con | foll
			print('all friends: ', str(all_friends))

			#Filter form friends

			# If somebody search for users
			users = all_friends.filter(
										Q(creator__username__icontains=query) | 
										Q(following__username__icontains=query)  
										#Q(email__icontains=query) |
										#Q(first_name__icontains=query) |
										#Q(last_name__icontains=query) | 
										#Q(profile__date_of_birth__icontains=query) 
										).distinct().exclude(pk=self.request.user.pk) # add profile bio lookup in future) 
			

			print('users: ', str(users))
			context['users'] = users
		else:
			# Get all your connections (friends) 
			con = self.request.user.profile.get_connections()
			foll = self.request.user.profile.get_followers()
			all_friends = con | foll
			# Filter out users already in that team






			context['users'] = all_friends

		print('query', str(query))
		print('get_context_data ivoked')
		# show the list of all friends
		return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):
	model = Team
	template_name = 'teams/team_delete.html'
	success_url = reverse_lazy('teams:team_list')





