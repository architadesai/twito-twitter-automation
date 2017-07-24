from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse

from .forms import (
    RegisterApp,
    AccessApp
)

from .models import ApplicationData, ApplicationAccess

from tweepy import (
    OAuthHandler,
    API
)



def index(request):
    return render(request, 'home/index.html')


@login_required
def applicationlogin(request):

    form = RegisterApp(request.POST or None)

    if form.is_valid():

        instance = form.save(commit=False)
        instance.username = request.user
        instance.save()
        return HttpResponseRedirect('/user/%s/' % instance.appname)


    return render(request, 'home/appdata.html', {"form":form})


@login_required
def applicationaccess(request, appname):

    form = AccessApp(request.POST or None)

    if form.is_valid():

        instance = form.save(commit=False)

        try:

            auth = OAuthHandler(instance.consumerkey, instance.consumersecret)
            auth.set_access_token(instance.accesstoken, instance.accesssecret)
            auth.get_authorization_url()

            instance.appname = ApplicationData.objects.get(appname=appname)
            instance.username = request.user

            instance.save()
            return HttpResponse("Congratulations!! Your are logged in to Twitter account")

        except Exception as e:

            return HttpResponseNotFound("Error Occurred. Try Again. " + str(e))

    return render(request, 'home/appaccess.html', {"form": form})