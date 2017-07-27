from django.contrib import admin

# Register your models here.

from .models import TwitterApp, LocationSearch


admin.site.register(TwitterApp)
admin.site.register(LocationSearch)