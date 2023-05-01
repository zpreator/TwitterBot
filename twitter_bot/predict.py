from util import generate_seq
import pickle
from keras.models import load_model


def get_text(seed):
    model = load_model('wonderland.h5')
    with open('mapping.pkl', 'rb') as file:
        mapping = pickle.load(file)
    seq_length = 30
    n_chars = 30
    return generate_seq(model, mapping, seq_length, seed, n_chars)


if __name__ == '__main__':
    print(get_text('what a '))