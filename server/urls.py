<<<<<<< HEAD
<<<<<<< HEAD
from django.conf.urls import patterns, include, urlfrom django.contrib import adminurlpatterns = patterns('',	url(r'^$', 							'api.views.index'),	url(r'^update/$', 					'api.views.update'),	url(r'^admin/', 					include(admin.site.urls)),		url(r'^users/', 					'api.views.getUsers'),	#url(r'^tasks/', 					'api.views.getTasks'),	url(r'^events/', 					'api.views.getEvents'),	url(r'^parts/', 					'api.views.getEventParticipations'),	url(r'^(?P<username>\w+)/profile/',	'api.views.getUser'),	#url(r'^(?P<username>\w+)/tasks/', 	'api.views.getUserTasks'),	url(r'^(?P<username>\w+)/events/',	'api.views.getUserEvents'),		url(r'^add/user/', 					'api.views.addUser'),	#url(r'^add/task/', 					'api.views.addTask'),	url(r'^create/event/', 				'api.views.createEvent'),	url(r'^update/event/', 				'api.views.updateEvent'),	url(r'^delete/event/', 				'api.views.deleteEvent'),	url(r'^add/event/', 				'api.views.addEvent'),		url(r'^addcomment/(?P<eventID>\d+)/$', 'api.views.addcomment'),	#url(r'^challenge/', 				'api.views.challenge'),	#url(r'^accept/', 					'api.views.decline'),	#url(r'^decline/', 					'api.views.decline'),	url(r'^like/', 						'api.views.rsvp'),	url(r'^join/', 						'api.views.join'),)from django.contrib.staticfiles.urls import staticfiles_urlpatternsurlpatterns += staticfiles_urlpatterns()
=======
from django.conf.urls import include, urlfrom django.contrib import adminfrom api import viewsurlpatterns = [	url(r'^$', 							views.index),	url(r'^update/$', 					views.update),	url(r'^admin/', 					admin.site.urls),	url(r'^users/', 					views.getUsers),	url(r'^tasks/', 					views.getTasks),	url(r'^events/', 					views.getEvents),	url(r'^parts/', 					views.getEventParticipations),	url(r'^(?P<username>\w+)/profile/',	views.getUser),	url(r'^(?P<username>\w+)/tasks/', 	views.getUserTasks),	url(r'^(?P<username>\w+)/events/',	views.getUserEvents),		url(r'^add/user/', 					views.addUser),	url(r'^add/task/', 					views.addTask),	url(r'^add/event/', 				views.addEvent),	url(r'^challenge/', 				views.challenge),	url(r'^accept/', 					views.decline),	url(r'^decline/', 					views.decline),	url(r'^like/', 						views.like),	url(r'^join/', 						views.join),]from django.contrib.staticfiles.urls import staticfiles_urlpatternsurlpatterns += staticfiles_urlpatterns()
>>>>>>> origin/master
=======
from django.conf.urls import include, urlfrom django.contrib import adminfrom api import viewsurlpatterns = [	url(r'^$', 							views.index),	url(r'^update/$', 					views.update),	url(r'^admin/', 					admin.site.urls),	url(r'^users/', 					views.getUsers),	url(r'^tasks/', 					views.getTasks),	url(r'^events/', 					views.getEvents),	url(r'^parts/', 					views.getEventParticipations),	url(r'^(?P<username>\w+)/profile/',	views.getUser),	url(r'^(?P<username>\w+)/tasks/', 	views.getUserTasks),	url(r'^(?P<username>\w+)/events/',	views.getUserEvents),		url(r'^add/user/', 					views.addUser),	url(r'^add/task/', 					views.addTask),	url(r'^add/event/', 				views.addEvent),	url(r'^challenge/', 				views.challenge),	url(r'^accept/', 					views.decline),	url(r'^decline/', 					views.decline),	url(r'^like/', 						views.like),	url(r'^join/', 						views.join),]from django.contrib.staticfiles.urls import staticfiles_urlpatternsurlpatterns += staticfiles_urlpatterns()
>>>>>>> origin/master
