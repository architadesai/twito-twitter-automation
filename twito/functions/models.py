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

class AppAccess(models.Model):

    user = models.ForeignKey(User, db_index=True)
    AppName = models.ForeignKey(TwitterApp, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    access_token = models.TextField(max_length=100)
    access_key = models.TextField(max_length=100)


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


    #user = models.ForeignKey(User, db_index=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, db_index=True)
    AppName = models.ForeignKey(TwitterApp, db_index=True)
    TaskName = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskLike(models.Model):

    user = models.ForeignKey(User, db_index=True)
    TaskName = models.ForeignKey(TasksList, db_index=True)
    AppName = models.ForeignKey(TwitterApp, db_index=True)
    tweetID = models.CharField(max_length=30)
    Time = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskFollow(models.Model):

    user = models.ForeignKey(User, db_index=True)
    TaskName = models.ForeignKey(TasksList, db_index=True, null=True)
    AppName = models.ForeignKey(TwitterApp, db_index=True)
    followUserID = models.CharField(max_length=30)
    Time = models.DateTimeField(auto_now_add=True, db_index=True)


class TaskreTweet(models.Model):

    user = models.ForeignKey(User, db_index=True)
    TaskName = models.ForeignKey(TasksList, db_index=True)
    AppName = models.ForeignKey(TwitterApp, db_index=True)
    tweetID = models.CharField(max_length=30)
    Time = models.DateTimeField(auto_now_add=True, db_index=True)



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