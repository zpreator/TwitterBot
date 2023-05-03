from twitter_bot.util import read_json, save_json, text_cleaner
import markovify
import spacy
nlp = spacy.load("en_core_web_trf")


class MarkovModel:
    def __init__(self):
        self.model = None
        self.markov_dict = None
        self.num_n_grams = 2

    def fit(self, text, state_size=2):
        doc = nlp(text_cleaner(text))
        sents = ' '.join([sent.text for sent in doc.sents if len(sent.text) > 1])
        self.model = POSifiedText(sents, state_size=state_size)

    def save(self, path):
        if '.json' not in path:
            path = path + '.json'
        save_json(path, self.markov_dict)

    def load_model(self, path):
        self.model = POSifiedText.from_json(read_json(path))

    def predict(self, seed=None, num_chars=280):
        bot_tweet = self.model.make_short_sentence(num_chars, init_state=list(seed.split(' ')))
        return bot_tweet


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence


def load_model(json_file):
    # model = markovify.Text.from_json(json_file)
    # model = POSifiedText.from_json(json_file)
    json = tp.readJson(json_file)
    model = POSifiedText.from_json(json)
    # model_json = model.to_json()
    # tp.saveJson('marko_model.json')
    return model