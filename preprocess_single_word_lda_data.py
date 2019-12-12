import pickle
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import datapath
import re
import csv
from collections import defaultdict
import json
import nltk
from nltk.corpus import stopwords as stops
import string


stopwords = stops.words('english')

# TODO: resolve naming issue between lemmatized corpus and corpus: delete the other one in both repos to avoid confusion
phrase_data = pickle.load(open("/Users/reuben/Dropbox/Reuben/Research/idioms/code/corpus_assembly/lemmatized_corpus.pkl",'rb'))
# single_word_data = pickle.load(open("/Users/reuben/Dropbox/Reuben/Research/idioms/code/corpus_assembly/single_word_corpus.pkl",'rb'))
single_word_data = pickle.load(open("/Users/reuben/Downloads/single_word_corpus.pkl",'rb'))


# items = sorted(phrase_data,key = lambda x: len(phrase_data[x]),reverse=True)



# print([x[0] for x in phrase_data[item]])

# raise Exception



def clean(text):

	text = text.split()
	text = [word.lower() for word in text if word not in stopwords]
	text = [word for word in text if word not in string.punctuation]
	text = [word for word in text if word not in list(item.split(" "))]

	return text

def text_to_num(texts):

	texts = [clean(text) for text in texts]

	common_dictionary = Dictionary(texts)
	common_dictionary.id2token = dict([(common_dictionary.token2id[x]+1,x) for x in common_dictionary.token2id.keys()])
	common_corpus = [[common_dictionary.token2id[word]+1 for word in text] for text in texts]

	return common_corpus, common_dictionary.token2id, common_dictionary.id2token

for item in phrase_data:

	word1, word2 = tuple(item.split(" "))
	sents_p = [x[0] for x in phrase_data[item]]
	sents_w1 = [x for x in single_word_data[word1]]
	sents_w2 = [x for x in single_word_data[word2]]

	word_1_index = len(sents_p)
	word_2_index = len(sents_p)+len(sents_w1)

	sents = sents_p+sents_w1+sents_w2

	common_corpus, token2id, id2token = text_to_num(sents)

	with open("phrases/"+item+"_corpus.json",'w') as f:
		f.write(json.dumps(common_corpus))

	with open("phrases/"+item+"_token2id.json",'w') as f:
		f.write(json.dumps(token2id))

	with open("phrases/"+item+"_id2token.json",'w') as f:
		f.write(json.dumps(id2token))

	# the split points in the concatenated corpus of sentences for phrase, word1, word2
	with open("phrases/"+item+"_indices.json",'w') as f:
		f.write(json.dumps((word_1_index,word_2_index)))





