from twitter_bot import TwitterBot

if __name__ == '__main__':
    bot = TwitterBot('@laurarawra')
    bot.train_model(model_type='lstm', pull_tweets=False, num_tweets=5000, char_level=True)
    print(bot.generate_sentence())