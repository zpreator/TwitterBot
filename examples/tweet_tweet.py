from twitter_bot import TwitterBot
import datetime

if __name__ == '__main__':
    print(datetime.datetime.today().weekday())
    bot = TwitterBot('@laurarawra', keys_path=r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\keys.ini')
    bot.corpus_path = r"C:\Users\zacha\PycharmProjects\TwitterBot\resources\datasets\laurarawra_archive2.txt"
    bot.train_model(save_path=r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\models\laurarawra\markov.json',
                    pull_tweets=False, state_size=2)
    bot.load_model(model_path=r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\models\laurarawra\markov.json', model_type='markov')
    for i in range(10):
        print(bot.generate_sentence())