# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib import messages
# Create your views here.


def post_display(request, id):
    post = Post.objects.get(id=id)
    allpost = Post.objects.all()
    context = {'post': post, 'posts': allpost, 'CommentForm': validate_comment()}
    return render(request, 'comments/TEMPLATE/index.html', context)

def post_comment(request, id):
	form = validate_comment(request.GET)
	if form.is_valid():
		comm = Comment()
		comm.text = form.cleaned_data['text']
		comm.post_link = Post.objects.get(id=id)
		comm.user = request.user
		comm.save()
	return redirect('/posts/{0}'.format(id))


def comment_remove(request, id):
    comment = Comment.objects.get(id=id)
    post_id = comment.post_link.id
    comment.delete()
    return redirect('/posts/{0}'.format(post_id))
	
	
def edit_post(request, id):
	post = Post.objects.get(id=id)
	if request.GET:
	   post.name = request.GET['name']
	   post.text = request.GET['text']
	   post.save()
	   return redirect(reverse('simple-post', args=[post.id]))
	else:
		context = {'PostForm': PostForm(instance=post), 'post' : post}
		return render (request, 'comments/TEMPLATE/editpost.html', context)
		
		
def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	if request.method == 'POST':
		data = request.POST
		try:
			User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
		except IntegrityError: 
			messages.info(request, 'User is already registered.')
			return redirect(reverse('signup'))
		user = authenticate(username=data['username'], password=data['password'])
		login(request, user)
		return redirect(reverse('mainpage'))
	else:
		form = SignupForm()
		context = {'form':form}
	return render(request, 'comments/TEMPLATE/signup.html', context)
		
		
def signin(request):
	if request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(reverse('signin'))
			else:
				return redirect(reverse('profile'))
		else:
			messages.info(request, 'Incorrect login or password')
			return redirect(reverse('signin'))
	if request.method != 'POST':
		form = SigninForm()
		context = {'form':form}
	return render(request, 'comments/TEMPLATE/signin.html', context)
	
	
def profile(request):
	if request.user.is_authenticated():
		context = {}
		return render(request, 'comments/TEMPLATE/profile.html', context)
	else:
		return redirect(reverse('signin'))
		
		
def logoutuser(request):
	logout(request)
	return redirect(reverse('mainpage'))
	
def main_page(request):
	post = Post.objects.all()
	if post:
		objects = post[0]
		context = {'post': objects, 'posts': post, 'CommentForm': validate_comment()}
		return render(request, 'comments/TEMPLATE/index.html', context)
	else:
		context = {}
		return render(request, 'comments/TEMPLATE/index.html', context)
		
	
	
#messages.add_message(request, messages.INFO, 'Hello world.')
#messages.debug(request, '%s SQL statements were executed.' % count)
#messages.info(request, 'Three credits remain in your account.')
#messages.success(request, 'Profile details updated.')
#messages.warning(request, 'Your account expires in three days.')
#messages.error(request, 'Document deleted.')