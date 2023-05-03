import os
import numpy as np

from twitter_bot.util import load_tokenizer, save_tokenizer, load_txt, save_txt, get_tweet_text, tokenize
from twitter_bot.config import create_twitter_api
from twitter_bot.lstm import LSTMModel
from twitter_bot.markov import MarkovModel


MODELS_FOLDER = r'../resources/models'
DATASETS_FOLDER = r'../resources/datasets'


class TwitterBot:
    def __init__(self,
                 user_id,
                 model_name=None,
                 consumer_key=None,
                 consumer_secret=None,
                 access_token=None,
                 access_token_secret=None):
        self.api = create_twitter_api(consumer_key,
                                      consumer_secret,
                                      access_token,
                                      access_token_secret)
        self.user_id = user_id
        self.model = None
        self.tokenizer = None
        if model_name is None:
            model_name = user_id.replace('@', '')
        self.model_name = model_name
        self.model_path = os.path.join(MODELS_FOLDER, self.model_name)
        self.tokenizer_path = os.path.join(MODELS_FOLDER, self.model_name + '.tokenizer')
        self.corpus_path = os.path.join(DATASETS_FOLDER, self.model_name + '.txt')

    def __repr__(self):
        return self.model_name

    def load_model(self, model_type='markov'):
        self.tokenize()
        if model_type == 'lstm':
            self.model = LSTMModel(self.tokenizer)
        else:
            self.model = MarkovModel()
        if os.path.exists(self.model_path):
            self.model.load_model(self.model_path)
        else:
            raise Exception('The twitter bot must be trained before the model can be loaded')

    def train_model(self, pull_tweets=False, model_type='lstm', **kwargs):
        text = self._get_text(pull_tweets)
        self.tokenize()
        if model_type == 'lstm':
            self.model = LSTMModel(self.tokenizer)
        else:
            self.model = MarkovModel()
        self.model.fit(text, **kwargs)
        self.model.save(self.model_path)

    def _get_text(self, pull_tweets=False):
        if pull_tweets:
            tweets = self.read_tweets()
            text = '. '.join(tweets)
            save_txt(text, self.corpus_path)
        elif os.path.exists(self.corpus_path):
            text = load_txt(self.corpus_path)
        else:
            raise Exception('Either the path to a .txt file must be valid, or pull_tweets should be true')
        return text

    def tokenize(self, pull_tweets=False):
        texts = self._get_text(pull_tweets).split('.')
        self.tokenizer = tokenize(texts)
        save_tokenizer(self.tokenizer, self.tokenizer_path)

    def read_tweets(self):
        return get_tweet_text(self.api, self.user_id)

    def generate_sentence(self, num_chars=280, num_words=None, seed=None):
        if self.model is not None:
            if seed is None:
                seed = self.generate_word()
            return self.model.predict(seed=seed, num_chars=num_chars)
        else:
            raise Exception('You need to train or load a model before being able to generate a sentence')

    def generate_word(self):
        if self.tokenizer is None:
            if os.path.exists(self.tokenizer_path):
                self.tokenizer = load_tokenizer(self.tokenizer_path)
            else:
                self.tokenize()

        word_index = self.tokenizer.word_index
        next_word_idx = np.random.choice(len(list(word_index.values())), size=1)
        word = list(word_index.keys())[list(word_index.values()).index(next_word_idx)]
        return word

    def tweet(self, text):
        self.api.update_status(text)

    def tweet_random_sentence(self, seed=None, num_chars=280):
        sentence = self.generate_sentence(num_chars=num_chars, seed=seed)
        self.api.update_status(sentence)