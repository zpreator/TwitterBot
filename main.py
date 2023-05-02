from IAmTheSenate import general_kenobi, load_model, clean_text
import config
import twitter
import os
import datetime


print(datetime.datetime.today().day)


def fake_laura_tweet():
    twitter_api = config.create_twitter_api()

    if datetime.datetime.today().weekday() == 5:
        tweets = twitter.get_tweet_text(twitter_api, '@laurarawra', 3000)
        laura_text = ''
        for tweet in tweets:
            tweet = ' '.join(filter(lambda x: x[0] != '@', tweet.split()))
            laura_text += tweet + '.'
        hello_there = general_kenobi(laura_text)
    else:
        hello_there = load_model('marko_model.json')
    bot_tweet = hello_there.make_short_sentence(280)
    bot_tweet = clean_text(bot_tweet)
    twitter_api.update_status(bot_tweet)
    print(bot_tweet)


def main():
    fake_laura_tweet()

    # txt_file = 'datasets/marktwain1.txt'
    # raw_text = open(txt_file, encoding='utf-8').read()
    # hello_there = general_kenobi(raw_text)

    # hello_there = load_model('marktwain.json')
    # print(hello_there.make_sentence())


if __name__ == '__main__':
    main()