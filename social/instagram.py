# -*- coding: utf-8 -*-
import requests

APP_ACCESS_TOKEN = '6168565408.4a4eeb7.ccac4ddd5dbd474085db8c6d99c4d32e'
BASE_URL = 'https://api.instagram.com/v1/'


def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
  print('GET request url : %s' % request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print('Username: %s' % (user_info['data']['username']))
      print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
      print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
      print('No. of posts: %s' % (user_info['data']['counts']['media']))
    else:
      print('User does not exist!')
  else:
    print ('Status code other than 200 received!')


def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print('GET request url : %s' % (request_url))
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      return user_info['data'][0]['id']
    else:
      return None
  else:
    print('Status code other than 200 received!')
    exit()

def get_user_info(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print('User does not exist!')
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print('GET request url : %s' % (request_url))
  user_info = requests.get(request_url).json()
  print(user_info)
get_user_info("berksefkatli")

self_info()