from django.contrib import admin

# Register your models here.
from .models import ApplicationData, ApplicationAccess, UserActivity

admin.site.register(ApplicationData)
admin.site.register(ApplicationAccess)
admin.site.register(UserActivity)