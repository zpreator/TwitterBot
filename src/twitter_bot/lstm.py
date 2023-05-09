import os
from keras.models import load_model
from keras.utils import to_categorical, pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from twitter_bot.util import generate_text


class LSTMModel:
    def __init__(self, tokenizer):
        self.model = None
        self.model_type = 'lstm'
        self.path = None
        self.vocab_size = len(tokenizer.word_index)
        self.tokenizer = tokenizer

    def fit(self, texts, embedding_dim=64, rnn_units=128, batch_size=64, num_epochs=10):
        if type(texts) == str:
            texts = texts.split('.')
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
            Dense(units=64, activation='relu'),
            Dense(self.vocab_size, activation='softmax')
        ])

        # Compile model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', run_eagerly=True)

        # Train model
        self.model.fit(X, Y, batch_size=batch_size, epochs=num_epochs)

    def save(self, path):
        if self.model is not None:
            self.model.save(path)
        else:
            raise Exception('The model does not exist yet')

    def load_model(self, path):
        self.model = load_model(path)

    def predict(self, seed=None, num_chars=280):
        bot_tweet = generate_text(seed, self.model, self.tokenizer, num_chars=num_chars)
        return bot_tweet



