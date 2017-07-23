from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class ApplicationData(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    appname = models.CharField(max_length=200)
    consumerkey = models.CharField(max_length=200)
    consumertoken = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Application Info"
        #ConsumerKey and ConsumerToken should be regenerated in order to update,
        # if user manually change permissions in twitter.dev.api

    def __str__(self):
        return "%s and %s Application" %(self.username, self.appname)




class ApplicationAccess(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    appname = models.ForeignKey(ApplicationData, on_delete=models.CASCADE)
    accesstoken = models.CharField(max_length=200)
    accesskey = models.CharField(max_length=200)
    accesstime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Application Access Info"

    def __str__(self):
        return "%s is accessed at %s" %(self.appname, self.accesstime)



class UserActivity(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    appname = models.ForeignKey(ApplicationData, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)

    class Meta:
        verbose_name = "User Activity"

    def __str__(self):
        return "List of Activities in application %s" %(self.appname)
