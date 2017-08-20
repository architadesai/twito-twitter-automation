
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


admin.site.register(AppAccess)
admin.site.register(TwitterApp)
admin.site.register(TasksList)
admin.site.register(TaskLike)
admin.site.register(TaskFollow)
admin.site.register(TaskreTweet)

#admin.site.register(LocationSearch)