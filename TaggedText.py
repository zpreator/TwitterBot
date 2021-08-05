import markovify
import nltk
import re
from unidecode import unidecode
from nltk.corpus import gutenberg

# corpus = textacy.Corpus.load('/path/to/corpus/',
#         name="corpus_name", compression='gzip')

class TaggedText(markovify.Text):

    def sentence_split(self, text):
        """
        Splits full-text string into a list of sentences.
        """
        sentence_list = []
        for doc in corpus:
            sentence_list += list(doc.sents)

        return sentence_list

    def word_split(self, sentence):
        """
        Splits a sentence into a list of words.
        """
        return ["::".join((word.orth_,word.pos_)) for word in sentence]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

    def test_sentence_input(self, sentence):
        """
        A basic sentence filter. This one rejects sentences that contain
        the type of punctuation that would look strange on its own
        in a randomly-generated sentence.
        """
        sentence = sentence.text
        reject_pat = re.compile(r"(^')|('$)|\s'|'\s|[\"(\(\)\[\])]")
        # Decode unicode, mainly to normalize fancy quotation marks
        if sentence.__class__.__name__ == "str":
            decoded = sentence
        else:
            decoded = unidecode(sentence)
        # Sentence shouldn't contain problematic characters
        if re.search(reject_pat, decoded): return False
        return True

    def generate_corpus(self, text):
        """
        Given a text string, returns a list of lists; that is, a list of
        "sentences," each of which is a list of words. Before splitting into
        words, the sentences are filtered through `self.test_sentence_input`
        """
        sentences = self.sentence_split(text)
        passing = filter(self.test_sentence_input, sentences)
        runs = map(self.word_split, sentences)
        print(runs[0])
        return runs

# # Generated the model
# model = TaggedText(corpus)
# # A sentence based on the model
# print(model.make_sentence())