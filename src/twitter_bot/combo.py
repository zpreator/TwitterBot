import os

from keras.layers import Embedding, GRU, Dense
from keras.models import Sequential, load_model
from keras.utils import pad_sequences, to_categorical
from keras.callbacks import EarlyStopping

from twitter_bot.markov import MarkovModel
from twitter_bot.util import predict_next_word


class ComboModel:
    def __init__(self, tokenizer):
        self.model = None
        self.path = None
        self.markov_model = MarkovModel()
        self.vocab_size = len(tokenizer.word_index)
        self.tokenizer = tokenizer

    def fit(self, texts, embedding_dim=50, rnn_units=150, batch_size=32, num_epochs=10):
        markov_text = texts
        if type(texts) == list:
            markov_text = '.'.join(texts)
        else:
            texts = texts.split('.')
        self.markov_model.fit(markov_text, state_size=1)

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

        # define model
        self.model = Sequential()
        self.model.add(Embedding(self.vocab_size, embedding_dim, input_length=30, trainable=True))
        self.model.add(GRU(rnn_units, recurrent_dropout=0.1, dropout=0.1))
        self.model.add(Dense(units=64, activation='relu'))
        self.model.add(Dense(self.vocab_size, activation='softmax'))

        # Compile model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', run_eagerly=True)

        # Train model
        early_stop = EarlyStopping(monitor='val_loss', patience=10)
        self.model.fit(X, Y, batch_size=batch_size, epochs=num_epochs, callbacks=[early_stop])

    def save(self, path):
        if self.model is not None:
            if os.path.isdir(path):
                h5_path = os.path.join(path, 'model.h5')
                markov_path = os.path.join(path, 'markov.json')
                self.model.save(h5_path)
                self.markov_model.save(markov_path)
            else:
                raise Exception('Please pass in a folder to save the combo model')
        else:
            raise Exception('The model does not exist yet')

    def load_model(self, path):
        if os.path.isdir(path):
            h5_path = os.path.join(path, 'model.h5')
            markov_path = os.path.join(path, 'markov.json')
            self.model = load_model(h5_path)
            self.markov_model.load_model(markov_path)
        else:
            raise Exception('Please pass in a folder to save the combo model')


    def predict(self, seed, num_chars=280, markov_every=2):
        if type(seed) == list:
            sentence = seed
        else:
            sentence = [seed]
        count = 1
        sentence_length = len(' '.join(sentence))
        while sentence_length < num_chars:
            if count % (markov_every) == 0:
                sentence.append(self.markov_model.predict_next_word(sentence[-1]))
            else:
                sentence.append(predict_next_word(seed, self.model, self.tokenizer))
            sentence_length = len(' '.join(sentence))
            count += 1
        return ' '.join(sentence)
