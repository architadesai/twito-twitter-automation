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

from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

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

        # print(ResultObjects)

    except Exception as e:
        print(e)

    return ResultObjects, TaskObjects

def getAPI(consumerKey, consumerToken, accessKey, accessToken):

    try:

        auth = OAuthHandler(consumerKey, consumerToken)

        auth.set_access_token(accessKey, accessToken)

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


@task(name="likeTweet")
def likeTweet(userObj, appObj, api, tweetID, taskObj):

    #tweet id of tweet which should be like by user which is connected to api
    #         # if SearchId[i] not in likes_ids:
    #         #
    #         #     print("like", SearchId[i], end=" - ")
    #         #     print((api.create_favorite(SearchId[i])).id_str)  # create_favorite method returns status
    #         #     likes_ids.append(SearchId[i])
    #         #
    #         # else:
    #         #     print("already like", SearchId[i])
    #         # print("favorites...", likes_ids)


    try:
        print("like", tweetID, end=" - ")
        print((api.create_favorite(tweetID).id_str))   # create_favorite method returns status
        appendTaskLike(userObj, appObj, tweetID, taskObj)

    except Exception as e:

        print("Already like")
        pass


@task(name="followUser")
def followUser(userObj, appObj, api, userSName, toFollowUserID, taskObj):

    #userSName is user screen_name
    #toFollowUsers is id of all user which should be followed by userSName

    #     if _follow:
    #
    #         # if i not in friends_ids:
    #         #     print("follow", i, end=" - ")
    #         #     print(api.create_friendship(i).screen_name)  #follow specific user
    #         #     friends_ids.append(i)
    #         # else:
    #         #     print("already follow", i)
    #
    #         if (api.show_friendship(source_screen_name=username, target_id=i))[1].followed_by:
    #             print("Already follow ", i)
    #         else:
    #             print("follow", i, end=" - ")
    #             print(api.create_friendship(i).screen_name)  #follow specific user
    #
    #         #it doesn't return error if user is already following to destination user
    #             #and it works same without error whether user is following or not
    #             #so we don't require to change, can remove upper feature
    #         # try:
    #         #     print("follow", i, end=" - ")
    #         #     print(api.create_friendship(i).screen_name)  #follow specific user
    #         # except Exception as e:
    #         #     print("Already follow")
    #         #     pass



    if (api.show_friendship(source_screen_name=userSName, target_id=toFollowUserID))[1].followed_by:
        print("Already follow ", )

    else:
        print("follow", toFollowUserID, end=" - ")
        print(api.create_friendship(toFollowUserID).screen_name)  # follow specific user
        appendTaskFollow(userObj, appObj, toFollowUserID, taskObj)

@task(name="reTweetTweet")
def reTweetTweet(userObj, appObj, api, tweetID, taskObj):

    # tweet id of tweet which should be retweet by user which is connected to api


    try:
        print("retweet", end=" - ")
        print((api.retweet(tweetID)).id_str)  # retweet specific tweet
        appendTaskreTweet(userObj, appObj, tweetID, taskObj)

    except Exception as e:

        print("Already retweeted")
        pass