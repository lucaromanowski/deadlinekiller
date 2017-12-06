from django.contrib.auth.models import User
from django.db import models


class Connection(models.Model):
	 created = models.DateTimeField(auto_now_add=True, editable=False)
	 creator = models.ForeignKey(User, related_name='friendship_creator_set')
	 following = models.ForeignKey(User, related_name='friend_set')
	 accepted = models.BooleanField(default=False)

	 def __str__(self):
	 	return 'Connection between {} and {}'.format(str(creator.username), str(following.username))