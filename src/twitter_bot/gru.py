

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