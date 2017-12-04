from django.conf import settings
from django.db import models
from django.urls import reverse


class Team(models.Model):
	name = models.CharField(max_length=80)
	slug = models.SlugField(max_length=80)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teams', blank=True, null=True)


	def __str__(self):
		return self.name


	def get_absolute_url(self):
		return reverse('teams:team_detail', args=[self.pk, self.slug])