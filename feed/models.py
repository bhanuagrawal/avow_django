# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import users
from django.utils import timezone

# Create your models here.
class UserPost(models.Model):
	image_url = models.CharField(max_length=200, null=True)
	time = models.DateTimeField(auto_now_add=True)
	show_info = models.BooleanField(default=False)


	class Meta:
		ordering = ('image_url',)
		db_table = "user_post"


class PostReceiver(models.Model):
	post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
	receiver = models.ForeignKey(users.models.Users, on_delete=models.CASCADE)

	class Meta:
		ordering = ('post',)
		db_table = "post_receiver"