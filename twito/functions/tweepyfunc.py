from tweepy import(
    OAuthHandler,
    API,
    Cursor,
)

from .models import (
    TasksList,
    TaskLike,
    TaskFollow,
    TaskreTweet
)


def searchUsers(api, queryUser, uniqueUser=False, total_search_result = 10, total_task_result=10):

    ResultObjects = []
    TaskObjects = []
    print(queryUser)

    try:
        for UserObject in Cursor(api.search_users, q=queryUser).items(total_search_result):

            ResultObjects.append(UserObject)

            if len(TaskObjects) < total_task_result:

                if uniqueUser:
                    if UserObject.user.id_str not in TaskObjects:
                        TaskObjects.append(UserObject.id_str)
                else:
                    TaskObjects.append(UserObject.id_str)

        #print(ResultObjects)
    except Exception as e:
        print(e)

    return ResultObjects, TaskObjects


def searchTweets(api, queryKeyword, language, location,
                 uniqueUser=False, total_search_result = 10, total_task_result=10):



    ResultObjects = []
    TaskObjects = {}

    print(queryKeyword)
    print("fdsfdsfs")

    try:
        for StatusObject in Cursor(api.search, q=queryKeyword, lang=language, geocode=location).items(total_search_result):

            ResultObjects.append(StatusObject)

            if len(TaskObjects.keys()) < total_task_result:

                if uniqueUser:
                    if StatusObject.user.id_str not in TaskObjects.keys():
                        TaskObjects[StatusObject.user.id_str] = str(StatusObject.id_str)
                else:
                    TaskObjects[StatusObject.user.id_str] = str(StatusObject.id_str)

        # print(ResultObjects)

    except Exception as e:
        print(e)

    return ResultObjects, TaskObjects



def getAPI(consumer_key, consumer_token,  access_token, access_key):

    try:
        auth = OAuthHandler(consumer_key, consumer_token)
        auth.get_authorization_url()

        auth.set_access_token(access_token, access_key)

        api = API(auth)
        twitterName = (api.me()).name

        return api

        # if consumer token and Access Tokens are valid then only would go further
    except Exception as e:

        print(str(e))
        return False


def appendTaskList(userObj, appObj, taskName):

    t = TasksList(user=userObj, AppName=appObj, TasksName=taskName)
    t.save()

def appendTaskLike(userObj, appObj, tweetID):

    t = TaskLike(user=userObj, AppName=appObj, tweetID=tweetID)
    t.save()

def appendTaskFollow(userObj, appObj, followUserID):

    t = TaskFollow(user=userObj, AppName=appObj, followUserID=followUserID)
    t.save()

def appendTaskreTweet(userObj, appObj, tweetID):

    t = TaskreTweet(user=userObj, AppName=appObj, tweetID=tweetID)
    t.save()



def likeTweet(userObj, appObj, api, tweetID):

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
        appendTaskLike(userObj, appObj, tweetID)

    except Exception as e:

        print("Already like")
        pass



def followUser(userObj, appObj, api, userSName, toFollowUserID):

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
        appendTaskFollow(userObj, appObj, toFollowUserID)


def reTweetTweet(userObj, appObj, api, tweetID):

    # tweet id of tweet which should be retweet by user which is connected to api


    try:
        print("retweet", end=" - ")
        print((api.retweet(tweetID)).id_str)  # retweet specific tweet
        appendTaskreTweet(userObj, appObj, tweetID)

    except Exception as e:

        print("Already retweeted")
        pass