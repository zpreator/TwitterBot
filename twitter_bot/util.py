import re
from keras.utils import pad_sequences
from typing import List
import numpy as np


def text_cleaner(text: str) -> str:
    """ Cleans text using regex

    Args:
        text: text to clean

    Returns:
        string
    """
    # lower case text
    new_string = text.lower()
    new_string = re.sub(r"'s\b","",new_string)
    # remove punctuations
    new_string = re.sub("[^a-zA-Z]", " ", new_string)
    long_words=[]
    # remove short word
    for i in new_string.split():
        if len(i)>=3:
            long_words.append(i)
    return (" ".join(long_words)).strip()


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
