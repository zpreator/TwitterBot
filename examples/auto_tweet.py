from twitter_bot import TwitterBot
import numpy as np
import datetime


if __name__ == '__main__':
    bot = TwitterBot('@laurarawra')
    bot.load_model()
    if datetime.datetime.today().weekday() == 5:
        bot.train_model(pull_tweets=True)
    else:
        bot.tweet_random_sentence(num_chars=np.random.choice(range(20, 280), size=1))
