from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse

from account.models import Profile
from teams.models import Team



class Project(models.Model):
	pass



class Deadline(models.Model):
	'''
	This model represents deadline.
	The focal point of the app.
	'''
	PRIORITIES = (
			('1', 'highest'),
			('2', 'high'),
			('3', 'medium'),
			('4', 'low'),
			('5', 'lowest'),

		)

	name = models.CharField(max_length=80)
	slug = models.SlugField(max_length=80)
	description = models.CharField(max_length=200)
	project = models.ForeignKey(Project, related_name='deadlines', blank=True, null=True)
	author = models.ForeignKey(User, related_name='deadlines', blank=True, null=True)
	deadline_date = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	priority = models.CharField(max_length=80, choices=PRIORITIES, default='3')	

	# M2M
	team = models.ManyToManyField(Team, blank=True, related_name='teams')
	participant = models.ManyToManyField(Profile, blank=True, related_name='participants')


	def __str__(self):
		return '{} created by {}'.format(self.name, self.author)

	def get_absolute_url(self):
		return reverse('deadlines:deadline_detail', args=[self.pk, self.slug])


