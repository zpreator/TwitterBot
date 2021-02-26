import tweepy
import logging
import os
import configparser

logger = logging.getLogger()

def create_api():
    consumer_key = "74jGD0Q8cvgcTjNbJg9q5ZUAL"
    consumer_secret = "6EuCVQPINXKYsNj8LTe9WcDejWtaatlSQtRIL3zzCrcXMAiVCU"
    access_token = "834474582748770304-ykpXhsF8HhQE9jMqBzO5VX27oggXXFH"
    access_token_secret = "6oJuIacK3maUJllKXV2WErmB7QAcnYr8pjtNUEwszphG8"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def readConfig():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config.get('default', 'since_id')

def setConfig(since_id):
    config = configparser.ConfigParser()
    config.read('data.ini')
    config['default']['since_id'] = since_id
    with open('data.ini', 'w') as f:
        config.write(f)