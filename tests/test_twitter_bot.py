import pytest
import os
from twitter_bot import TwitterBot

TEMP_FOLDER = os.path.join(os.path.split(__file__)[0], 'temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)


def test_config():
    bot = TwitterBot('@laurarawra')
    with pytest.raises(NotImplementedError):
        bot.tweet('message')

    with pytest.raises(NotImplementedError):
        bot.tweet_random_sentence()


def test_markov_model():
    bot = TwitterBot('@laurarawra')
    with open(bot.corpus_path, 'w') as file:
        file.write('This is a corpus of text')
    save_path = os.path.join(TEMP_FOLDER, 'model.json')
    bot.train_model(save_path=save_path, model_type='markov')
    assert os.path.exists(save_path)

    # I could probably add a seed or something... but this should suffice for now
    for _ in range(100):
        assert bot.generate_word() in ['this', 'is', 'a', 'corpus', 'of', 'text']


def test_lstm_model():
    bot = TwitterBot('@laurarawra')
    with open(bot.corpus_path, 'w') as file:
        file.write('This is a corpus of text')
    save_path = os.path.join(TEMP_FOLDER, 'lstm.h5')
    bot.train_model(save_path=save_path, model_type='lstm')
    assert os.path.exists(save_path)
    assert type(bot.generate_sentence(num_chars=100)) == str
