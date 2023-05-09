from twitter_bot import TwitterBot

if __name__ == '__main__':
    bot = TwitterBot('@laurarawra', keys_path=r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\keys.ini')
    # bot.train_model(r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\temp\combo', model_type='combo', pull_tweets=True, num_tweets=50, num_epochs=1)
    bot.load_model(r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\temp\combo', model_type='combo')
    print(bot.generate_sentence())