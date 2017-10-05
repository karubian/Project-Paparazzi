import tweepy

consumer_key = "iJp4X3rXDw59Wk48dS9o8Krgr"
consumer_secret = "NumnqCgZvwqpF402JbcgCWPJPR44uThju83yhyF3ewjXES3LoC"
access_key = "916015993016717313-1C329HlKA5tbAjFYvTnVXzG6rk8PNLz"
access_secret = "JmYVfB8zABEminF0JKXtK5GDZTEtjGA1gO3rQ3jHrCxkQ"

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    auth.get_authorization_url()
    api = tweepy.API(auth)
except tweepy.TweepError:
    print('Hata')

user = api.get_user("kesinlikleburak")  # kullanıcıyı ogunal00 olarak seçtik
i=0
public_tweets = api.user_timeline(screen_name = "projectpaparazz",count=10) # ogunal00 kullanıcısının 5 adet tweeti
for tweet in public_tweets:
        print(tweet.created_at)
        print(i)
        i=i+1
        print(tweet)
# print(user)