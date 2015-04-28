#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pickle
import tweepy
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
  for user in tweepy.Cursor(api.list_members,screen_name,list_name).items():
    ids.append(user.id)

  return ids

def main():
  pass

if __name__ == '__main__':
  configure_tweepy()
  load_data()
  main()
