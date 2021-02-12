#!/usr/bin/env python
# coding: utf-8

# In[35]:


class Decoder():
    #Sorts the encoding problems
    def solve_appostrophe(self, text):
        #Facebook has two different types of apostrophe, UTF-8 cannot deal with one of them
        text = text.replace("â\x80\x99","'")
        return text

    def decode(self, text):
        text = self.solve_appostrophe(text)
        return text

