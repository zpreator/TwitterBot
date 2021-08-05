# Standard python imports
import pandas as pd
import numpy as np
import sys


# 3rd party import
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils
import markovify
import spacy

# Project imports
from config import create_twitter_api, create_reddit_api, create_groupme_api
import twitter
import reddit
import groupme
from TaggedText import TaggedText

# https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/


def text_processing(txt_file):
    # Reading text file
    raw_text = open(txt_file, 'r', encoding='utf-8').read()
    raw_text = raw_text.lower()
    # Gets unique characters
    chars = sorted(list(set(raw_text)))
    # Character-number mapping
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    n_chars = len(raw_text)
    n_vocab = len(chars)
    print("Total Characters: ", n_chars)
    print("Total Vocab: ", n_vocab)

    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 100
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i:i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)
    print("Total Patterns: ", n_patterns)

    # reshape X to be [samples, time steps, features]
    X = np.reshape(dataX, (n_patterns, seq_length, 1))
    # normalize
    X = X / float(n_vocab)
    # one hot encode the output variable
    Y = np_utils.to_categorical(dataY)

    return X, Y


def train_model(X, Y):
    # define the LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(Y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # define the checkpoint
    filepath = "checkpoints/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    # Fit the model
    model.fit(X, Y, epochs=20, batch_size=128, callbacks=callbacks_list)


def create_text(txt_file):
    # load the network weights
    raw_text = open(txt_file, 'r', encoding='utf-8').read()
    raw_text = raw_text.lower()
    # create mapping of unique chars to integers, and a reverse mapping
    chars = sorted(list(set(raw_text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))
    # summarize the loaded data
    n_chars = len(raw_text)
    n_vocab = len(chars)
    print("Total Characters: ", n_chars)
    print("Total Vocab: ", n_vocab)
    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 100
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i:i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)
    print("Total Patterns: ", n_patterns)
    # reshape X to be [samples, time steps, features]
    X = np.reshape(dataX, (n_patterns, seq_length, 1))
    # normalize
    X = X / float(n_vocab)
    # one hot encode the output variable
    y = np_utils.to_categorical(dataY)
    # define the LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    # load the network weights
    filename = "checkpoints/weights-improvement-20-2.0294.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # pick a random seed
    start = np.random.randint(0, len(dataX) - 1)
    pattern = dataX[start]
    print("Seed:")
    print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
    # generate characters
    for i in range(1000):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]

def read_big_csv():
    df = pd.read_csv('datasets/wikipedia_txt.csv')
    print(df.head())
    # for chunk in pd.read_csv('datasets/en-books-dataset.csv', chunksize=30):
    #     print(chunk.head())

def train_markov_chain(files):
    mega_text = []
    for file in files:
        if '.csv' in file:
            df = pd.read_csv(file)
            lines = list(df['body_text'].values)
        elif '.txt' in file:
            with open(file) as this_file:
                lines = this_file.readlines()
        mega_text.extend(lines)
    markovify.Text(mega_text)


def main():
    # twitter_api = create_twitter_api()
    # reddit_api = create_reddit_api()
    # if reddit_api:
    #     df_pm = reddit.load_reddit_posts(reddit_api, 'prequalmemes', 2)
    # X, Y = text_processing('wonderland.txt')
    # train_model(X, Y)
    # create_text('datasets/wonderland.txt')
    # create_text('wonderland.txt')

    # files = ['datasets/marktwain1.txt.txt', 'datasets/wonderland.txt']
    # train_markov_chain(files)

    txt_file = 'datasets/marktwain1.txt'
    raw_text = open(txt_file, encoding='utf-8').read()

    model = TaggedText(raw_text)
    print(model.make_sentence())

if __name__ == '__main__':
    main()
