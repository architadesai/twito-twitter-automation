#import tablib
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
#from django.utils import timezone
from .models import (
    TwitterApp,

)

from .forms import (
    TwitterApp_Form,

)

import tweepy

login_url = '/'


def index(request):
    return render(request, 'index.html')


@login_required(login_url=login_url)
def dashboard(request):

    if request.method == 'POST':

        form = TwitterApp_Form(request.POST)

        # log form details here

        if form.is_valid():

            _consumerKey = request.POST['ConsumerKey'].strip()
            _consumerToken = request.POST['ConsumerToken'].strip()
            _access_token = request.POST['access_token'].strip()
            _access_key = request.POST['access_key'].strip()

            try:
                auth = tweepy.OAuthHandler(_consumerKey, _consumerToken)
                auth.get_authorization_url()

                auth.set_access_token(_access_token,_access_key)

                api = tweepy.API(auth)
                api.update_status('tweepy + oauth!')

                # if consumer token and Access Tokens are valid then only would go further

                app = form.save(commit=False)
                app.user = request.user
                app.save()

                return redirect('/dashboard/')

            except Exception as e:
                # log exception
                print(str(e))

                messages.warning(
                    request,
                    '''Error in Consumer Key/Toekn!
                    Please try again with correct Twitter App Credentials!''')

                return redirect('/dashboard/')
        else:
            print(form.errors)
            return redirect('/dashboard/')

    else:

        form = TwitterApp_Form()

        apps = TwitterApp.objects.filter(
            user=request.user).order_by('-created_at')

        return render(request, 'dashboard.html', {'apps': apps, 'form': form})


@login_required(login_url=login_url)
def appPage(request, app_id):

    app = get_object_or_404(TwitterApp, id=app_id, user=request.user)

    users = TwitterApp.objects.filter(AppName=app)

    return render(request, 'app.html', {'app': app, 'users': users})


@login_required(login_url=login_url)
def deleteTwitterApp(request, app_id):

    get_object_or_404(TwitterApp, id=app_id, user=request.user).delete()

    return redirect('/dashboard/')

