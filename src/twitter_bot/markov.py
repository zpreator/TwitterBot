import os
from twitter_bot.util import read_json, save_json, text_cleaner
import markovify
import spacy
nlp = spacy.load("en_core_web_sm")


class MarkovModel:
    def __init__(self):
        self.model = None
        self.model_type = 'markov'
        self.path = None
        self.markov_dict = None

    def fit(self, text, state_size=2):
        doc = nlp(text_cleaner(text))
        sents = ' '.join([sent.text for sent in doc.sents if len(sent.text) > 1])
        self.model = POSifiedText(sents, state_size=state_size)

    def save(self, path):
        self.path = os.path.join(path, self.model_type + '.json')
        save_json(self.path, self.model.to_json())

    def load_model(self, path):
        self.path = os.path.join(path, self.model_type + '.json')
        self.model = POSifiedText.from_json(read_json(self.path))

    def predict(self, seed=None, num_chars=280):
        bot_tweet = self.model.make_short_sentence(num_chars)
        return bot_tweet


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence
