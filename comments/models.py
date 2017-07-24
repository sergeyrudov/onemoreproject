# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    name = models.CharField('Article', max_length=250)
    text = models.TextField('Full description', max_length=250)


    def __str__(self):
        return '{0} - {1}'.format(self.name, self.text)
		


class Comment(models.Model):
	user = models.ForeignKey(User, null=True)
	text = models.CharField('Name the comment', max_length=250)
	date_created = models.DateTimeField('Date created',auto_now_add = True, auto_created = True)
	post_link = models.ForeignKey(Post)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.text, self.date_created, self.user.username)
		
		
	



