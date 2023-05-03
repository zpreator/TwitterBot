import spacy
import re
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
warnings.filterwarnings('ignore')

# https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33
nltk.download('gutenberg')

# import novels as text objects
hamlet = gutenberg.raw('shakespeare-hamlet.txt')
macbeth = gutenberg.raw('shakespeare-macbeth.txt')
caesar = gutenberg.raw('shakespeare-caesar.txt')


# utility function for text cleaning
def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b', '', text)
    text = ' '.join(text.split())
    return text

#remove chapter indicator
hamlet = re.sub(r'Chapter \d+', '', hamlet)
macbeth = re.sub(r'Chapter \d+', '', macbeth)
caesar = re.sub(r'Chapter \d+', '', caesar)

# apply cleaning function to corpus
hamlet = text_cleaner(hamlet)
caesar = text_cleaner(caesar)
macbeth = text_cleaner(macbeth)

#parse cleaned novels
nlp = spacy.load("en_core_web_trf")
print('loading hamlet')
hamlet_doc = nlp(hamlet)
print('loading macbeth')
macbeth_doc = nlp(macbeth)
print('loading caesar')
caesar_doc = nlp(caesar)

hamlet_sents = ' '.join([sent.text for sent in hamlet_doc.sents if len(sent.text) > 1])
macbeth_sents = ' '.join([sent.text for sent in macbeth_doc.sents if len(sent.text) > 1])
caesar_sents = ' '.join([sent.text for sent in caesar_doc.sents if len(sent.text) > 1])

shakespeare_sents = hamlet_sents + macbeth_sents + caesar_sents

# # create text generator using markovify
# generator_1 = markovify.Text(shakespeare_sents, state_size=3)

# #We will randomly generate three sentences
# for i in range(3):
#     print(generator_1.make_sentence())
#
# # We will randomly generate three more sentences of no more than 100 characters
# for i in range(3):
#     print(generator_1.make_short_sentence(max_chars=100))


# next we will use spacy's part of speech to generate more legible text
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence


# Call the class on our text
generator_2 = POSifiedText(shakespeare_sents, state_size=3)

# now we will use the above generator to generate sentences
for i in range(5):
    print(generator_2.make_sentence())#print 100 characters or less sentences
for i in range(5):
    print(generator_2.make_short_sentence(max_chars=100))