#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import os
import pickle
import random
import time
import tweepy
from time import sleep
from information_spec import *

MEMBERS_PICKLE_FILE = 'pickles/downloaded_lists_members.p'
MEMBERS_EXPORTED_PICKLE_FILE = 'pickles/exported_lists_members.p'
TIME = str(time.time()).split('.')[0]
TXT_FILE = 'exports/export_{0}.txt'.format(TIME)

def configure_tweepy():
  global api

  auth = tweepy.OAuthHandler(spec_consumer_key, spec_consumer_secret)
  auth.set_access_token(spec_access_token, spec_access_token_secret)
  api = tweepy.API(auth)

def load_data():
  global downloaded_lists_members
  global exported_lists_members

  # pickle load
  if not os.path.isdir('pickles'):
    os.makedirs('pickles')

  if not os.path.isfile(MEMBERS_PICKLE_FILE):
    # create downloaded users pickle file
    downloaded_lists_members = {}
    d_members_file = open(MEMBERS_PICKLE_FILE,'wb')
    pickle.dump(downloaded_lists_members, d_members_file)    
  else:
    d_members_file = open(MEMBERS_PICKLE_FILE,'rb')
    downloaded_lists_members = pickle.load(d_members_file)

  if not os.path.isfile(MEMBERS_EXPORTED_PICKLE_FILE):
    # create exported users pickle file
    exported_lists_members = {}
    e_members_file = open(MEMBERS_EXPORTED_PICKLE_FILE,'wb')
    pickle.dump(exported_lists_members, e_members_file)
  else:
    e_members_file = open(MEMBERS_EXPORTED_PICKLE_FILE,'rb')
    exported_lists_members = pickle.load(e_members_file)

  d_members_file.close()
  e_members_file.close()

  # exports directory creation
  if not os.path.isdir('exports'):
    os.makedirs('exports')

  # txt file creation
  txt_file = open(TXT_FILE, 'wb')
  txt_file.write('')
  txt_file.close()

def save_data():
  d_members_file = open(MEMBERS_PICKLE_FILE,'wb')
  pickle.dump(downloaded_lists_members, d_members_file)
  
  e_members_file = open(MEMBERS_EXPORTED_PICKLE_FILE,'wb')
  pickle.dump(exported_lists_members, e_members_file)


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
      sys.stdout.write(" and I'm back.\n")
      sys.stdout.flush()
      return get_list_users(screen_name, list_name)

def download():
  for list_id in spec_lists.keys():
    if list_id not in downloaded_lists_members:
      list_data = spec_lists[list_id]
      print 'Downloading list #{0}, name {1}...'.\
        format(list_id, list_data['list_name'])
      users = get_list_users(list_data['screen_name'], list_data['list_name'])
      random.shuffle(users)
      if users is not None:
        downloaded_lists_members[list_id] = users        
        print 'done.'
        save_data()

def export(no_extra = False):
  for list_id in downloaded_lists_members.keys():
    if list_id not in exported_lists_members:
      exported_lists_members[list_id] = 0
    elif exported_lists_members[list_id] == len(downloaded_lists_members):
      print 'All users for list #{0} have been exported.'.format(list_id)
      continue

    previous_export = exported_lists_members[list_id]
    export_range = spec_lists[list_id]['target_size']
    if not no_extra:
      extra = (export_range * 15) / 100
      export_range += extra

    if export_range > len(downloaded_lists_members[list_id]):
      export_range = len(downloaded_lists_members[list_id])

    exported_lists_members[list_id] = export_range

    print 'Exporting {0} users from list #{1}'.\
      format((export_range - previous_export), list_id)
    txt_file = open(TXT_FILE, 'a')
    users_to_export = \
      downloaded_lists_members[list_id][previous_export:export_range]
    for user in users_to_export:
      txt_file.write('{0}\n'.format(user))
    txt_file.close()
    save_data()

if __name__ == '__main__':
  configure_tweepy()
  load_data()
  download()
  export()
