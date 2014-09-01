#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from studiosnaps import views

urlpatterns = patterns('studiosnaps.views',
	url(r'^$', views.home, name='home'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.user_logout, name='user_logout'),

	url(r'^starttracking/$', views.starttracking, name='starttracking'),
	url(r'^stoptracking/$', views.stoptracking, name='stoptracking'),
)