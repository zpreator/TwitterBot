import os
from twitter_bot.util import generate_text
from keras.layers import Embedding, GRU, Dense
from keras.models import Sequential, load_model
from keras.utils import pad_sequences, to_categorical
from keras.callbacks import EarlyStopping


class GRUModel:
    def __init__(self, tokenizer):
        self.model = None
        self.model_type = 'lstm'
        self.path = None
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

        # define model
        self.model = Sequential()
        self.model.add(Embedding(self.vocab_size, 50, input_length=30, trainable=True))
        self.model.add(GRU(150, recurrent_dropout=0.1, dropout=0.1))
        self.model.add(Dense(units=64, activation='relu'))
        self.model.add(Dense(self.vocab_size, activation='softmax'))

        # Compile model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', run_eagerly=True)

        # Train model
        early_stop = EarlyStopping(monitor='val_loss', patience=10)
        self.model.fit(X, Y, batch_size=batch_size, epochs=num_epochs, callbacks=[early_stop])

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



def train_model(text, model_path):
    cleaned_text = util.text_cleaner(text)
    sequences = util.create_seq(cleaned_text)

    # create a character mapping index
    chars = sorted(list(set(cleaned_text)))
    mapping = dict((c, i) for i, c in enumerate(chars))
    with open('src/twitter_bot/mapping.pkl', 'wb') as file:
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