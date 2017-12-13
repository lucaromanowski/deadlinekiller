from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from .models import Connection 


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
		return context


class MakeConnectionView(LoginRequiredMixin, View):
	
	def post(self, request,  *args, **kwargs):

		user = User.objects.get(username=request.user)
		print('user: ', str(user))
		following = User.objects.get(username=request.POST['friend'])
		print('following: ', str(following))
		
		# Create new connection
		connection = Connection.objects.create(creator=user, following=following)
		print('connection: ', str(connection))
		return redirect('friends:connections')