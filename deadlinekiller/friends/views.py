from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, View

from .models import Connection 

from account.models import Profile


class Connections(LoginRequiredMixin, ListView):
	model = Connection
	template_name = 'friends/connections_list.html'
	context_object_name = 'connections'

	def get_context_data(self, **kwargs):
		context = super(Connections, self).get_context_data()
		query = self.request.GET.get("q")
		if query:
			# Get potentially new friends
			users = User.objects.filter(
										Q(username__icontains=query) | 
										Q(email__icontains=query) |
										Q(first_name__icontains=query) |
										Q(last_name__icontains=query) | 
										Q(profile__date_of_birth__icontains=query) 
										).distinct().exclude(pk=self.request.user.pk) # add profile bio lookup in future
			

			# Exclude users that are already friends with request.user (We want to see only users that are not our friends yet)
			# Get user onnections
			user_connections = Connection.objects.filter(Q(creator=self.request.user)|
														 Q(following=self.request.user))
			
			# Create list of users from connections
			connected_users = []
			for i in user_connections:
				connected_users.append(i.creator)
				connected_users.append(i.following)
			connected_users = set(connected_users)

			# Remove connected users from users in search results
			for user in connected_users:
				# if user is in connected users, remove it form users
				try:
					# Create new users queryset
					users = users.exclude(username=user.username)
				except:
					continue

			# Put users into the context
			context['users'] = users	

		# Getting friends ( filtering in template - change it)

		# Try to get followers and and connected by Profile methods
		# Connection.creator
		con = self.request.user.profile.get_connections()
		# Connection.following
		foll = self.request.user.profile.get_followers()
	
		# All logged in user connections
		connections = con | foll
		connections = connections.filter(accepted=True)	
		number_of_friends = connections.count()
		connections = connections[0:2]
		

		# Connections
		context['friends'] = connections
		# Number of friends
		context['friends_quantity'] = number_of_friends
		return context


class FriendsListView(LoginRequiredMixin, ListView):
	model = Connection
	template_name = 'friends/friends_list.html'
	context_object_name = 'friends'


	def get_context_data(self, **kwargs):
		context = super(FriendsListView, self).get_context_data()
		# Getting friends ( filtering in template - change it)

		# Try to get followers and and connected by Profile methods
		# Connection.creator
		con = self.request.user.profile.get_connections()
		# Connection.following
		foll = self.request.user.profile.get_followers()

		connections = con | foll
		connections = connections.filter(accepted=True)
		number_of_friends = connections.count()
		context['friends_quantity'] = number_of_friends
		context['friends'] = connections
		return context


class MakeConnectionView(LoginRequiredMixin, View):
	
	def post(self, request,  *args, **kwargs):
		user = User.objects.get(username=request.user)
		following = User.objects.get(username=request.POST['friend'])
		
		# Create new connection
		connection = Connection.objects.create(creator=user, following=following)
		return redirect('friends:connections')


class DeleteConnectionView(LoginRequiredMixin, DeleteView):
	model = Connection
	success_url = reverse_lazy('friends:connections')


class FriendsInvitationsView(LoginRequiredMixin, ListView):
	model = Connection
	template_name = 'friends/invitations_list.html'
	context_object_name = 'invited_friends'


	def get_context_data(self, **kargs):
		context = super(FriendsInvitationsView, self).get_context_data()
		# users i invited
		invited_by_me = self.request.user.profile.get_connections().filter(accepted=False)
		# users inviteted me
		invited_me = self.request.user.profile.get_followers().filter(accepted=False)
		context['invited_by_me'] = invited_by_me
		context['invited_me'] = invited_me


		return context