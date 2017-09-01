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

    # def get_absolute_url(self):
    #     return "/dashboard/%s/" % self.id

    def __str__(self):
        return self.appName


    # def __unicode__(self):
    #     return self.appName


class AppAccess(models.Model):

    user = models.ForeignKey(User, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    accessToken = models.TextField(max_length=100)
    accessKey = models.TextField(max_length=100)


# class LocationSearch(models.Model):
#
#     user = models.ForeignKey(User, db_index=True)
#     AppName = models.ForeignKey(TwitterApp)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     radius = models.FloatField()
#     radiusUnit = models.CharField(max_length=2, default='km', choices=(('km','km'),('mi','mi')))
#     SearchTime = models.DateTimeField(auto_now=True)

#def get_user():



class TasksList(models.Model):


    user = models.ForeignKey(User, db_index=True)
    appName = models.ForeignKey(TwitterApp, db_index=True)
    taskName = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True, db_index=True)


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



        # class UserInfo(models.Model):
#
#     user = models.OneToOneField(User, db_index=True)
#     TwitterId = models.IntegerField()
#     UserName = models.CharField(max_length=100)
#     ScreenName = models.CharField(max_length=150)
#     friends =
#     followers =
#     TwitterProfile =
#     description =
#     tweets =
#     likes =