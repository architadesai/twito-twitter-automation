from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from functions import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='homepage'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^dashboard/(?P<app_id>[\w]+)/$',
        views.appPage, name='twitterApp'),

    url(r'^dashboard/(?P<app_id>[\w]+)/delete/$',
        views.deleteTwitterApp, name='twitterApp'),

    # url(r'^dashboard/(?P<app_id>[\w]+)/search/$',
    #     views.Search, kwargs={'location':True}, name='SearchByLocation'),
    #
    # url(r'^dashboard/(?P<app_id>[\w]+)/search/$',
    #     views.Search, kwargs={'location':False}, name='SearchByKeyword'),

    url(r'^dashboard/(?P<app_id>[\w]+)/search/$',
        views.Search, name='Search'),


    url(r'^dashboard/(?P<app_id>[\w]+)/searchuser/$',
        views.searchUser, name='searchuser'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
