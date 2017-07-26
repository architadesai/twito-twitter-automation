from __future__ import unicode_literals

from django.db import models
from .random_primary import RandomPrimaryIdModel as RandomPrimaryId
from django.contrib.auth.models import User
# Create your models here.


class TwitterApp(RandomPrimaryId):
    user = models.ForeignKey(User, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    AppName = models.TextField(max_length=50)
    ConsumerKey = models.TextField(max_length=100)
    ConsumerToken = models.TextField(max_length=100)

    def get_absolute_url(self):
        return "/dashboard/%s/" % self.id


class TwitterApp_User(models.Model):
    user = models.ForeignKey(User, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    app = models.ForeignKey(TwitterApp, on_delete=models.CASCADE)
    access_token = models.TextField(max_length=100)
    access_key = models.TextField(max_length=100)
    screen_name = models.TextField(max_length=100, db_index=True)
    id_int = models.IntegerField()
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=200)
    profile_pic_url = models.URLField()
    followers_count = models.IntegerField()
    verified = models.BooleanField()
    profile_url = models.URLField()
    date_joined = models.DateTimeField()

    class Meta:
        unique_together = ('app', 'screen_name')

    def get_absolute_url(self):
        return "/dashboard/%s/%s/" % self.app.id, self.id


class Twitter_Task:
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField()
    status = models.TextField(max_length=20)
    completed_at = models.DateTimeField()
    twitterApp = models.ForeignKey(TwitterApp)
    TwitterApp_User = models.ForeignKey(TwitterApp_User)
