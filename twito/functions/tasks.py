from __future__ import absolute_import, unicode_literals
import time
import tweepy
from random import randint
from celery.decorators import task
from .models import TwitterApp, TwitterApp_User


def get_twitter_user(user, app_id, user_id):

    app = TwitterApp.objects.get(id=app_id, user=user)
    auth = tweepy.OAuthHandler(app.ConsumerKey, app.ConsumerToken)
    app_user = TwitterApp_User.objects.get(screen_name=user_id, app=app)
    auth.set_access_token(app_user.access_token, app_user.access_key)

    tw_user = tweepy.API(auth, compression=True, wait_on_rate_limit=True)

    return tw_user


@task
def follow_csv(user, app_id, user_id, target):

    tw_user = get_twitter_user(user, app_id, user_id)

    for person in target[:20000]:
        tw_user.get_user(person).follow()
        time.sleep(randint(30, 300))


@task
def follow_followers_of(user, app_id, user_id, target, amount):

    tw_user = get_twitter_user(user, app_id, user_id)

    for follower_id in tweepy.Cursor(tw_user.followers_ids,
                                     id=target).items(int(float(amount))):
        tw_user.get_user(follower_id).follow()
        time.sleep(randint(30, 300))


@task
def follow_people_with_hash(user, app_id, user_id, target):

    tw_user = get_twitter_user(user, app_id, user_id)

    for page in range(1, 26):
        for people in tw_user.search_users(target, page=page):
            tw_user.get_user(people).follow()
            time.sleep(randint(30, 300))
        time.sleep(300)

    # log the result


@task
def follow_people_list(user, app_id, user_id, username, listname):

    tw_user = get_twitter_user(user, app_id, user_id)

    for page in tweepy.Cursor(tw_user.list_members,
                              username, listname).pages():
        for person in page:
            person.follow()
            time.sleep(randint(30, 300))
        time.sleep(randint(30, 300))


@task
def unfollow_all(user, app_id, user_id):

    tw_user = get_twitter_user(user, app_id, user_id)

    for page in tweepy.Cursor(tw_user.followers_ids).pages():
        for person in page:
            tw_user.destroy_friendship(person)
            time.sleep(randint(30, 300))


@task
def unfollow_people_list(user, app_id, user_id, username, listname):

    tw_user = get_twitter_user(user, app_id, user_id)

    for page in tweepy.Cursor(tw_user.list_members,
                              username, listname).pages():
        for person in page:
            tw_user.destroy_friendship(person)
            time.sleep(randint(30, 300))
        time.sleep(randint(20, 200))


@task
def unfollow_last_custom(user, app_id, user_id, amount):

    tw_user = get_twitter_user(user, app_id, user_id)

    for person in tweepy.Cursor(tw_user.followers_ids).items(
            int(float(amount))):
        tw_user.destroy_friendship(person)
        time.sleep(randint(30, 300))


@task
def unfollow_csv(user, app_id, user_id, target):

    tw_user = get_twitter_user(user, app_id, user_id)

    for person in target[:20000]:
        tw_user.destroy_friendship(person)
        time.sleep(randint(30, 300))
