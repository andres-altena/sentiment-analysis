#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


class TextTokeniser():
    def __init__(self):
        self._en_stop = set(stopwords.words('english'))
        self._useless_words = []

    def tokenise(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z\s_]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.split()

    def get_lemma(self, term):
        return WordNetLemmatizer().lemmatize(term)

    def get_stem(self, term):
        return PorterStemmer().stem(term)

    def clean_and_tokenise_text(self, text):
        tokens = self.tokenise(text)
        tokens = [token for token in tokens if token not in self._en_stop]
        tokens = [self.get_stem(token) for token in tokens]
        tokens = [token for token in tokens if token not in self._useless_words]
        return tokens

