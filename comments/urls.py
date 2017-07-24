# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^([0-9]+)$', views.post_display, name='simple-post'),
    url(r'^([0-9]+)/newcomment', views.post_comment, name='new-comment'),
    url(r'^([0-9]+)/removecomment', views.comment_remove, name='delete-comment'),
	url(r'^([0-9]+)/edit', views.edit_post, name='edit-post')
    ]
	
