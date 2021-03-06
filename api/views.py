from api.models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
import json
from operator import itemgetter

CATEGORY_CHOICES = ((0, 'Health'), (1, 'Fitness'), (2, 'Social'))
STATUS_CHOICES = ((0, 'Open'), (1, 'Accepted'), (2, 'Declined'))
USER_TYPES = ((True, 'Organizer'), (False, 'User'))

@csrf_exempt
def index(request):
	try:
		if not User.objects.filter(username=str(request.META['geuid'])).exists():
			query = User(username=str(request.META['geuid']), name=str(request.META['gefirstname'])+" "+str(request.META['gelastname']), country="U.S.A", is_org=False, email=str(request.META['gemail']), donations=0)
			query.save()
		return render(request,'api/events.html', {'admin': request.user.is_superuser, 'current_user': str(request.META['gefirstname'])+" "+str(request.META['gelastname']), 'events': getEvents(request, True).values(), 'pastevents': getPastEvents(request, True).values()})
	except Exception as e:
		return HttpResponse(str(e), status=500)

def update(request):
	print 'Updating....'
	response = JsonResponse({'events': getEvents(request, True).values()}, status=200, safe=False)
	response['access-control-allow-origin'] = '*'
	return response

def getAnnualStats(request):
	mysum = getUserEventsStats(request, str(request.META['geuid']))[2]
	#mysum = getUserEventsStats(request, "212447934")[1]
	return render(request,'api/annual.html', {'admin': request.user.is_superuser, 'current_user': str(request.META['gefirstname'])+" "+str(request.META['gelastname']), 'my_sum': mysum, 'all_attendees': getAllUserEventsStats(request).values(), 'all_ssos': getAllUserSSOs(request).values()})

