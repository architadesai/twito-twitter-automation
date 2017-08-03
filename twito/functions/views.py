
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    TwitterApp,
    TasksList,

)


from .forms import (
    TwitterApp_Form,
    SearchLocation_Form,
)

from tweepy import(
    OAuthHandler,
	API,
	Cursor,
)


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
                auth = OAuthHandler(_consumerKey, _consumerToken)
                auth.get_authorization_url()

                auth.set_access_token(_access_token,_access_key)

                api = API(auth)
                twitterName = (api.me()).name

                # if consumer token and Access Tokens are valid then only would go further

                app = form.save(commit=False)
                app.user = request.user
                app.save()

                t = TasksList(user=request.user, AppName=app, TaskName="Application Created")
                t.save()

                return redirect('/dashboard/')

            except Exception as e:
                # log exception
                print(str(e))

                messages.warning(
                    request,
                    '''Error in Consumer Key/Token!
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


    if request.method == 'POST':

        form = SearchLocation_Form(request.POST)


        if form.is_valid():

            _keyword = request.POST['keyword']
            _lang = request.POST['lang']
            _latitude = request.POST['latitude']
            _longitude = request.POST['longitude']
            _radius = request.POST['radius']
            _radiusUnit = request.POST['radiusUnit']

            try:

                request.session['keyword'] = _keyword
                request.session['lang'] = _lang
                request.session['latitude'] = _latitude
                request.session['longitude'] = _longitude
                request.session['radius'] = _radius
                request.session['radiusUnit'] = _radiusUnit

                # TwitoApp = get_object_or_404(TwitterApp, id=app_id, user=request.user)
                #
                # app = form.save(commit=False)
                # app.user = request.user
                # app.AppName = TwitoApp
                # app.save()

                return redirect('/dashboard/' + app_id + '/search/')


                # auth = OAuthHandler(TwitoApp.ConsumerKey, TwitoApp.ConsumerToken)
                # auth.get_authorization_url()
                #
                # auth.set_access_token(TwitoApp.access_token, TwitoApp.access_key)
                #
                # api = API(auth)

                # StatusObjects = api.search(geocode=str(_latitude) + "," +
                #                                    str(_longitude) + "," +
                #                                    (str(_radius) + _radiusUnit)
                #                            )


                #return render(request, 'searchlocation.html', {'status': StatusObjects})
                #return redirect('/dashboard/'+app_id+'/'+'search/')

                # authenticated_user = api.me().screen_name
                #
                # trends = api.trends_available()
                # followers = api.followers_ids(authenticated_user)
                # friends = api.friends_id(authenticated_user)



            except Exception as e:

                print(e)
                return redirect('/dashboard/'+app_id+'/')
        else:
            print(form.errors)
            return redirect('/dashboard/'+app_id+'/')

    else:

        TwitoApp = get_object_or_404(TwitterApp, id=app_id, user=request.user)

        auth = OAuthHandler(TwitoApp.ConsumerKey, TwitoApp.ConsumerToken)
        auth.get_authorization_url()

        auth.set_access_token(TwitoApp.access_token, TwitoApp.access_key)

        api = API(auth)

        username = (api.me()).screen_name

        #trends = api.trends_available()
        followers = api.followers(username)  #returns user object
        friends = api.friends(username)      #returns user object
        tweets = api.user_timeline()             #returns status object
        #lists =
        likes = api.favorites(username)          #returns status object
        #messages = api.direct_messages()
        tasks = TasksList.objects.filter(AppName=TwitoApp)      #returns TaskList objects as Queryset


        return render(request, 'app.html', {'app': TwitoApp, 'followers':followers,
                                                  'friends':friends,'tweets':tweets,'likes':likes,
                                                  'tasks':tasks})






@login_required(login_url=login_url)
def searchLocationwise(request, app_id):

    try:


        app = get_object_or_404(TwitterApp, id=app_id, user=request.user)

        t = TasksList(user=request.user, AppName=app, TaskName="Search by User")
        t.save()

        auth = OAuthHandler(app.ConsumerKey, app.ConsumerToken)
        auth.get_authorization_url()

        auth.set_access_token(app.access_token, app.access_key)

        api = API(auth)

        arg_key = request.session.get('keyword')
        arg_lang = request.session.get('lang')
        arg_geo = str(request.session.get('latitude')) + "," +\
              str(request.session.get('longitude')) + "," +\
              (str(request.session.get('radius')))+\
              (request.session.get('radiusUnit'))


        StatusObjects = []

        for StatusObject in Cursor(api.search,q=arg_key,lang=arg_lang,geocode=arg_geo).items(20):
            StatusObject.user.profile_image_url_https=StatusObject.user.profile_image_url_https.replace('_normal','')
            StatusObjects.append(StatusObject)

        #User Object is In Status Object

        return render(request, 'searchlocation.html', {'status': StatusObjects,'app':app})

    except Exception as e:

        print(e)
        return redirect('/dashboard/'+app_id+'/')



@login_required(login_url=login_url)
def deleteTwitterApp(request, app_id):


    app = get_object_or_404(TwitterApp, id=app_id, user=request.user)

    t = TasksList(user=request.user, AppName=app, TaskName="Application Deleted")
    t.save()

    app.delete()

    return redirect('/dashboard/')


    # https://twitter.com/narendramodi/status/891865991503806464
    # https://twitter.com/Devchan39963044

    #####################MAKE USER AWARE OF ERROR SHOW ERROR MESSAGE BY POP UP MENU ####################
#DONE ###################ADD CHOOSE FIELD in radius Unit(km or mi)#############################
########################PAGINATION IN RESULT TWEETS#################################
#DONE #########################CLEAR PROFILE PHOTO#################################
############################ALL AUTH#############################################
##############MAKE SPECIFIC FIELD OF FORM AS REQUIRED##########################
##################PROVIDE CHECKBOX FOR KEYWORD AND LANG QUERY#####################
######################EVEN USER AND APP IS DELETED TASK TABLE SHOULD CONTAIN THEIR RECORDS###################
#################FOR LOOP IS REPEATED IN APP.HTML FOR SAME STATUS OR SAME USER OBJECT REMOVE IT####################




##########################THINGS TO DISPLAY##############################
    #authenticated user's profile #me()
    #User of Application(More than one user possible for one application)
    #followers    #followers_ids
    # #when particular user is clicked #get_user (returns user all info)
    #friends       #friends_ids
    #User of Their App (they might or might not be either followers or friends)
    #list of tasks (our Task database objects )
    #search by location  #search
    #search by tag/message/username/tweet and specific language #search_user  #search
    #Direct Messages (Sent by me && Sent to me) #direct_messages #sent_direct_messages
