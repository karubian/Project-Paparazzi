from instagram.client import InstagramAPI

access_token = "6168565408.1677ed0.fb723d37d2a5470cb54dc279942a42cb"
client_secret = "7d86390e8a3d42c7a0197ab1e8fcd079"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="berksefkatli", count=10)
for media in recent_media:
    print(media.caption.text)


