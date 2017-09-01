from __future__ import unicode_literals

from django.db import models
from .random_primary import RandomPrimaryIdModel as RandomPrimaryId
from django.contrib.auth.models import User
# Create your models here.


class TwitterApp(RandomPrimaryId):

    user = models.ForeignKey(User, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    appName = models.TextField(max_length=50)
    consumerKey = models.TextField(max_length=100)
    consumerToken = models.TextField(max_length=100)


    def __str__(self):
        return self.appName


class AppAccess(models.Model):

    user = models.ForeignKey(User, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    accessToken = models.TextField(max_length=100)
    accessKey = models.TextField(max_length=100)



class TasksList(models.Model):


    user = models.ForeignKey(User, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    taskName = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.taskName


class TaskLike(models.Model):

    user = models.ForeignKey(User, db_index=True)
    taskName = models.ForeignKey(TasksList, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    tweetID = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskFollow(models.Model):

    user = models.ForeignKey(User, db_index=True)
    taskName = models.ForeignKey(TasksList, db_index=True, null=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    followUserID = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskreTweet(models.Model):

    user = models.ForeignKey(User, db_index=True)
    taskName = models.ForeignKey(TasksList, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    tweetID = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True, db_index=True)



