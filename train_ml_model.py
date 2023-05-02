from twitter_bot import util
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import pandas as pd
from keras.utils import to_categorical, pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import LSTM, Dense, GRU, Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint
import config
import twitter

# twitter_api = config.create_twitter_api()
# tweets = twitter.get_tweet_text(twitter_api, '@laurarawra', 3000)
# laura_text = ''
# for tweet in tweets:
#     tweet = ' '.join(filter(lambda x: x[0] != '@', tweet.split()))
#     laura_text += tweet + '.'

# laura_text = ''
# with open('datasets/wonderland.txt', 'r') as file:
#     for line in file.readlines():
#         laura_text += line


def train_model(text, model_path):
    cleaned_text = util.text_cleaner(text)
    sequences = util.create_seq(cleaned_text)

    # create a character mapping index
    chars = sorted(list(set(cleaned_text)))
    mapping = dict((c, i) for i, c in enumerate(chars))
    with open('twitter_bot/mapping.pkl', 'wb') as file:
        pickle.dump(mapping, file)
    encoded_sequences = util.encode_seq(sequences, mapping)

    # vocabulary size
    vocab = len(mapping)
    encoded_sequences = np.array(encoded_sequences)
    # create X and y
    X, y = encoded_sequences[:,:-1], encoded_sequences[:,-1]
    # one hot encode y
    y = to_categorical(y, num_classes=vocab)
    # create train and validation sets
    X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

    print('Train shape:', X_tr.shape, 'Val shape:', X_val.shape)

    # define model
    model = Sequential()
    model.add(Embedding(vocab, 50, input_length=30, trainable=True))
    model.add(GRU(150, recurrent_dropout=0.1, dropout=0.1))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dense(vocab, activation='softmax'))
    print(model.summary())

    # compile the model
    model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer='adam')
    # fit the model
    early_stop = EarlyStopping(monitor='val_loss', patience=10)
    model.fit(X_tr, y_tr, epochs=100, validation_data=(X_val, y_val), callbacks=[early_stop])

    model.save(model_path)


def train_model_2(text, model_path):
    # Define hyperparameters
    vocab_size = 10000
    embedding_dim = 128
    rnn_units = 256
    batch_size = 32
    num_epochs = 100

    # Load and preprocess text data
    text = text.lower()  # preprocess text data
    texts = text.split('.')

    # Create vocabulary
    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(texts)
    if len(tokenizer.word_index) < vocab_size:
        vocab_size = len(tokenizer.word_index)
        tokenizer = Tokenizer(num_words=vocab_size)
        tokenizer.fit_on_texts(texts)
    with open('tokenizer.pkl', 'wb') as file:
        pickle.dump(tokenizer, file)


    # Convert text to numerical representations
    sequences = tokenizer.texts_to_sequences(texts)

    # Create training data
    X = []
    Y = []
    for seq in sequences:
        for i in range(1, len(seq)):
            X.append(seq[:i])
            Y.append(seq[i])
    X = pad_sequences(X, maxlen=30)
    Y = to_categorical(Y, num_classes=vocab_size)

    # Define RNN model
    model = Sequential([
        Embedding(vocab_size, embedding_dim),
        LSTM(rnn_units),
        Dense(vocab_size, activation='softmax')
    ])

    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', run_eagerly=True)

    # Train model
    model.fit(X, Y, batch_size=batch_size, epochs=num_epochs)

    model.save(model_path)




if __name__ == '__main__':
    # wonderland_txt = ''
    # with open('datasets/wonderland.txt', 'r') as file:
    #     for line in file.readlines():
    #         wonderland_txt += line
    # train_model(wonderland_txt, 'wonderland.h5')
    # twitter_api = config.create_twitter_api()
    # tweets = twitter.get_tweet_text(twitter_api, '@laurarawra', 3000)
    # laura_text = ''
    # for tweet in tweets:
    #     tweet = ' '.join(filter(lambda x: x[0] != '@', tweet.split()))
    #     laura_text += tweet + '.'
    #
    # with open('laura.txt', 'w', encoding="utf-8") as file:
    #     file.write(laura_text)

    with open('datasets/laura.txt', 'r', encoding="utf-8") as file:
        laura_text = file.read()

    train_model_2(laura_text, 'laura.h5')