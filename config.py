# Standard python imports
import logging
import os
import configparser

# Third party imports
import praw
import prawcore.exceptions
import tweepy
from groupy.client import Client


def create_groupme_api():
    keys = readKeys()
    groupme_key = keys['groupme']['access_token']
    client = Client.from_token(groupme_key)
    groups = list(client.groups.list_all())
    for group in groups:
        print(group.name)
        if group.name == 'Large Fry Larrys':
            lfl = group
    return lfl


def create_twitter_api():
    keys = readKeys()
    consumer_key = keys['twitter']['consumer_key']
    consumer_secret = keys['twitter']['consumer_secret']
    access_token = keys['twitter']['access_token']
    access_token_secret = keys['twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API", e)
        raise e
    return api


def create_reddit_api():
    keys = readKeys()
    personal = keys['reddit']['personal']
    secret   = keys['reddit']['secret']
    username = keys['reddit']['username']
    password = keys['reddit']['password']
    user_agent = keys['reddit']['user_agent']

    reddit_api = praw.Reddit(client_id=personal,
                             client_secret=secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)
    reddit_api.read_only = True
    try:
        me = reddit_api.user.me()
        return reddit_api
    except prawcore.exceptions.ResponseException:
        print('Something went wrong with authentication')
        return None


def readKeys():
    config = configparser.ConfigParser()
    config.read('keys.ini')
    return config

def readConfig(file='data.ini'):
    config = configparser.ConfigParser()
    config.read(file)
    return config.get('default', 'since_id')

def setConfig(since_id):
    config = configparser.ConfigParser()
    config.read('data.ini')
    config['default']['since_id'] = since_id
    with open('data.ini', 'w') as f:
        config.write(f)
