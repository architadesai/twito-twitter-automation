from django.conf.urls import include, url
from django.contrib import admin

from home.views import (
    index,
    applicationlogin,
    applicationaccess,
)

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index, name="HomePage"),

    url(r'^dashboard/$', applicationlogin, name="ApplicationLogin"),

    url(r'^dashboard/(?P<appname>\w+)/$', applicationaccess, name="ApplicationAccess"),


]


######################UPDATE login link to specific user name ###############
######################UPDATE app link to specific app name###############
############Also to make sure that login user should not be able to check other user acc by line####################
################Add login page to beginning, instead of admin login#####################