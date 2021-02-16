#!/usr/bin/env python
# coding: utf-8

# In[22]:


from Tokeniser import TextTokeniser
from Decoder import Decoder
import pandas as pd

class Preprocessor():
    #Preprocessor object will deal with 
    #1st Preprocessing data
    #2nd Tokenising data
    #3rd Preprocessing tokenised data
    
    def __init__(self):
        self.tokeniser = TextTokeniser()
        self.decoder = Decoder()
    
    def pre_token_preprocessing(self, text):
        #text = pd.to_str(text)
        text = str(text)
        text = self.decoder.decode(text)
        return text
    
    def post_token_preprocessing(self, text):
        return text
    
    def preprocess_text(self, text):
        #initial preprocessing
        text = self.pre_token_preprocessing(text)
        #Tokenise the text
        text = self.tokeniser.clean_and_tokenise_text(text)
        #final preprocessing
        text = self.post_token_preprocessing(text)
        
        return text

