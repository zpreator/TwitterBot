from twitter_bot.util import generate_seq
import pickle
from keras.models import load_model
import tensorflow as tf
from keras.utils import pad_sequences


def get_text(seed):
    model = load_model('wonderland.h5')
    with open('twitter_bot/mapping.pkl', 'rb') as file:
        mapping = pickle.load(file)
    seq_length = 30
    n_chars = 30
    return generate_seq(model, mapping, seq_length, seed, n_chars)


def get_text2(seed):
    max_len = 30
    model = load_model('laura.h5')
    with open('tokenizer.pkl', 'rb') as file:
        tokenizer = pickle.load(file)
    word_index = tokenizer.word_index
    input_seq = tokenizer.texts_to_sequences([seed])[0]
    sentence = ''
    for j in range(10):  # generate 10 words per sentence
        x = pad_sequences([input_seq], maxlen=max_len)
        y_pred = model.predict(x)
        y_pred = tf.reshape(y_pred, (1, -1))
        next_word_idx = tf.random.categorical(y_pred, num_samples=1)[-1, 0].numpy()
        next_word = list(word_index.keys())[list(word_index.values()).index(next_word_idx)]
        sentence += ' ' + next_word
    return sentence


if __name__ == '__main__':
    print(get_text2('what a '))