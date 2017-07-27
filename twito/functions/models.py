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
    access_token = models.TextField(max_length=100, default="Not Assigned")
    access_key = models.TextField(max_length=100, default="Not Assigned")

    def get_absolute_url(self):
        return "/dashboard/%s/" % self.id

class LocationSearch(models.Model):

    user = models.ForeignKey(User, db_index=True)
    AppName = models.ForeignKey(TwitterApp)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    radiusUnit = models.CharField(max_length=2, default='km', choices=(('km','km'),('mi','mi')))

