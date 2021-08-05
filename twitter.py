import textParser as tp


def parseTweets(api, userID):
    # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
    all_tweets = queryUserTweets(api, userID, 50)
    filename = str(userID) + '.json'
    dictionary = tp.readJson(filename)
    for info in all_tweets:
        dictionary = tp.parseString(info.full_text, dictionary)

    tp.saveJson(filename, dictionary)
    return filename


def get_max_id(api, userID):
    tweet = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=1,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    return tweet[-1].id


def queryUserTweets(api, userID, num_tweets=None, oldest_id=None):
    """ Query for tweets from specified user
    Args:
        - api: tweepy api object
        - userID: string specified user
        - num_tweets: int number of tweets to get, default is None
                    for all tweets
        - since_id: int optional time id to grab tweets since_id
    Returns:
        - tweets: list of tweepy tweet objects"""
    loop = True
    if not num_tweets:
        count = 200
        num_tweets = 10000
    elif num_tweets < 200:
        count = num_tweets
        loop = False
    else:
        count = 200

    if oldest_id is not None:
        max_id = oldest_id - 1
    else:
        max_id = get_max_id(api, userID)
    all_tweets = []
    while loop:
        # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
        tweets = api.user_timeline(screen_name=userID,
                                # 200 is the maximum allowed count
                                count=count,
                                include_rts = False,
                                max_id=max_id,
                                # Necessary to keep full_text
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )
        print('Tweets read: ', len(all_tweets))
        if len(tweets) == 0 or not loop or len(all_tweets) > num_tweets:
            all_tweets.extend(tweets)
            break
        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id
        max_id = oldest_id
    return all_tweets


def get_tweet_text(api, userID, num_tweets=50):
    tweets_text = []
    tweets = queryUserTweets(api, userID, num_tweets)
    for info in tweets:
        tweets_text.append(info.full_text)
    return tweets_text