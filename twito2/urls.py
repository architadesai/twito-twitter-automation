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

    url(r'^login/$', applicationlogin, name="ApplicationLogin"),

    url(r'^user/(?P<appname>\w+)/$', applicationaccess, name="ApplicationAccess"),


]


######################UPDATE login link to specific user name ###############
######################UPDATE app link to specific app name###############