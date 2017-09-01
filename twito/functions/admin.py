
from django.contrib import admin

# Register your models here.

from .models import (
    TwitterApp,
    TasksList,
    TaskreTweet,
    TaskFollow,
    TaskLike,
    AppAccess,
)


#admin.site.register(LocationSearch)

class TwitterAppAdmin(admin.ModelAdmin):

    list_display = ["appName","user","createdAt"]
    class Meta:

        model = TwitterApp

class AppAccessAdmin(admin.ModelAdmin):

    list_display = ["appName","user","createdAt"]
    class Meta:

        model = AppAccess

class TasksListAdmin(admin.ModelAdmin):

    list_display = ["appName","user","taskName","time"]
    class Meta:

        model = TasksList

class TaskLikeAdmin(admin.ModelAdmin):

    list_display = ["appName","user","tweetID","time"]
    class Meta:

        model = TaskLike

class TaskFollowAdmin(admin.ModelAdmin):

    list_display = ["appName","user","followUserID","time"]
    class Meta:

        model = TaskFollow

class TaskreTweetAdmin(admin.ModelAdmin):

    list_display = ["appName","user","tweetID","time"]
    class Meta:

        model = TaskreTweet



admin.site.register(AppAccess, AppAccessAdmin)
admin.site.register(TwitterApp, TwitterAppAdmin)
admin.site.register(TasksList, TasksListAdmin)
admin.site.register(TaskLike, TaskLikeAdmin)
admin.site.register(TaskFollow, TaskFollowAdmin)
admin.site.register(TaskreTweet, TaskreTweetAdmin)

