import pickle

import spacy
from wonderwords import RandomSentence
nlp = spacy.load('en_core_web_sm')

with open('datasets/laurarawra.txt', 'r', encoding="utf-8") as file:
    laura_text = file.read()

doc = nlp(laura_text)

nouns = []
verbs = []
adjectives = []
for token in doc:
    if token.pos_ == "NOUN" or token.pos_ == "PRON":
        nouns.append(token.text)
    elif token.pos_ == "VERB":
        verbs.append(token.text)
    elif token.pos_ == "ADJ":
        adjectives.append(token.text)

generator = RandomSentence(nouns=nouns, verbs=verbs, adjectives=adjectives)

with open('sentence_generator.pkl', 'wb') as file:
    pickle.dump(generator, file)