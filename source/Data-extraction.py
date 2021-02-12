#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pathlib import *
import json
import os
from os.path import isfile, join
from datetime import datetime
import chardet


# In[2]:


def json_to_df(data):
    
# INPUTS: data - this is the dictionary which is obtained from the json
#
# OUTPUTS: df - a pandas dataframe with the information loaded in, the columns renamed and reordered. 
#               WE ARE GETTING RID OF "share","photos","ip" COLUMNS. THESE ONLY EXIST IN SOME CHATS 
#               - not interested for analysis. We also convert timestamp into datetime

    #Input data into df
    df = pd.DataFrame.from_dict(data["messages"])
    df["Title"] = data["title"]
    df["IsGroup"] = data["thread_type"]
    df["StillPart"] = data["is_still_participant"]

    #The participants are shown as a list, we want the list to be in a single dataframe cell so we convert into a string:
    participants = list()
    for participant in data["participants"]:
        participants.append(participant["name"])
    num_participants = len(participants)
    participants = ",".join(participants)

    df["Participants"] = participants
    df["NumParticipants"] = num_participants
    
    #Convert timestamp_ms into datetime
    df["DateTime"] = [datetime.fromtimestamp(timestamp/1000) for timestamp in df["timestamp_ms"]]
    
    #Rename and reorder columns    
    df.rename(columns={"content": "Message", "sender_name": "Sender"}, inplace = True)
    columns = ["Title","IsGroup","StillPart","NumParticipants","Participants","Sender","Message",                "DateTime","type"]
    df = df[columns]

    
    return df


# In[3]:


def sort_decoding_problems(df):
    #Sorts the encoding problems
    
    #Facebook has two different types of apostrophe, UTF-8 cannot deal with one of them
    df.replace({"â\x80\x99" : "'"}, regex = True, inplace = True)
    
    return df


# In[6]:


def load_data():
    #Deal with paths
    path_to_inbox = Path("..") / "data" / "inbox"
    chats = os.listdir(path_to_inbox)

    messages_df = pd.DataFrame()

    #Load the jsons 
    for chat in chats:
        #Each chat is stored in a different directory
        path_to_person = path_to_inbox / chat
        #Message files are stored as jsons - some chats have multiple jsons - find all jsons
        message_files = [pos_json for pos_json in os.listdir(path_to_person) if pos_json.endswith('.json')]
        #Load each json and append them to a singular dataframe for each person
        person_df = pd.DataFrame()

        for message_file in message_files:
            path_to_json = path_to_person / message_file
            with open(path_to_json, encoding='utf-8') as json_data:
                loaded_json_data = json.load(json_data)
                #Looking at the jsons we have several categories in the dict - we have:
                #'participants'
                #'messages'
                #'title',
                #'is_still_participant' = True or False
                #thread_type = RegularGroup or Regular
                #thread_path

            #Input the json into a dataframe:
            single_json_df = json_to_df(loaded_json_data)
            #Append the single_dfjson_df to the person/groupchat's dataframe
            person_df = person_df.append(single_json_df)

        #Now append the person/groupchat's df to the overall df
        messages_df = messages_df.append(person_df)
        messages_df.reset_index(drop = True, inplace = True)
        
    #Sort out the decoding errors found in messages_df
    messages_df = sort_decoding_problems(messages_df)

    return messages_df


# In[7]:


messages_df = load_data()
messages_df.to_csv("../data/processed/initial_df.csv", index=False)

