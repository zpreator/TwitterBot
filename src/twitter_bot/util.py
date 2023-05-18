import pickle
import re
import json
import os
from keras.utils import pad_sequences
from typing import List
import numpy as np
from keras.preprocessing.text import Tokenizer
from happytransformer import HappyTextToText, TTSettings
happy_tt = HappyTextToText("T5",  "prithivida/grammar_error_correcter_v1")
settings = TTSettings(do_sample=True, top_k=10, temperature=0.5,  min_length=1, max_length=100)


def parseTweets(api, userID):
    # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
    all_tweets = query_user_tweets(api, userID, 50)
    filename = str(userID) + '.json'
    dictionary = read_json(filename)
    for info in all_tweets:
        dictionary = parse_string(info.full_text, dictionary)

    save_json(filename, dictionary)
    return filename


def get_max_id(api, userID):
    tweet = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=1,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    return tweet[-1].id


def query_user_tweets(api, userID, num_tweets=None, oldest_id=None):
    """ Query for tweets from specified user
    Args:
        - api: tweepy api object
        - userID: string specified user
        - num_tweets: int number of tweets to get, default is None
                    for all tweets
        - since_id: int optional time id to grab tweets since_id
    Returns:
        - tweets: list of tweepy tweet objects"""
    loop = True
    if not num_tweets:
        count = 200
        num_tweets = 10000
    elif num_tweets < 200:
        count = num_tweets
        loop = False
    else:
        count = 200

    if oldest_id is not None:
        max_id = oldest_id - 1
    else:
        max_id = get_max_id(api, userID)
    all_tweets = []
    while True:
        # https://fairyonice.github.io/extract-someones-tweet-using-tweepy.html
        tweets = api.user_timeline(screen_name=userID,
                                # 200 is the maximum allowed count
                                count=count,
                                include_rts = False,
                                max_id=max_id,
                                # Necessary to keep full_text
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )
        if len(tweets) == 0 or not loop or len(all_tweets) > num_tweets:
            all_tweets.extend(tweets)
            break
        all_tweets.extend(tweets)
        oldest_id = tweets[-1].id
        max_id = oldest_id
        if not loop:
            break
    print('Tweets read: ', len(all_tweets))
    return all_tweets


def get_tweet_text(api, userID, num_tweets=50):
    tweets_text = []
    tweets = query_user_tweets(api, userID, num_tweets)
    for info in tweets:
        tweets_text.append(info.full_text)
    return tweets_text


def read_json(path):
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                dictionary = json.load(file)
                return dictionary
        else:
            save_json(path, {})
            return str({})
    except Exception as e:
        print(e)
        return str({})


def save_json(path, dictionary):
    with open(path, 'w+') as f:
        json.dump(dictionary, f)


def parse_string(text, dictionary):
    words = text.replace('.', '').replace(',', '').replace(':', '').replace(';', '').split(' ')
    for i in range(len(words)-2):
        key = words[i] + ' ' + words[i+1]
        value = words[i+2]
        try:
            if value not in dictionary[key]:
                dictionary[key].append(value)
        except:
            dictionary[key] = []
            dictionary[key].append(value)
    return dictionary


# def text_cleaner(text: str) -> str:
#     """ Cleans text using regex
#
#     Args:
#         text: text to clean
#
#     Returns:
#         string
#     """
#     # lower case text
#     new_string = text.lower()
#     new_string = re.sub(r"'s\b","",new_string)
#     # remove punctuations
#     new_string = re.sub("[^a-zA-Z]", " ", new_string)
#     long_words=[]
#     # remove short word
#     for i in new_string.split():
#         if len(i)>=3:
#             long_words.append(i)
#     return (" ".join(long_words)).strip()
#

def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b', '', text)
    text = ' '.join(text.split())
    return text

def create_seq(text: str) -> List[str]:
    """ Breaks down text into sequences of 30 characters

    Args:
        text: text to create sequence from

    Returns:
        list
    """
    length = 30
    sequences = list()
    for i in range(length, len(text)):
        # select sequence of tokens
        seq = text[i-length:i+1]
        # store
        sequences.append(seq)
    print('Total Sequences: %d' % len(sequences))
    return sequences


def encode_seq(seq: list, mapping: dict):
    sequences = list()
    for line in seq:
        # integer encode line
        encoded_seq = [mapping[char] for char in line]
        # store
        sequences.append(encoded_seq)
    return sequences


def generate_seq(model, mapping, seq_length, seed_text, n_chars):
    in_text = seed_text
    # generate a fixed number of characters
    for _ in range(n_chars):
        # encode the characters as integers
        encoded = [mapping[char] for char in in_text]
        # truncate sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        # predict character
        predict_y = model.predict(encoded, verbose=0)
        yhat = np.argmax(predict_y, axis=1)
        # yhat = model.predict_classes(encoded, verbose=0)
        # reverse map integer to character
        out_char = ''
        for char, index in mapping.items():
            if index == yhat:
                out_char = char
                break
        # append to input
        in_text += char
    return in_text


def load_tokenizer(path):
    with open(path, 'rb') as file:
        tokenizer = pickle.load(file)
    return tokenizer


def save_tokenizer(tokenizer, path):
    with open(path, 'wb') as file:
        pickle.dump(tokenizer, file)


def load_txt(path):
    with open(path, 'r', encoding="utf-8") as file:
        text = file.read()
    return text


def save_txt(text, path):
    with open(path, 'w', encoding="utf-8") as file:
        file.write(text)


def tokenize(texts, vocab_size=10000, char_level=False):
    # Create vocabulary
    tokenizer = Tokenizer(num_words=vocab_size, char_level=char_level)
    tokenizer.fit_on_texts(texts)
    if len(tokenizer.word_index) < vocab_size:
        vocab_size = len(tokenizer.word_index)
        tokenizer = Tokenizer(num_words=vocab_size, char_level=char_level)
        tokenizer.fit_on_texts(texts)
    return tokenizer


def generate_text(seed, model, tokenizer, num_words=None, num_chars=None):
    sentence = seed
    if num_words is not None:
        for _ in range(num_words):
            new_word = predict_next_word(sentence, model, tokenizer)
            sentence += ' ' + new_word
    elif num_chars is not None:
        while len(sentence) < num_chars:
            new_word = predict_next_word(sentence, model, tokenizer)
            sentence += ' ' + new_word
    else:
        raise Exception('Pass either num_words or num_chars')
    return happy_tt.generate_text("gec:" + sentence, args=settings).text.capitalize()


def predict_next_word(seed, model, tokenizer, max_len=30):
    input_seq = tokenizer.texts_to_sequences([seed])[0]
    word_index = tokenizer.word_index
    x = pad_sequences([input_seq], maxlen=max_len)
    y_pred = model.predict(x)[0]
    next_word_idx = np.random.choice(len(y_pred), size=1, p=y_pred)
    next_word_idx += 1
    next_word = list(word_index.keys())[list(word_index.values()).index(next_word_idx)]
    return next_word