import os
import random

import numpy as np
import tempfile

import openai

from twitter_bot.util import load_tokenizer, save_tokenizer, load_txt, append_to_corpus, get_tweet_text, tokenize
from twitter_bot.config import create_twitter_api_v2, create_openai_key
from twitter_bot.lstm import LSTMModel
from twitter_bot.markov import MarkovModel
from twitter_bot.gru import GRUModel
from twitter_bot.combo import ComboModel


class TwitterBot:
    def __init__(self,
                 user_id,
                 keys_path=None,
                 api_key=None,
                 api_key_secret=None,
                 access_token=None,
                 access_token_secret=None,
                 openai_key=None):
        self.api = None
        if not all([api_key is None, api_key_secret is None, access_token is None, access_token_secret is None,
                    keys_path is None]):
            # self.api = create_twitter_api(api_key=api_key,
            #                               api_key_secret=api_key_secret,
            #                               access_token=access_token,
            #                               access_token_secret=access_token_secret,
            #                               keys_path=keys_path)
            self.api = create_twitter_api_v2(keys_path=keys_path)
        self.openai_key = openai_key
        if self.openai_key is None:
            self.openai_key = create_openai_key(keys_path=keys_path)
        openai.api_key = self.openai_key
        self.user_id = user_id
        self.model = None
        self.tokenizer = None
        self.tokenizer_path = os.path.join(tempfile.gettempdir(), 'tokenizer.pkl')
        self.corpus_path = os.path.join(tempfile.gettempdir(), self.user_id + '.txt')

    def __repr__(self):
        return f'{self.user_id} bot'

    def load_model(self, model_path, model_type='markov'):
        self.tokenize()
        if model_type.lower() == 'lstm':
            self.model = LSTMModel(self.tokenizer)
            ext = '.h5'
        elif model_type.lower() == 'gru':
            self.model = GRUModel(self.tokenizer)
            ext = '.h5'
        elif model_type.lower() == 'markov':
            self.model = MarkovModel()
            ext = '.json'
        elif model_type.lower() == 'combo':
            self.model = ComboModel(self.tokenizer)
            self.model.load_model(model_path)
            return
        else:
            raise Exception('Please pass in either lstm, gru or markov')
        if os.path.isdir(model_path):
            found = False
            for file in os.listdir(model_path):
                if ext in os.path.splitext(file)[1].lower():
                    model_path = os.path.join(model_path, file)
                    if found:
                        raise Exception(f'There are more than one files ending in {ext} in {model_path}')
                    found = True
            if not found:
                raise Exception(f'There are no files ending in {ext} in {model_path}')
        elif ext not in os.path.splitext(model_path):
            raise Exception(f'model save_path must end in {ext} for {model_type} models. '
                            'Alternatively, pass in a path to a folder containing the model')
        self.model.load_model(model_path)

    def train_model(self, save_path, model_type='markov', pull_tweets=False,
                    num_tweets=100, char_level=False, **kwargs):
        texts = self._get_texts(pull_tweets=pull_tweets, num_tweets=num_tweets)
        self.tokenize(char_level=char_level)
        if model_type.lower() == 'lstm':
            self.model = LSTMModel(self.tokenizer)
            ext = '.h5'
        elif model_type.lower() == 'gru':
            self.model = GRUModel(self.tokenizer)
            ext = '.h5'
        elif model_type.lower() == 'markov':
            self.model = MarkovModel()
            ext = '.json'
        elif model_type.lower() == 'combo':
            self.model = ComboModel(self.tokenizer)
            self.model.fit(texts, **kwargs)
            self.model.save(save_path)
            return
        else:
            raise Exception('Please pass in either lstm, gru or markov')
        self.model.fit(texts, **kwargs)
        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, f'{self.user_id.split("@")[1]}{ext}')
        elif ext not in os.path.splitext(save_path):
            raise Exception(f'model save_path must end in {ext} for {model_type} models. '
                            'Alternatively, pass in a path to a folder')
        self.model.save(save_path)

    def _get_texts(self, pull_tweets=False, num_tweets=100):
        if pull_tweets:
            texts = self.get_tweets(num_tweets=num_tweets)
            append_to_corpus(texts, self.corpus_path)
        elif os.path.exists(self.corpus_path):
            texts = load_txt(self.corpus_path)
        else:
            raise Exception('Either the path to a .txt file must be valid, or pull_tweets should be true')
        return texts

    def tokenize(self, pull_tweets: bool = False, char_level: bool = False) -> None:
        """ Sets up the tokenize object class variable and saves a copy of the tokenizer

        Args:
            pull_tweets: should the model pull new tweets to tokenize
            char_level: tokenize on a character level instead of word level

        Returns:

        """
        texts = self._get_texts(pull_tweets)
        if len(texts) == 1:
            texts = texts[0].split('.')
        self.tokenizer = tokenize(texts, char_level=char_level)
        save_tokenizer(self.tokenizer, self.tokenizer_path)

    def get_tweets(self, num_tweets: int = 10) -> list[str]:
        """ Gets tweets from the user starting from the most recent

        Args:
            num_tweets: Number of tweets to get

        Returns:
            list[str]
        """
        if self.api is None:
            raise NotImplementedError('The api was not configured, please add the 4 keys when creating a TwitterBot object')
        return get_tweet_text(self.api, self.user_id, num_tweets=num_tweets)

    def generate_sentence(self, num_chars: int = 280, seed: str = None) -> str:
        """ Generates a random sentence based on the selected model (self.model)

        Args:
            num_chars (optional): number of characters to limit the sentence to
            seed (optional): beginning string to kick things off

        Returns:
            str
        """
        if self.model is not None:
            if seed is None:
                seed = self.generate_word()
            prediction = self.model.predict(seed=seed, num_chars=num_chars)
            return self.gpt_filter(prediction)
        else:
            raise Exception('You need to train or load a model before being able to generate a sentence')

    def generate_word(self) -> str:
        """ Picks a random word from the users twitter vocabulary

        Returns:
            str
        """
        if self.tokenizer is None:
            if os.path.exists(self.tokenizer_path):
                self.tokenizer = load_tokenizer(self.tokenizer_path)
            else:
                self.tokenize()

        word_index = self.tokenizer.word_index
        next_word_idx = np.random.choice(len(list(word_index.values())), size=1)
        next_word_idx += 1  # Because the tokenizer starts indices at 1 for some reason
        word = list(word_index.keys())[list(word_index.values()).index(next_word_idx)]
        return word

    def tweet(self, text):
        if self.api is None:
            raise NotImplementedError('The api was not configured, please add the 4 keys when creating a TwitterBot object')
        try:
            self.api.update_status(text)
        except:
            self.api.create_tweet(text=text)

    def tweet_random_sentence(self, seed: str = None, num_chars: int = 280) -> None:
        """ Generates a random sentence and then posts it on Twitter

        Args:
            seed (optional): beginning string to kick things off
            num_chars (optional): number of characters to limit the sentence to

        Returns:

        """
        sentence = self.generate_sentence(num_chars=num_chars, seed=seed)
        try:
            print(sentence)
        except:
            pass
        if self.api is None:
            raise NotImplementedError('The api was not configured, please add the 4 keys when creating a TwitterBot object')
        self.tweet(sentence)

    def gpt_filter(self, sentence):
        # Get a random set of tweets to inform the chatbot of the writing style
        tweets = self._get_texts(pull_tweets=False)[0].split('.')
        random_tweets = random.sample(tweets, 100)
        random_tweets_str = ','.join([f'[{x}]' for x in random_tweets])

        # Define the chatbot role
        system_msg = "You are a twitter bot, responsible for generating funny tweets"
        # Define the request to the chatbot
        user_msg = f"Write one tweet, of no more than 280 characters given this sentence as an inspiration for the theme: '{sentence}'. " \
                   "Here are a few additional examples of tweets of which I would like you to mimic their tone. They are each in square brackets: "
        user_msg += random_tweets_str
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                                messages=[{"role": "system", "content": system_msg},
                                                          {"role": "user", "content": user_msg}])
        final_output = response['choices'][0]['message']['content']  # Extract content from api response

        # Remove added quotes at the beginning and end
        if final_output[0] == '"' and final_output[-1] == '"':
            final_output = final_output[1:-1]
        return final_output