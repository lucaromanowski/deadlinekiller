from django.db import models


class Team(models.Model):
	name = models.CharField(max_length=80)
	slug = models.SlugField(max_length=80)


	def __str__(self):
		return self.name