import configparser
import os
import tempfile

import tweepy

LAST_TWEET_INFO_PATH = os.path.join(tempfile.gettempdir(), 'latest_tweet.ini')


def create_twitter_api(api_key=None, api_key_secret=None, access_token=None, access_token_secret=None, keys_path=None):
    if keys_path is None or not os.path.exists(keys_path):
        if not all([api_key, api_key_secret, access_token, access_token_secret]):
            raise Exception('Either pass in the keys and tokens, or create a file called '
                            '"keys.ini" in the resources folder')
    else:
        keys = read_keys(keys_path)
        api_key = keys['twitter']['api_key']
        api_key_secret = keys['twitter']['api_key_secret']
        access_token = keys['twitter']['access_token']
        access_token_secret = keys['twitter']['access_token_secret']
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API", e)
        raise e
    return api

def create_openai_key(keys_path):
    keys = read_keys(keys_path)
    return keys['openai']['key']

def create_twitter_api_v2(api_key=None, api_key_secret=None, access_token=None, access_token_secret=None, bearer_token=None, keys_path=None):
    if keys_path is None or not os.path.exists(keys_path):
        if not all([api_key, api_key_secret, access_token, access_token_secret, bearer_token]):
            raise Exception('Either pass in the keys and tokens, or create a file called '
                            '"keys.ini" in the resources folder')
    else:
        keys = read_keys(keys_path)
        api_key = keys['twitter']['api_key']
        api_key_secret = keys['twitter']['api_key_secret']
        access_token = keys['twitter']['access_token']
        access_token_secret = keys['twitter']['access_token_secret']

    client = tweepy.Client(
        consumer_key=api_key, consumer_secret=api_key_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    return client


def read_keys(keys_path):
    config = configparser.ConfigParser()
    config.read(keys_path)
    return config


def read_config(file=LAST_TWEET_INFO_PATH):
    config = configparser.ConfigParser()
    config.read(file)
    return config.get('default', 'since_id')


def set_config(since_id):
    config = configparser.ConfigParser()
    config.read(LAST_TWEET_INFO_PATH)
    config['default']['since_id'] = since_id
    with open('data.ini', 'w') as f:
        config.write(f)
