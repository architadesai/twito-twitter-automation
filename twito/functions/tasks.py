from celery.decorators import task
#from celery.utils.log import get_task_logger

#logger = get_task_logger(__name__)

from .models import (
    TwitterApp,
    TasksList,

)

from django.contrib.auth.models import User

from .tweepyfunc import (

    followUser,
    likeTweet,
    reTweetTweet,
    getAPI,


)

#you can not pass django-models as argument of celery task
#so either you can pass primary key and then refetch object again
#or you can use pickle library to convert query obj in to string and then pass to tasks functions

@task(name="likeAllTweets")
def likeAllTweets(userObjID, twitoAppObjID, taskObjID, taskIDs):


    userObj = User.objects.get(id=userObjID)
    twitoAppObj = TwitterApp.objects.get(id=twitoAppObjID, user=userObj)
    taskObj = TasksList.objects.get(id=taskObjID)
    # accssObj = AppAccess.objects.get(user=userObj, appName=twitoAppObj)

    api = getAPI(userObj, twitoAppObj)

    if api:
        for i in taskIDs.values():
            likeTweet(userObj, twitoAppObj, api, i, taskObj)
        print("Successfully performed like ")
    else:
        print("Error occurred..")


@task(name="followAllUsers")
def followAllUsers(userObjID, twitoAppObjID, taskObjID, taskIDs):

    userObj = User.objects.get(id=userObjID)
    twitoAppObj = TwitterApp.objects.get(id=twitoAppObjID, user=userObj)
    taskObj = TasksList.objects.get(id=taskObjID)

    api = getAPI(userObj, twitoAppObj)

    if api:
        for i in taskIDs:
            followUser(userObj, twitoAppObj, api, api.me().screen_name, i, taskObj)
        print("Successfully performed follow")
    else:
        print("Error occurred..")


@task(name="reTweetAllTweets")
def reTweetAllTweets(userObjID, twitoAppObjID, taskObjID, taskIDs):

    userObj = User.objects.get(id=userObjID)
    twitoAppObj = TwitterApp.objects.get(id=twitoAppObjID, user=userObj)
    taskObj = TasksList.objects.get(id=taskObjID)

    api = getAPI(userObj, twitoAppObj)

    if api:
        for i in taskIDs.values():
            reTweetTweet(userObj, twitoAppObj, api, i, taskObj)
        print("Successfully performed retweet")
    else:
        print("Error occurred..")
