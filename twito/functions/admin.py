from django.contrib import admin

# Register your models here.

from .models import TwitterApp

admin.site.register(TwitterApp)