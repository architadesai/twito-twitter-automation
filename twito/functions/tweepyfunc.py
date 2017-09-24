from tweepy import(
    OAuthHandler,
    API,
    Cursor,
)

from .models import (
    TasksList,
    TaskLike,
    TaskFollow,
    TaskreTweet,
    TwitterApp,
    AppAccess,
)


def searchUsers(api, queryUser, uniqueUser=False, totalSearchResult = 10, totalTaskResult=10):

    ResultObjects = []
    TaskObjects = []

    print("query = ",queryUser)

    try:
        for UserObject in Cursor(api.search_users, q=queryUser).items(totalSearchResult):
            ResultObjects.append(UserObject)

            if len(TaskObjects) < totalTaskResult:
                if uniqueUser:
                    if UserObject.id_str not in TaskObjects:
                        TaskObjects.append(UserObject.id_str)
                else:
                    TaskObjects.append(UserObject.id_str)

    except Exception as e:
        print(e)
    return ResultObjects, TaskObjects

def searchTweets(api, queryKeyword, language, location,
                 uniqueUser=False, totalSearchResult = 10, totalTaskResult=10):

    ResultObjects = []
    TaskObjects = {}

    print("keyword = ",queryKeyword)
    print("location = ",location)

    try:
        for StatusObject in Cursor(api.search, q=queryKeyword, lang=language, geocode=location).items(totalSearchResult):
            ResultObjects.append(StatusObject)

            if len(TaskObjects.keys()) < totalTaskResult:
                if uniqueUser:
                    if StatusObject.user.id_str not in TaskObjects.keys():
                        TaskObjects[StatusObject.user.id_str] = str(StatusObject.id_str)
                else:
                    TaskObjects[StatusObject.user.id_str] = str(StatusObject.id_str)

    except Exception as e:
        print(e)
    return ResultObjects, TaskObjects


def getAPI(userObj, twitoAppObj):

    try:
        accObj = AppAccess.objects.get(user=userObj, appName=twitoAppObj)
        auth = OAuthHandler(twitoAppObj.consumerKey, twitoAppObj.consumerToken)
        auth.set_access_token(accObj.accessToken, accObj.accessKey)
        api = API(auth)
        twitterName = (api.me()).name
        return api

        # if consumer token and Access Tokens are valid then only would go further
    except Exception as e:
        print(str(e))
        return False

def appendTaskList(userObj, appObj, taskName, Obj=False):

    t = TasksList(user=userObj, appName=appObj, taskName=taskName)
    t.save()
    if Obj:
        return t

def appendTaskLike(userObj, appObj, tweetID, taskObj):

    t = TaskLike(user=userObj, appName=appObj, tweetID=tweetID, taskName=taskObj)
    t.save()

def appendTaskFollow(userObj, appObj, followUserID, taskObj):

    t = TaskFollow(user=userObj, appName=appObj, followUserID=followUserID, taskName=taskObj)
    t.save()

def appendTaskreTweet(userObj, appObj, tweetID, taskObj):

    t = TaskreTweet(user=userObj, appName=appObj, tweetID=tweetID, taskName=taskObj)
    t.save()


def likeTweet(userObj, appObj, api, tweetID, taskObj):

    try:
        print("like")
        print((api.create_favorite(tweetID).id_str))   # create_favorite method returns status
        appendTaskLike(userObj, appObj, tweetID, taskObj)

    except Exception as e:
        print("Already like")
        pass


def followUser(userObj, appObj, api, userSName, toFollowUserID, taskObj):

    try:
        print("follow")
        print(api.create_friendship(toFollowUserID).screen_name)  #follow specific user
    except Exception as e:
        print("Already follow")
        pass

def reTweetTweet(userObj, appObj, api, tweetID, taskObj):

    # tweet id of tweet which should be retweet by user which is connected to api
    try:
        print("retweet")
        print((api.retweet(tweetID)).id_str)  # retweet specific tweet
        appendTaskreTweet(userObj, appObj, tweetID, taskObj)

    except Exception as e:
        print("Already retweeted")
        pass