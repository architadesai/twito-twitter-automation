import tablib
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import TwitterApp, TwitterApp_User
from .forms import TwitterApp_Form, csv_file
from .tasks import *
import tweepy

# login_url 'variable'
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

            try:
                auth = tweepy.OAuthHandler(_consumerKey, _consumerToken)
                auth.get_authorization_url()

                # if consumer token are valid then only would go further

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

    users = TwitterApp_User.objects.filter(app=app)

    return render(request, 'app.html', {'app': app, 'users': users})


@login_required(login_url=login_url)
def deleteTwitterApp(request, app_id):

    get_object_or_404(TwitterApp, id=app_id, user=request.user).delete()

    return redirect('/dashboard/')


@login_required(login_url=login_url)
def getTwitterAuthURL(request, app_id):

    app = get_object_or_404(TwitterApp, id=app_id, user=request.user)

    callback_url = 'http://twito.co/dashboard/' + \
        str(app_id) + '/callback/'

    auth = tweepy.OAuthHandler(
        app.ConsumerKey, app.ConsumerToken, callback_url)

    try:
        return redirect(auth.get_authorization_url())
    except Exception as e:
        print(e)
        messages.warning(
            request, 'Problem connecting with Twitter! Try again.')
        return redirect(app.get_absolute_url())


@login_required(login_url=login_url)
def twitterCallback(request, app_id):

    app = get_object_or_404(TwitterApp, id=app_id, user=request.user)

    auth = tweepy.OAuthHandler(app.ConsumerKey, app.ConsumerToken)

    oauth_token = request.GET.get('oauth_token', '')
    oauth_verifier = request.GET.get('oauth_verifier', '')

    auth.request_token = {'oauth_token': oauth_token,
                          'oauth_token_secret': oauth_verifier}

    try:
        auth.get_access_token(verifier=oauth_verifier)
    except Exception as e:
        # log this error
        print(str(e))
        messages.warning('Could not connect to twitter! Please try again.')
        return redirect(app.get_absolute_url())

    user = tweepy.API(auth)

    try:
        me = user.me()
    except Exception as e:
        # log this error
        print(str(e))
        messages.warning('Not able to get your info from Twitter! Try again.')
        return redirect(app.get_absolute_url())

    TwitterAppUser = TwitterApp_User()

    try:
        TwitterAppUser.user = request.user
        TwitterAppUser.app = app
        TwitterAppUser.access_token = auth.access_token
        TwitterAppUser.access_key = auth.access_token_secret
        TwitterAppUser.screen_name = me.screen_name
        TwitterAppUser.id_int = me.id
        TwitterAppUser.name = me.name
        TwitterAppUser.description = me.description
        TwitterAppUser.profile_pic_url = me.profile_image_url_https.replace(
            '_normal', '')
        TwitterAppUser.followers_count = me.followers_count
        TwitterAppUser.verified = me.verified
        TwitterAppUser.location = me.location
        TwitterAppUser.date_joined = timezone.make_aware(me.created_at)
    except Exception as e:
        # log exception here
        print(str(e))
        messages.warning('Not able to create your user! Try again.')

        redirect(app.get_absolute_url())

    try:
        TwitterAppUser.save()
    except Exception as e:
        print(e)
        messages.warning(
            request, '''If you are trying to add same user again in the same app,
            sorry but that doesn't make sense!''')
        return redirect(app.get_absolute_url())

    return redirect(app.get_absolute_url())


@login_required(login_url=login_url)
def taskPage(request, app_id, user_id):

    if request.method == 'POST':

        action = request.POST.get('action')
        sub_action = request.POST.get('sub_action')

        # log details here

        if action == 'follow':

            if sub_action == 'follow-csv':

                form = csv_file(request.POST, request.FILES)
                if form.is_valid():
                    imported_data = tablib.Dataset(
                        form.cleaned_data['csv_file'].read(
                        ).decode('utf-8').split('\n'))
                    messages.success(request, 'Success! Scheduled the task.')
                    follow_csv.delay(request.user, app_id,
                                     user_id, imported_data.dict[0][:-1])
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')
                else:
                    messages.warning(request, 'Error! Try again.')
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'follow-followers-of':

                target = request.POST.get('target')
                amount = request.POST.get('amount')

                if target and amount:
                    follow_followers_of.delay(
                        request.user, app_id, user_id, target, amount)
                    messages.success(request, 'Success! Scheduled the task.')
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'follow-people-of-list':

                listname = request.POST.get('listname')
                username = request.POST.get('username')

                if target and amount and amount:
                    follow_people_list.delay(
                        request.user, app_id, user_id,
                        username, listname)
                    messages.success(request, 'Success! Scheduled the task.')
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'follow-people-with-hash':

                target = request.POST.get('target')

                if target:
                    follow_people_with_hash.delay(
                        request.user, app_id, user_id, target)
                    messages.success(request, 'Success! Scheduled the task.')
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')

        if action == 'unfollow':

            if sub_action == 'unfollow-all':
                unfollow_all.delay(request.user, app_id, user_id)
                messages.success(request, 'Success! Scheduled the task.')
                redirect('/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'unfollow-people-of-list':
                username = request.POST.get('username')
                listname = request.POST.get('listname')
                unfollow_people_list.delay(
                    request.user, app_id, user_id, username, listname)
                messages.success(request, 'Success! Scheduled the task.')
                return redirect('/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'unfollow-last-custom':
                amount = request.POST.get('amount')
                unfollow_last_custom.delay(
                    request.user, app_id, user_id, amount)
                messages.success(request, 'Success! Scheduled the task.')
                return redirect('/dashboard/' + app_id + '/' + user_id + '/')

            if sub_action == 'unfollow-custom-csv':
                form = csv_file(request.POST, request.FILES)

                if form.is_valid():
                    imported_data = tablib.Dataset(
                        form.cleaned_data['csv_file'].read(
                        ).decode('utf-8').split('\n'))

                    unfollow_custom_csv.delay(request.user, app_id, user_id,
                                              imported_data.dict[0][:-1])
                    messages.success(request, 'Success! Scheduled the task.')
                    return redirect(
                        '/dashboard/' + app_id + '/' + user_id + '/')

        messages.warning('Oops! Something went wrong!')

        return redirect('/dashboard/' + app_id + '/' + user_id + '/')

    else:
        app = get_object_or_404(TwitterApp, id=app_id, user=request.user)
        tw_user = get_object_or_404(
            TwitterApp_User, app=app, screen_name=user_id)

        return render(request, 'user.html', {'app': app, 'twuser': tw_user})


@login_required(login_url=login_url)
def deleteAppUser(request, app_id, user_id):

    get_object_or_404(TwitterApp_User, id=user_id,
                      user=request.user).delete()

    return redirect('/dashboard/' + app_id + '/')
