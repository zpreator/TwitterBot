import tweepy
import textParser as tp

# http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work/5307230#5307230

# # Authenticate to Twitter
# auth = tweepy.OAuthHandler("79yGA6PWDZGFGhuDkKMLGRq3g", "HQWalSRkO4ftvC6CaFyPhdVojsbW3RsUbd68rpRYUOGn0nA4TN")
# auth.set_access_token("834474582748770304-feFx4pHJSycUYLRdMUnHlORKCh320pL", "eyb0r4BT75xTOTymk11glMCS6CG0bQUrCzHg2UnDz7cJa")

# Create API object
# api = tweepy.API(auth)


# Create a tweet
# api.update_status("Hello Tweepy")


# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

# api.update_profile(description="I like Python")
# userID = '@elonmusk'
# userID = '@BoredElonMusk'
# userID = '@MKBHD'
# userID = '@SnazzyQ'
# userID = '@ericandre'
# userID = '@billburr'
# userID = '@VancityReynolds'
# userID = '@laurarawra'
# userID = '@koripaigers'
# userID = '@EsplinJackson'
# userID = '@jesplin32'

# filename = 'elonText.json'
# filename = 'techGuys.json'
# filename = 'comediansText.json'
# filename = 'lauraText.json'
# filename = 'koriText.json'
# filename = 'jacksonText.json'

def parseTweets(api, userID):
    # user = api.get_user(userID)

    # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
    # tweets = api.user_timeline(screen_name=userID, 
    #                         # 200 is the maximum allowed count
    #                         count=200,
    #                         include_rts = False,
    #                         # Necessary to keep full_text 
    #                         # otherwise only the first 140 words are extracted
    #                         tweet_mode = 'extended'
    #                         )
    # all_tweets = []
    # all_tweets.extend(tweets)
    # oldest_id = tweets[-1].id
    # while True:
    #     tweets = api.user_timeline(screen_name=userID, 
    #                         # 200 is the maximum allowed count
    #                         count=200,
    #                         include_rts = False,
    #                         max_id = oldest_id - 1,
    #                         # Necessary to keep full_text 
    #                         # otherwise only the first 140 words are extracted
    #                         tweet_mode = 'extended'
    #                         )
    #     if len(tweets) == 0:
    #         break
    #     oldest_id = tweets[-1].id
    #     all_tweets.extend(tweets)
    #     # print('N of tweets downloaded till now {}'.format(len(all_tweets)))
    all_tweets = queryUserTweets(api, userID, 50)
    filename = str(userID) + '.json'
    dictionary = tp.readJson(filename)
    for info in all_tweets:
        dictionary = tp.parseString(info.full_text, dictionary)

    tp.saveJson(filename, dictionary)
    return filename


def queryUserTweets(api, userID, num_tweets=None, oldest_id=None):
    """ Query for tweets from specified user
    Inputs:
        - api: tweepy api object
        - userID: string specified user
        - num_tweets: int number of tweets to get, default is None
                    for all tweets
        - since_id: int optional time id to grab tweets since_id
    Returns:
        - tweets: list of tweepy tweet objects"""
    loop = True
    if num_tweets < 200:
        count = num_tweets
        loop = False
    else:
        count = 200

    if oldest_id is not None:
        max_id = oldest_id - 1

    all_tweets = []
    while True:
        # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
        tweets = api.user_timeline(screen_name=userID, 
                                # 200 is the maximum allowed count
                                count=count,
                                include_rts = False,
                                max_id = max_id,
                                # Necessary to keep full_text 
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )
        if len(tweets) == 0 or not loop:
            break
        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id
        max_id = oldest_id
    return all_tweets