
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView, DeleteView, View

from .forms import TeamCreationForm
from .models import Team
from account.models import Profile
from friends.models import Connection


class TeamListView(LoginRequiredMixin, ListView):
	model = Team
	context_object_name = 'teams'
	template_name = 'teams/team_list.html'


	def get_queryset(self):
		return Team.objects.filter(creator=self.request.user) 

	def get_context_data(self, *args, **kwargs):
		context = super(TeamListView, self).get_context_data()
		# Get all teams that user.profile is a member of
		teams_of_user = Team.objects.filter(profile=self.request.user.profile)
		# Put teams of user into a context
		context['teams_of_user'] = teams_of_user
		return context


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
			
			# Check if user is a team member allready and remove it from results
			for c in users:
				if c.creator.profile in team_members:
					users = users.exclude(pk=c.pk)

				elif c.following.profile in team_members:
					users = users.exclude(pk=c.pk)
			context['users'] = users
		else:
			# Get all your connections (friends) 
			con = self.request.user.profile.get_connections()
			foll = self.request.user.profile.get_followers()
			# Get all connections together 
			all_friends = con | foll

			# Check if friend is a team member allready and remove it from results
			for c in all_friends:
				if c.creator.profile in team_members:
					all_friends = all_friends.exclude(pk=c.pk)

				elif c.following.profile in team_members:
					all_friends = all_friends.exclude(pk=c.pk)			
			context['users'] = all_friends
		return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):
	model = Team
	template_name = 'teams/team_delete.html'
	success_url = reverse_lazy('teams:team_list')


class AddToTheTeamView(LoginRequiredMixin, View):
	'''
	This view adds a user (his profile) to the team
	and removes it.
	'''

	def post(self, request, *args, **kwargs):
		# Case 1 add team member
		if request.POST.get('status') == 'add':

			# Get a team
			team = get_object_or_404(Team, pk=request.POST.get('team_pk'))
			# Get connection
			connection = get_object_or_404(Connection, pk=request.POST.get('con_pk'))

			# Get user from connection
			creator = connection.creator
			following = connection.following

			# Get user that is not a logged in user
			if creator == request.user:
				new_member = following
			else:
				new_member = creator
			# Add new user profile to the team
			team.profile_set.add(new_member.profile)
			team.save()

		# Case 2 remove team member
		elif request.POST.get('status') == 'remove':
			
			# Get a team
			team = get_object_or_404(Team, pk=request.POST.get('team_pk'))
			
			# Get a profile
			profile = get_object_or_404(Profile, pk=request.POST.get('profile_pk'))
			
			# Remove given profile from the team
			team.profile_set.remove(profile)
		
		return redirect('teams:team_list')








