# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
	name =  models.CharField(max_length=100, null=True)
	username = models.CharField(max_length=100, null=True, unique=True)
	password = models.CharField(max_length=50)
	status = models.CharField(max_length=50, default="active")


	class Meta:
		ordering = ('name',)
		db_table = "users"



class Follow(models.Model):
	user = models.ForeignKey(Users,  on_delete=models.CASCADE)
	following = models.ForeignKey(Users, related_name='user_following',on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)

	def getFollowingUsername(self):
		return self.following.username

	def getUsername(self):
		return self.user.username

		

	class Meta:
		ordering = ('user',)
		db_table = "follow"
		unique_together = ('user', 'following',)


class AndroidDevice(models.Model):
	user = models.ForeignKey(Users,  on_delete=models.CASCADE)
	device_id = models.CharField(max_length=300, null=True)

	class Meta:
		ordering = ('user',)
		db_table = "android_devices"