import spacy
import re
import markovify
import textParser as tp


nlp = spacy.load("en_core_web_trf")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence


# utility function for text cleaning
def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b', '', text)
    text = ' '.join(text.split())
    return text


def general_kenobi(text, state_size=2):
    """ Returns a Markovify.Text object that has been filtered through a NLP.

    Args:
        """
    print('Loading natural learning process..')
    print('This will take a minute')
    doc = nlp(text_cleaner(text))
    sents = ' '.join([sent.text for sent in doc.sents if len(sent.text) > 1])
    oh_hi_mark = POSifiedText(sents, state_size=state_size)
    this_json = oh_hi_mark.to_json()
    tp.saveJson('marko_model.json', this_json)
    return oh_hi_mark

def load_model(json_file):
    # model = markovify.Text.from_json(json_file)
    # model = POSifiedText.from_json(json_file)
    json = tp.readJson(json_file)
    model = POSifiedText.from_json(json)
    # model_json = model.to_json()
    # tp.saveJson('marko_model.json')
    return model
