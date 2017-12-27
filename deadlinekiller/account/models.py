from django.conf import settings
from django.db import models
from django.urls import reverse

from friends.models import Connection
from teams.models import Team



class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	# In future (# add profile bio lookup in future in friends app)
	bio = models.TextField(blank=True, null=True)

	# from Teams app
	team = models.ManyToManyField(Team, blank=True)


	def get_connections(self):
		connections = Connection.objects.filter(creator=self.user)
		return connections


	def get_followers(self):
		followers = Connection.objects.filter(following=self.user)
		return followers


	def __str__(self):
		return 'Profile of: {}'.format(self.user.username)

	def get_absolute_url(self):
		return reverse('account:profile', args=[self.pk])

