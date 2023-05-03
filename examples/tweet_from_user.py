from twitter_bot import TwitterBot


if __name__ == '__main__':
    bot = TwitterBot('@laurarawra')
    bot.load_model()
    print('Generating a word: ', bot.generate_word())
    print('Generating a sentence: ', bot.generate_sentence())
    print('Reading tweets: ', bot.read_tweets())
