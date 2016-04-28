from api.models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.shortcuts import render
<<<<<<< HEAD
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
import json
=======
import json
from django.template import loader
>>>>>>> origin/master
=======
import json
from django.template import loader
>>>>>>> origin/master

CATEGORY_CHOICES = ((0, 'Health'), (1, 'Fitness'), (2, 'Social'))
STATUS_CHOICES = ((0, 'Open'), (1, 'Accepted'), (2, 'Declined'))
USER_TYPES = ((True, 'Organizer'), (False, 'User'))

@csrf_exempt
def index(request):
<<<<<<< HEAD
<<<<<<< HEAD
	return render(request,'api/events.html', {'admin': request.user.is_superuser, 'events': getEvents(request, True).values(), 'pastevents': getPastEvents(request, True).values()})
=======
=======
>>>>>>> origin/master
    template = loader.get_template('api/index.html')
    context = {
        'events': getEvents(request, True).values(),
    }
    return HttpResponse(template.render(context, request))
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master

def update(request):
	print 'Updating....'
	response = JsonResponse({'events': getEvents(request, True).values()}, status=200, safe=False)
	response['access-control-allow-origin'] = '*'
	return response

def getUsers(request):
	try:
		users = {}
		for user in User.objects.all():
<<<<<<< HEAD
<<<<<<< HEAD
			users[user.username] = {'name':user.name, 'country':user.country, 'org':user.is_org, 'donations':user.donations, 'email':user.email}
=======
			users[user.username] = {'name':user.name, 'country':user.country, 'org':user.is_org}
>>>>>>> origin/master
=======
			users[user.username] = {'name':user.name, 'country':user.country, 'org':user.is_org}
