from django.db import models
from datetime import datetime

CATEGORY_CHOICES = ((0, 'Health'), (1, 'Fitness'), (2, 'Social'))
STATUS_CHOICES = ((0, 'Open'), (1, 'Accepted'), (2, 'Declined'))
USER_TYPES = ((True, 'Organizer'), (False, 'User'))

class User(models.Model):
	username = models.CharField(max_length=15, primary_key=True) # SSO
	name = models.CharField(max_length=30) # First & Last Name
	country = models.CharField(max_length=30)
	donations = models.IntegerField()
	email = models.CharField(max_length=30)
	is_org = models.BooleanField('organizer', default=False)
	def __str__(self):
		return "%s (%s)" % (self.name, dict(USER_TYPES)[self.is_org])

class BadgeDB(models.Model):
	username = models.CharField(max_length=15, primary_key=True) # SSO
	name = models.CharField(max_length=30) # First & Last Name
	badgeNumber = models.CharField(max_length=20) #badge number
	def __str__(self):
		return self.name

# IGNORE
class Task(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=2500)
	category = models.IntegerField(choices=CATEGORY_CHOICES)
	def __str__(self):
		return "%s (%s)" % (self.name, dict(CATEGORY_CHOICES)[self.category])

class Event(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=2500)
	category = models.IntegerField(choices=CATEGORY_CHOICES)
	max_capacity = models.IntegerField()
	start_date = models.DateTimeField(default=datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0))
	end_date = models.DateTimeField(default=datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0)) # no need
	suggested_donation = models.IntegerField()
	org = models.ForeignKey(User)
	def __str__(self):
		return "%s (%s)" % (self.name, dict(CATEGORY_CHOICES)[self.category])

class Comment(models.Model):
	owner = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	comment = models.TextField()
	canRemove = models.BooleanField(default=False)
	def __str__(self):
		return self.owner.name

class Participation(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	has_joined = models.BooleanField(default=False)
	has_rsvpd = models.BooleanField(default=False) # RSVP
	created = models.DateTimeField(auto_now_add=True) # no need
	def __str__(self):
		if self.has_joined:
			return "%s has joined %s" % (self.user.name, self.event)
		return "%s has rsvpd %s" % (self.user.name, self.event)
#IGNORE
class Challenge(models.Model):
	creator = models.ForeignKey(User, null=True, related_name='creator')
	assignee = models.ForeignKey(User, null=True, related_name='assignee')
	task = models.ForeignKey(Task)
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "%s challenges %s to %s" % (self.creator.name, self.assignee.name, self.task.description.lower())