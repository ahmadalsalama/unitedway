from django.contrib import admin
from api.models import User, Task, Event, Participation, Challenge, BadgeDB, Comment

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(Participation)
admin.site.register(Challenge)
admin.site.register(BadgeDB)
admin.site.register(Comment)