#-*- coding: utf-8 -*-
from studiosnaps.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=30)
	password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('city', 'happy')