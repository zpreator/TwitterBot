import tweepy
import logging
from config import create_api, setConfig, readConfig
from parseTweets import parseTweets
from generateTweet import generateTweet
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def checkForTweets(api, maxTime):
    messages = api.list_direct_messages(100)
    times = []
    print('Checking for new messages')
    newMessages = False
    for dm in messages:
        message_data = dm.message_create['message_data'] 
        text = message_data['text']
        senderID = dm.message_create['sender_id']
        sender = api.get_user(senderID).screen_name
        # new_since_id = max()
        times.append(dm.created_timestamp)
        recipient = api.get_user(dm.message_create['target']['recipient_id']).screen_name
        same = (recipient == sender)
        if int(dm.created_timestamp) > int(maxTime) and (sender != 'APlayaNamedZach'):
            print('Responding to message from: ', sender)
            filename = parseTweets(api, sender)
            tweet = generateTweet(filename)
            api.send_direct_message(senderID, tweet)
            print('Sending tweet: ', tweet)
            newMessages = True
    if not newMessages:
        print('No new messages')
    maxTime = max(times)
    setConfig(maxTime)
    return maxTime

def main():
    api = create_api()
    loop = True
    since_id = readConfig()
    parseTweets(api, '@elonmusk')
    # while True:
    #     since_id = checkForTweets(api, since_id)
    #     logger.info("Waiting...")
    #     time.sleep(60)
    #     loop = False

if __name__ == "__main__":
    main()