def getUsers(request):
	try:
		users = {}
		for user in User.objects.filter():
			users[user.username] = {'name':user.name, 'country':user.country, 'org':user.is_org, 'donations':user.donations, 'email':user.email}
		response = JsonResponse(users, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getEvents(request, index=False):
	try:
		events = {}
		canEdit = request.user.is_superuser
		for event in Event.objects.filter(start_date__gte=datetime.today()):
			jlist = Participation.objects.filter(event=event, has_joined=True)
			rlist = Participation.objects.filter(event=event, has_rsvpd=True)
			joinedlist = []
			for p in jlist:
				joinedlist.append(p.user.name)
			rsvpdlist = []
			for p in rlist:
				rsvpdlist.append(p.user.name)
			count_joined = len(jlist)
			count_rsvpd = len(rlist)
			canEdit = canEdit or str(request.META['geuid']) == str(event.org.username)
			events[event.id] = {'id':event.id, 'canEdit':canEdit, 'name':event.name, 'rsvpdlist':rsvpdlist, 'joinedlist':joinedlist, 'suggested_donation':event.suggested_donation, 'description':event.description,'max_capacity':event.max_capacity, 'catCode':2, 'category':"Social", 'start_date':event.start_date.strftime("%d-%m-%Y"), 'start_time':event.start_date.strftime("%H:%M"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'end_time':event.end_date.strftime("%H:%M"), 'org_username':event.org.username, 'org_name':event.org.name, 'count_rsvpd':count_rsvpd, 'count_joined':count_joined}
		if index:
			return events
		response = JsonResponse(events, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)
		
def getPastEvents(request, index=False):
	try:
		events = {}
		for event in Event.objects.exclude(start_date__gte=datetime.today()):
			jlist = Participation.objects.filter(event=event, has_joined=True)
			rlist = Participation.objects.filter(event=event, has_rsvpd=True)
			joinedlist = []
			for p in jlist:
				joinedlist.append(p.user.name)
			rsvpdlist = []
			for p in rlist:
				rsvpdlist.append(p.user.name)
			count_joined = len(jlist)
			count_rsvpd = len(rlist)
			events[event.id] = {'id':event.id, 'name':event.name, 'rsvpdlist':rsvpdlist, 'joinedlist':joinedlist,'description':event.description,'max_capacity':event.max_capacity, 'suggested_donation':event.suggested_donation, 'catCode':2, 'category':"Social", 'start_date':event.start_date.strftime("%d-%m-%Y"), 'start_time':event.start_date.strftime("%H:%M"), 'end_date':event.end_date.strftime("%d-%m-%Y"), 'end_time':event.end_date.strftime("%H:%M"), 'org_username':event.org.username, 'org_name':event.org.name, 'count_rsvpd':count_rsvpd, 'count_joined':count_joined}
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
		response = JsonResponse({'username':user.username, 'name':user.name, 'country':user.country, 'org':user.is_org, 'email':user.email, 'donations':user.donations}, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUserEvents(request, username):
	try:
		user = User.objects.get(username=username)
		events = {}
		u_events = Participation.objects.filter(user=user).order_by('-created')
		for u in u_events:
			events[u.id] = {'has_joined':u.has_joined, 'has_rsvpd':u.has_rsvpd, 'event':u.event.id}
		response = JsonResponse(events, status=200, safe=False)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getUserEventsStats(request, username):
	try:
		total = 0
		count = 0
		user = User.objects.get(username=username)
		u_events = Participation.objects.filter(user=user).order_by('-created')
		for u in u_events:
			if u.has_joined:
				total+= u.event.suggested_donation
				count+=1
		totalwithdrinks = total + 3*(user.num_drinks)
		result = [count, total, totalwithdrinks]
		return result
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getAllUserEventsStats(request):
	try:		
		result = {}
		for usr in User.objects.all():
			#print usr.username
			total = 0
			count = 0
			u_events = Participation.objects.filter(user=usr)
			for u in u_events:
				if u.has_joined:
					total+= u.event.suggested_donation
					count+=1
			total = total + 3*(usr.num_drinks)
			result[usr.username] = {'name':usr.name, 'sso':usr.username, 'count':int(count), 'total':total}
			
		#print result
		newlist = sorted(result.iteritems(), key=lambda (x, y): y['count'], reverse=True)
		usercount = 1
		sortedTopTenResults = {}
		for (item, value) in newlist:
			if usercount >= 11:
				break
			newvalue = value
			newvalue['rank'] = usercount
			sortedTopTenResults[usercount] = newvalue
			print newvalue
			usercount+=1
		return sortedTopTenResults
	except Exception as e:
		return HttpResponse(str(e), status=500)

def getAllUserSSOs(request):
	try:		
		result = {}
		for usr in User.objects.all():
			#print usr.username
			total = 0
			count = 0
			u_events = Participation.objects.filter(user=usr)
			for u in u_events:
				if u.has_joined:
					total+= u.event.suggested_donation
					count+=1
			result[usr.username] = {'name':usr.name, 'sso':usr.username, 'count':count, 'total':total}
		return result
	except Exception as e:
		return HttpResponse(str(e), status=500)


def getEventParticipations(request):
	try:
		result = {}
		participations = Participation.objects.filter(event=request.GET['event'])
		for p in participations:
			result[p.id] = {'username':p.user.username, 'name': p.user.name, 'country': p.user.country, 'rsvp': p.has_rsvpd, 'join': p.has_joined}
		response = JsonResponse(result, status=200, safe=False)
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@login_required(login_url='/admin/login')
def createEvent(request):
	return render(request,'api/create.html', {'current_user': str(request.META['gefirstname'])+" "+str(request.META['gelastname'])})

@csrf_exempt
@login_required(login_url='/admin/login/')
def addUser(request):
	try:
		query = User(username=request.GET['username'], name=request.GET['name'], country="N/A", is_org=request.GET['is_org'], )
		query.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
@login_required(login_url='/admin/login/')
def addEvent(request):
	try:
		org = User.objects.get(username=request.GET['org'])
		org.is_org = True
		org.save()
		query = Event(org=org, name=request.GET['name'], description=request.GET['description'], category=0, max_capacity=request.GET['max_capacity'], suggested_donation=request.GET['suggested_donation'], start_date=request.GET['start_date'], end_date=request.GET['start_date'])
		query.save()
		response = HttpResponse(True, status=200)

		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

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

		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@login_required(login_url='/admin/login/')
def uploadDrinks(request):
	try:
		drinks_array = json.loads(request.GET['drinkArray'])
		responsearray = ""
		for u in drinks_array:
			drinker = BadgeDB.objects.get(badgeNumber=str(u))
			user = User.objects.get(username=drinker.username)
			user.num_drinks = user.num_drinks + 1
			user.save()
			#responsearray = responsearray + " " + str(drinker.username) + " " + str(user.num_drinks)
			#user.donations = user.num_drinks
			#user.save()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
@login_required(login_url='/admin/login/')
def deleteEvent(request):
	try:
		e = Event.objects.get(id=request.GET['eventID'])
		#print "Stuff"			
		e.delete()
		response = HttpResponse(True, status=200)
		response['access-control-allow-origin'] = '*'
		return response
	except Exception as e:
		return HttpResponse(str(e), status=500)

@csrf_exempt
def join(request):
	try:
		attendee = BadgeDB.objects.get(badgeNumber=request.GET['badgenum'])
		if not User.objects.filter(username=attendee.username).exists():
			query = User(username=attendee.username, name=attendee.name, country="U.S.A", is_org=False, email="N/A", donations=0)
			query.save()
		user = User.objects.get(username=attendee.username)
		event = Event.objects.get(id=request.GET['eID'])
		participation = Participation.objects.filter(user=user, event=event)
		if len(participation) > 0:
			participation = participation[0]
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
def rsvp(request):
	try:
		if not User.objects.filter(username=str(request.META['geuid'])).exists():
			query = User(username=str(request.META['geuid']), name=str(request.META['gefirstname'])+" "+str(request.META['gelastname']), country="U.S.A", is_org=False, email=str(request.META['gemail']), donations=0)
			query.save()

		user = User.objects.get(username=str(request.META['geuid']))
		event = Event.objects.get(id=request.GET['eID'])
		participation = Participation.objects.filter(user=user, event=event)
		if len(participation) > 0:
			participation = participation[0]
			if participation.has_rsvpd:
				participation.has_rsvpd = False
				participation.save()
			else:
				participation.has_rsvpd = True
				participation.save()
		else:
			query = Participation(user=user, event=event, has_rsvpd=True)
			query.save()
			response = HttpResponse(True, status=200)
			response['access-control-allow-origin'] = '*'
			return response
	except Exception as e:
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
