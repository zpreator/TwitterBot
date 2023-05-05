from twitter_bot import TwitterBot
import numpy as np
import datetime


if __name__ == '__main__':
    print('\n')
    print(datetime.datetime.today().strftime('%Y-%m-%d'))
    print('_'*100)
    print('Making API connection...')
    bot = TwitterBot('@laurarawra')
    print('Success!')
    print('Loading model...')
    bot.load_model('markov')
    print('Success!')
    # print(bot.get_tweets())
    print('Tweeting...')
    # bot.tweet_random_sentence(num_chars=np.random.choice(range(20, 280), size=1))
    print('Success!')

    # Only train weekly on new tweets
    if datetime.datetime.today().weekday() == 5:
        print('It\'s that time of the week! Time to update the model')
        bot.train_model(pull_tweets=True, model_type='markov', state_size=3)
        print('Successfully updated the model :)')