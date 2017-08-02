from django.contrib import admin

# Register your models here.

from .models import TwitterApp, TasksList


admin.site.register(TwitterApp)
admin.site.register(TasksList)

#admin.site.register(LocationSearch)