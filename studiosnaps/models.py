#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	city = models.CharField(max_length=50)
	happy = models.BooleanField(default=True)

	def __unicode__(self):
		return u"Profile {0}".format(self.user.username)