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

data = pickle.load(open("/Users/reuben/Dropbox/Reuben/Research/idioms/code/corpus_assembly/corpus.pkl",'rb'))

items = sorted(data,key = lambda x: len(data[x]),reverse=True)

item = items[1]

sents_and_trees = data[item]

sents = [x[0] for x in sents_and_trees]

# print(item)
# print(len(sents))
# print(sents[:10])

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

common_corpus, token2id, id2token = text_to_num(sents)

with open(item+"_corpus.json",'w') as f:
	f.write(json.dumps(common_corpus))

with open(item+"_token2id.json",'w') as f:
	f.write(json.dumps(token2id))

with open(item+"_id2token.json",'w') as f:
	f.write(json.dumps(id2token))



