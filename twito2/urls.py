from django.conf.urls import include, url
from django.contrib import admin

from home.views import (
    index,
    applicationlogin,
)

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index, name="HomePage"),

    url(r'^login/', applicationlogin, name="ApplicationLogin"),

]
