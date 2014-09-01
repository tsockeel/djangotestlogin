#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from studiosnaps.forms import LoginForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from studiosnaps.models import UserProfile

import logging
import zmq
from zmq.log.handlers import PUBHandler

# Create your views here.


def home(request):
	# Process form data
	error = False
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			# Check input data and return a valid user if exists
			user = authenticate(username=login_form.cleaned_data["username"], password=login_form.cleaned_data["password"])
			if user:
				# Do the login
				login(request, user)
			else:
				error = True
	else:
		login_form = LoginForm()

	track(request, "home")
	return render_to_response('studiosnaps/home.html', locals(), RequestContext(request))

def user_login(request):
	# Process form data
	if request.method == 'POST':

		# Check if the username/password combination is valid and a User object is returned if it is
		user = authenticate(username=request.POST['username'], password=request.POST['password'])

		if user:
			login(request, user)
			return HttpResponseRedirect('/studiosnaps/')
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		track(request, "user_login")
		return render_to_response('studiosnaps/home.html', {}, RequestContext(request))

@login_required
def user_logout(request):
	track(request, "user_logout")
	logout(request)
	return HttpResponseRedirect('/studiosnaps/')
		
@login_required
def profile(request):
	context = RequestContext(request)
	user = User.objects.get(username=request.user)
	currentProfile = user.userprofile

	if request.method == "POST":
		profile_form = UserProfileForm(data=request.POST)
		if profile_form.is_valid():
			currentProfile.city = profile_form.cleaned_data['city']
			currentProfile.happy = profile_form.cleaned_data['happy']
			currentProfile.save();
			edit = False
			return HttpResponseRedirect('/studiosnaps/')
	else:
		edit = True
		profile_form = UserProfileForm(instance=currentProfile) 

	track(request, "profile")
	return render_to_response('studiosnaps/profile.html', locals(), context)

def register(request):
	# Get the client context, machine details
	context = RequestContext(request)

	# Process form data
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			# Save the user's form data to the database.
			userCreated = user_form.save()

			# Hash the password 
			userCreated.set_password(user_form.cleaned_data["password"])
			userCreated.save()

			userprofileCreated = UserProfile(user=userCreated)
			userprofileCreated.save()

			user = authenticate(username=user_form.cleaned_data["username"]	, password=user_form.cleaned_data["password"])
			if user:
				login(request, user)
			return HttpResponseRedirect('/studiosnaps/')
		else:
			print user_form.errors

	else:
		user_form = UserForm()

	track(request, "register")
	# Render the template depending on the context.
	return render_to_response('studiosnaps/register.html',locals(), context)

def starttracking(request):

	logger = logging.getLogger("tracking")

	if request.session.get('isTracking', False) == False:
		isSetup = False
		for o in logger.handlers:
			isSetup = isinstance(o, PUBHandler)
		if not isSetup:
			pub = zmq.Context().socket(zmq.PUB)
			pub.bind('tcp://*:5555')
			handler = PUBHandler(pub)
			logger.setLevel(logging.DEBUG)
			logger.addHandler(handler)

	request.session['isTracking'] = True
	track(request, "START TRACKING")

	return redirect('home')

def stoptracking(request):
	track(request, "STOP TRACKING")
	request.session['isTracking'] = False
	return redirect('home')

def track(request, message):
	if request.session.get('isTracking', False) == True:
		logger = logging.getLogger("tracking")
		logger.log(logging.INFO, "user %s: tracked:%s" % (request.user, message))
