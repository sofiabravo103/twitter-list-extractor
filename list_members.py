#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import sys
import pickle
import tweepy
from time import sleep
from information_spec import *

MEMBERS_PICKLE_FILE = 'pickles/downloaded_lists_members.p'

def configure_tweepy():
  global api

  auth = tweepy.OAuthHandler(spec_consumer_key, spec_consumer_secret)
  auth.set_access_token(spec_access_token, spec_access_token_secret)
  api = tweepy.API(auth)

def load_data():
  global downloaded_lists_members

  if not os.path.isdir('pickles'):
    os.makedirs('pickles')
    downloaded_lists_members = {}
  else:
    members_file = open(MEMBERS_PICKLE_FILE,'rb')
    downloaded_lists_members = pickle.load(members_file)

def save_data():
  members_file = open(MEMBERS_PICKLE_FILE,'wb')
  pickle.dump(downloaded_lists_members, members_file)

def get_list_users(screen_name, list_name):
  ids = []
  try:
    for user in tweepy.Cursor(api.list_members,screen_name,list_name).items():
      ids.append(user.id)
    return ids
  except tweepy.error.TweepError as e:
    print '\t[DOWNLOAD ERROR] Error with data in list "{0}": {1}'.\
      format(list_name, e[0][0]['message'])
    if e[0][0]['code'] == 88:
      sys.stdout.write('Sleeping for 15 minutes...')
      sys.stdout.flush()
      sleep(900)
      sys.stdout.write(" and I'm back.")
      sys.stdout.flush()
      return get_list_users(screen_name, list_name)


def main():
  for list_id in spec_lists.keys():
    if list_id not in downloaded_lists_members:
      list_data = spec_lists[list_id]
      print 'Downloading list #{0}, name {1}...'.\
        format(list_id, list_data['list_name'])
      users = get_list_users(list_data['screen_name'], list_data['list_name'])
      if users is not None:
        downloaded_lists_members[list_id] = users        
        print 'Done'
        save_data()

if __name__ == '__main__':
  configure_tweepy()
  load_data()
  main()
