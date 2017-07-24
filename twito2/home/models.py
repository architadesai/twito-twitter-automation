from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class ApplicationData(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    appname = models.CharField(max_length=200, primary_key=True)

    class Meta:
        verbose_name = "Application Info"
        #ConsumerKey and ConsumerToken should be regenerated in order to update,
        # if user manually change permissions in twitter.dev.api

    def __str__(self):
        return "%s %s " %(self.username, self.appname)




class ApplicationAccess(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    appname = models.ForeignKey(ApplicationData, on_delete=models.CASCADE)
    consumerkey = models.CharField(max_length=200, default="")
    consumersecret = models.CharField(max_length=200, default="")
    accesstoken = models.CharField(max_length=200, default="")
    accesssecret = models.CharField(max_length=200, default="")
    accesstime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Application Access Info"

    def __str__(self):
        return "%s" %(self.appname)



class UserActivity(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    appname = models.ForeignKey(ApplicationData, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)

    class Meta:
        verbose_name = "User Activity"

    def __str__(self):
        return "List of Activities in application %s" %(self.appname)
