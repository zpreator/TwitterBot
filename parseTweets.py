import tweepy
import textParser as tp

# http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work/5307230#5307230

# Authenticate to Twitter
auth = tweepy.OAuthHandler("79yGA6PWDZGFGhuDkKMLGRq3g", "HQWalSRkO4ftvC6CaFyPhdVojsbW3RsUbd68rpRYUOGn0nA4TN")
auth.set_access_token("834474582748770304-feFx4pHJSycUYLRdMUnHlORKCh320pL", "eyb0r4BT75xTOTymk11glMCS6CG0bQUrCzHg2UnDz7cJa")

# Create API object
api = tweepy.API(auth)


# Create a tweet
# api.update_status("Hello Tweepy")


try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# api.update_profile(description="I like Python")
# userID = '@elonmusk'
# userID = '@BoredElonMusk'
# userID = '@MKBHD'
# userID = '@SnazzyQ'
# userID = '@ericandre'
# userID = '@billburr'
userID = '@VancityReynolds'

# filename = 'elonText.json'
# filename = 'techGuys.json'
filename = 'comediansText.json'

olMusky = api.get_user(userID)

# https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
while True:
    tweets = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           max_id = oldest_id - 1,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    all_tweets.extend(tweets)
    print('N of tweets downloaded till now {}'.format(len(all_tweets)))

dictionary = tp.readJson(filename)
for info in all_tweets:
    dictionary = tp.parseString(info.full_text, dictionary)

tp.saveJson(filename, dictionary)