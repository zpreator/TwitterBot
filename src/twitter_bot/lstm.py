from keras.models import load_model, Model
import numpy as np
from happytransformer import HappyTextToText, TTSettings
from keras.utils import pad_sequences
from keras.utils import to_categorical, pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import LSTM, Dense, GRU, Embedding
from twitter_bot.util import tokenize

happy_tt = HappyTextToText("T5",  "prithivida/grammar_error_correcter_v1")
settings = TTSettings(do_sample=True, top_k=10, temperature=0.5,  min_length=1, max_length=100)


class LSTMModel:
    def __init__(self, tokenizer):
        self.model = None
        self.vocab_size = len(tokenizer.word_index)
        self.tokenizer = tokenizer

    def fit(self, texts, embedding_dim=128, rnn_units=256, batch_size=32, num_epochs=10):
        # Convert text to numerical representations
        sequences = self.tokenizer.texts_to_sequences(texts)

        # Create training data
        X = []
        Y = []
        for seq in sequences:
            for i in range(1, len(seq)):
                X.append(seq[:i])
                Y.append(seq[i])
        X = pad_sequences(X, maxlen=30)
        Y = to_categorical(Y, num_classes=self.vocab_size)

        # Define RNN model
        self.model = Sequential([
            Embedding(self.vocab_size, embedding_dim),
            LSTM(rnn_units),
            Dense(self.vocab_size, activation='softmax')
        ])

        # Compile model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', run_eagerly=True)

        # Train model
        self.model.fit(X, Y, batch_size=batch_size, epochs=num_epochs)

    def save(self, path):
        if '.h5' not in path:
            path = path + '.h5'
        if self.model is not None:
            self.model.save(path)
        else:
            raise Exception('The model does not exist yet')

    def load_model(self, path):
        self.model = load_model(path)

    def predict(self, seed=None, num_chars=280):
        bot_tweet = generate_text(seed, self.model, self.tokenizer, num_chars=num_chars)
        return bot_tweet


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
    next_word = list(word_index.keys())[list(word_index.values()).index(next_word_idx)]
    return next_word