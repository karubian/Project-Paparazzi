# -*- coding: utf-8 -*-
import tweepy
import twitter_config as tw



try:
    auth = tweepy.OAuthHandler(tw.consumer_key, tw.consumer_secret)
    auth.set_access_token(tw.access_key, tw.access_secret)
    auth.get_authorization_url()
    api = tweepy.API(auth)
except tweepy.TweepError:
    print('Hata')

user = api.get_user("projectpaparazz")
i=0
public_tweets = api.user_timeline(screen_name = "projectpaparazz",count=10)
for tweet in public_tweets:
        print(tweet.created_at)
        print(i)
        i=i+1
        print(tweet)
# print(user)