>>>>>>> origin/master
		response = JsonResponse(users, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

<<<<<<< HEAD
<<<<<<< HEAD
def getEvents(request, index=False):
	try:
		events = {}
		canEdit = request.user.is_superuser
		for event in Event.objects.filter(start_date__gte=datetime.today()):
			count_joined = len(Participation.objects.filter(event=event, has_joined=True))
			count_rsvpd = len(Participation.objects.filter(event=event, has_rsvpd=True))
			events[event.id] = {'id':event.id, 'name':event.name, 'description':event.description,'max_capacity':event.max_capacity, 'catCode':2, 'category':"Social", 'start_date':event.start_date.strftime("%d-%m-%Y"), 'start_time':event.start_date.strftime("%H:%M"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'end_time':event.end_date.strftime("%H:%M"), 'org_username':event.org.username, 'org_name':event.org.name, 'count_rsvpd':count_rsvpd, 'count_joined':count_joined}
			#events[event.id] = {'id':event.id, 'name':event.name, 'description':event.description, 'category':dict(CATEGORY_CHOICES)[event.category], 'start_date':event.start_date.strftime("%d-%m-%Y"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'org':event.org.name, 'count_liked':count_liked, 'count_joined':count_joined}
		if index:
			return events
		response = JsonResponse(events, status=200, safe=False)
=======
=======
>>>>>>> origin/master
def getTasks(request):
	try:
		tasks = {}
		for task in Task.objects.all():
			tasks[task.id] = {'name':task.name, 'description':task.description, 'category':dict(CATEGORY_CHOICES)[task.category]}
		response = JsonResponse(tasks, status=200, safe=False)
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)
<<<<<<< HEAD
<<<<<<< HEAD
		
def getPastEvents(request, index=False):
	try:
		events = {}
		for event in Event.objects.exclude(start_date__gte=datetime.today()):
			count_joined = len(Participation.objects.filter(event=event, has_joined=True))
			count_rsvpd = len(Participation.objects.filter(event=event, has_rsvpd=True))
			events[event.id] = {'id':event.id, 'name':event.name, 'description':event.description,'max_capacity':event.max_capacity, 'catCode':2, 'category':"Social", 'start_date':event.start_date.strftime("%d-%m-%Y"), 'start_time':event.start_date.strftime("%H:%M"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'end_time':event.end_date.strftime("%H:%M"), 'org_username':event.org.username, 'org_name':event.org.name, 'count_rsvpd':count_rsvpd, 'count_joined':count_joined}
=======
=======
>>>>>>> origin/master

def getEvents(request, index=False):
	try:
		events = {}
		for event in Event.objects.all():
			count_joined = len(Participation.objects.filter(event=event, has_joined=True))
			count_liked = len(Participation.objects.filter(event=event, has_liked=True))
			events[event.id] = {'id':event.id, 'name':event.name, 'description':event.description, 'catCode':event.category, 'category':dict(CATEGORY_CHOICES)[event.category], 'start_date':event.start_date.strftime("%d-%m-%Y"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'org':event.org.name, 'count_liked':count_liked, 'count_joined':count_joined}
			#events[event.id] = {'id':event.id, 'name':event.name, 'description':event.description, 'category':dict(CATEGORY_CHOICES)[event.category], 'start_date':event.start_date.strftime("%d-%m-%Y"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'org':event.org.name, 'count_liked':count_liked, 'count_joined':count_joined}
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		if index:
			return events
		response = JsonResponse(events, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUser(request, username):
	try:
		user = User.objects.get(username=username)
<<<<<<< HEAD
<<<<<<< HEAD
		response = JsonResponse({'username':user.username, 'name':user.name, 'country':user.country, 'org':user.is_org, 'email':user.email, 'donations':user.donations}, status=200, safe=False)
=======
=======
>>>>>>> origin/master
		response = JsonResponse({'username':user.username, 'name':user.name, 'country':user.country, 'org':user.is_org}, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUserTasks(request, username):
	try:
		from_tasks = {}
		to_tasks = {}
		f_tasks = Challenge.objects.filter(creator=username).order_by('-created')
		t_tasks = Challenge.objects.filter(assignee=username).order_by('-created')
		for f in f_tasks:
			from_tasks[f.id] = {'creator':f.creator.username,'assignee':f.assignee.username,'status':dict(STATUS_CHOICES)[f.status],'date':f.created.strftime("%d-%m-%Y")}
		for t in t_tasks:
			to_tasks[t.id] = {'creator':t.creator.username,'assignee':t.assignee.username,'status':dict(STATUS_CHOICES)[t.status],'date':t.created.strftime("%d-%m-%Y")}
		response = JsonResponse({'from_tasks': from_tasks, 'to_tasks': to_tasks}, status=200, safe=False)
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUserEvents(request, username):
	try:
		events = {}
		u_events = Participation.objects.filter(user=username).order_by('-created')
		for u in u_events:
<<<<<<< HEAD
<<<<<<< HEAD
			events[u.id] = {'has_joined':u.has_joined, 'has_rsvpd':u.has_rsvpd, 'event':u.event.id}
=======
			events[u.id] = {'has_joined':u.has_joined, 'has_liked':u.has_liked, 'event':u.event.id}
>>>>>>> origin/master
=======
			events[u.id] = {'has_joined':u.has_joined, 'has_liked':u.has_liked, 'event':u.event.id}
>>>>>>> origin/master
		response = JsonResponse(events, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getEventParticipations(request):
	try:
		result = {}
		participations = Participation.objects.filter(event=request.GET['event'])
		for p in participations:
<<<<<<< HEAD
<<<<<<< HEAD
			result[p.id] = {'username':p.user.username, 'name': p.user.name, 'country': p.user.country, 'rsvp': p.has_rsvpd, 'join': p.has_joined}
=======
			result[p.id] = {'username':p.user.username, 'name': p.user.name, 'country': p.user.country, 'like': p.has_liked, 'join': p.has_joined}
>>>>>>> origin/master
=======
			result[p.id] = {'username':p.user.username, 'name': p.user.name, 'country': p.user.country, 'like': p.has_liked, 'join': p.has_joined}
>>>>>>> origin/master
		response = JsonResponse(result, status=200, safe=False)
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

<<<<<<< HEAD
<<<<<<< HEAD
@login_required(login_url='/admin/login')
def createEvent(request):
	return render(request,'api/create.html')

@csrf_exempt
@login_required(login_url='/admin/login/')
def addUser(request):
	try:
		query = User(username=request.GET['username'], name=request.GET['name'], country="N/A", is_org=request.GET['is_org'], )
=======
=======
>>>>>>> origin/master

@csrf_exempt
def addUser(request):
	try:
		query = User(username=request.GET['username'], name=request.GET['name'], country=request.GET['country'], is_org=request.GET['org'])
		query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def addTask(request):
	try:
		query = Task(name=request.GET['name'], description=request.GET['description'], category=int(request.GET['category']))
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
<<<<<<< HEAD
<<<<<<< HEAD
@login_required(login_url='/admin/login/')
=======
>>>>>>> origin/master
=======
>>>>>>> origin/master
def addEvent(request):
	try:
		org = User.objects.get(username=request.GET['org'])
		if org.is_org:
<<<<<<< HEAD
<<<<<<< HEAD
			query = Event(org=org, name=request.GET['name'], description=request.GET['description'], category=0, max_capacity=request.GET['max_capacity'], suggested_donation=request.GET['suggested_donation'], start_date=request.GET['start_date'], end_date=request.GET['start_date'])
=======
			query = Event(org=org, name=request.GET['name'], description=request.GET['description'], category=int(request.GET['category']), start_date=request.GET['start'],  end_date=request.GET['end'])
>>>>>>> origin/master
=======
			query = Event(org=org, name=request.GET['name'], description=request.GET['description'], category=int(request.GET['category']), start_date=request.GET['start'],  end_date=request.GET['end'])
>>>>>>> origin/master
			query.save()
			response = HttpResponse(True, status=200)
		else:
			response = HttpResponse('User is not an organizer.', status=200)

		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

<<<<<<< HEAD
<<<<<<< HEAD
@csrf_exempt
def updateEvent(request):
	try:
		org = User.objects.get(username=request.GET['org_username'])
		if org.is_org:
			e = Event.objects.get(id=request.GET['eventID'])
			if request.user.is_superuser or request.user.username == e.org.username:
				e.org = org
				e.save()
				e.name = request.GET['name']
				e.save()
				e.description = request.GET['description']
				e.save()
				e.max_capacity = request.GET['max_capacity']
				e.save()
				e.suggested_donation = request.GET['suggested_donation']
				e.save()
				e.start_date = request.GET['start_date']
				e.save()
				e.end_date = request.GET['start_date']
				e.save()
			#query = Event(org=org, name=request.GET['name'], description=request.GET['description'], category=0, max_capacity=request.GET['max_capacity'], suggested_donation=request.GET['suggested_donation'], start_date=request.GET['start_date'], end_date=request.GET['start_date'])
				response = HttpResponse(True, status=200)
			else:
				response = HttpResponse('User is not an organizer.', status=200)
		else:
			response = HttpResponse('New user is not an organizer.', status=200)

=======
=======
>>>>>>> origin/master

@csrf_exempt
def challenge(request):
	try:
		creator = User.objects.get(username=request.GET['creator'])
		assignee = User.objects.get(username=request.GET['assignee'])
		task = Task.objects.get(id=request.GET['task'])
		query = Challenge(creator=creator, assignee=assignee, task=task)
		query.save()
		response = HttpResponse(True, status=200)
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

<<<<<<< HEAD
<<<<<<< HEAD

@csrf_exempt
@login_required(login_url='/admin/login/')
def deleteEvent(request):
	try:
		e = Event.objects.get(id=request.GET['eventID'])
		#print "Stuff"			
		e.delete()
=======
=======
>>>>>>> origin/master
@csrf_exempt
def accept(request):
	try:
		challenge = Challenge.objects.get(id=request.GET['challenge'])
		challenge.status = 1
		challenge.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def decline(request):
	try:
		challenge = Challenge.objects.get(id=request.GET['challenge'])
		challenge.status = 2
		challenge.save()
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def join(request):
	try:
		user = User.objects.get(username=request.GET['user'])
		event = Event.objects.get(id=request.GET['event'])
		participation = Participation.objects.filter(user=user, event=event)
		if len(participation) > 0:
			participation = participation[0]
			if participation.has_joined:
				participation.has_joined = False
			else:
				participation.has_joined = True
			participation.save()
		else:
			query = Participation(user=user, event=event, has_joined=True)
			query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		update(request)
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
<<<<<<< HEAD
<<<<<<< HEAD
def rsvp(request):
=======
def like(request):
>>>>>>> origin/master
=======
def like(request):
>>>>>>> origin/master
	try:
		user = User.objects.get(username=request.GET['user'])
		event = Event.objects.get(id=request.GET['event'])
		participation = Participation.objects.filter(user=user, event=event)
		if len(participation) > 0:
			participation = participation[0]
<<<<<<< HEAD
<<<<<<< HEAD
			if participation.has_rsvpd:
				participation.has_rsvpd = False
			else:
				participation.has_rsvpd = True
			participation.save()
		else:
			query = Participation(user=user, event=event, has_rsvpd=True)
=======
=======
>>>>>>> origin/master
			if participation.has_liked:
				participation.has_liked = False
			else:
				participation.has_liked = True
			participation.save()
		else:
			query = Participation(user=user, event=event, has_liked=True)
<<<<<<< HEAD
>>>>>>> origin/master
=======
>>>>>>> origin/master
			query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		update(request)
		return response
	except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
		return HttpResponse(str(e), status=500)
		
def addcomment(request, eventID):
	try:
		'''
		user = User.objects.get(username=request.META['geuid'])
		event = Event.objects.get(id=eventID)
    	c = {}
    	c.update(csrf(request))
    	e = Comment(owner=user,\
                	event=event,\
                	comment=request.POST['comment'])
    	e.save()
    
    	e.canRemove = True
    
    	e.save()
    	#return render_to_response('ahmadsapp/comment.html', {'comment':e})'''
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

'''
def getTasks(request):
	try:
		tasks = {}
		for task in Task.objects.all():
			tasks[task.id] = {'name':task.name, 'description':task.description, 'category':dict(CATEGORY_CHOICES)[task.category]}
		response = JsonResponse(tasks, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def challenge(request):
	try:
		creator = User.objects.get(username=request.GET['creator'])
		assignee = User.objects.get(username=request.GET['assignee'])
		task = Task.objects.get(id=request.GET['task'])
		query = Challenge(creator=creator, assignee=assignee, task=task)
		query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def accept(request):
	try:
		challenge = Challenge.objects.get(id=request.GET['challenge'])
		challenge.status = 1
		challenge.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def decline(request):
	try:
		challenge = Challenge.objects.get(id=request.GET['challenge'])
		challenge.status = 2
		challenge.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def addTask(request):
	try:
		query = Task(name=request.GET['name'], description=request.GET['description'], category=int(request.GET['category']))
		query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUserTasks(request, username):
	try:
		from_tasks = {}
		to_tasks = {}
		f_tasks = Challenge.objects.filter(creator=username).order_by('-created')
		t_tasks = Challenge.objects.filter(assignee=username).order_by('-created')
		for f in f_tasks:
			from_tasks[f.id] = {'creator':f.creator.username,'assignee':f.assignee.username,'status':dict(STATUS_CHOICES)[f.status],'date':f.created.strftime("%d-%m-%Y")}
		for t in t_tasks:
			to_tasks[t.id] = {'creator':t.creator.username,'assignee':t.assignee.username,'status':dict(STATUS_CHOICES)[t.status],'date':t.created.strftime("%d-%m-%Y")}
		response = JsonResponse({'from_tasks': from_tasks, 'to_tasks': to_tasks}, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

'''
=======
		return HttpResponse(str(e), status=500)
>>>>>>> origin/master
=======
		return HttpResponse(str(e), status=500)
>>>>>>> origin/master
