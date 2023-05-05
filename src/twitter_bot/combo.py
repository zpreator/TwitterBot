

class ComboModel:
    def __init__(self, tokenizer):
        self.model = None
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
        if '.h5' not in path:
            path = path + '.h5'
        self.path = path
        if self.model is not None:
            self.model.save(path)
        else:
            raise Exception('The model does not exist yet')

    def load_model(self, path):
        self.path = path
        if '.h5' not in path:
            self.path = path + '.h5'
        self.model = load_model(self.path)

    def predict(self, seed=None, num_chars=280):
        bot_tweet = generate_text(seed, self.model, self.tokenizer, num_chars=num_chars)
        return bot_tweet
