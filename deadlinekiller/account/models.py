from django.conf import settings
from django.db import models

from teams.models import Team


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	# from Teams app
	team = models.ManyToManyField(Team, blank=True)


	def __str__(self):
		return 'Profile of: {}'.format(self.user.username)

