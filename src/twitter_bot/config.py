import configparser
import os

import tweepy

PROJECT_PATH = os.path.split(os.path.split(os.path.split(__file__)[0])[0])[0]
LAST_TWEET_INFO_PATH = os.path.join(PROJECT_PATH, 'resources', 'temp', 'data.ini')
KEYS_PATH = os.path.join(PROJECT_PATH, 'resources', 'keys.ini')


def create_twitter_api(api_key=None, api_key_secret=None, access_token=None, access_token_secret=None):
    if not os.path.exists(KEYS_PATH):
        if not all([api_key, api_key_secret, access_token, access_token_secret]):
            raise Exception('Either pass in the keys and tokens, or create a file called '
                            '"keys.ini" in the resources folder')
    else:
        keys = read_keys()
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


def read_keys():
    config = configparser.ConfigParser()
    config.read(KEYS_PATH)
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
