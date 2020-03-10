#!/usr/bin/env python
# coding: utf-8

# In[40]:


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wordcloud
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
additional_word = set(['im', 'get', 'say', 'go', 'dont', 'know','make',
                       'oh','yeah','come','baby','want','cause','let','youre'])
with open('banned_words_list.txt', 'r') as f:
    banned_word = [line.strip() for line in f]

#final stop_words set contains banned_word and additional words
stop_words = stop_words.union(additional_word)

def plot_wordcloud(generation_string,index):
    """
    plot and save wordcloud for a specific generation of lyric words
    input:
    generation_string: a string containing all words in ten years
    """
    assert isinstance(generation_string,str)
    font='myfont.ttf'
    c =wordcloud.WordCloud(scale=2,width=400,height=300,font_path=font,collocations=False,background_color='white',
                           max_words = 1400,max_font_size = 95,random_state=int(index))
    c.generate(generation_string) 
    c.to_file("wordcloud"+str(index+50)[-2:]+"s.png")


# In[41]:


def main():
    """
    extract the words from datasets and plot wordclouds
    """   
    path="data/combined_dataset"  
    path_list=os.listdir(path)
    path_list.sort()  
    for index,filename in enumerate(path_list):
        df=pd.read_csv(os.path.join(path,filename))
        if index==0:
            year_list=[]
        for i in range(len(df)):
            cur_list = df.loc[i,'words'].replace('\'', '')
            cur_list = cur_list.strip('][').split(', ')
            if len(cur_list) != 0:
                for wd in cur_list:
                    if wd in banned_word:wd='DT'
                    if wd not in stop_words:year_list.append(wd)
                
        #convert list to string
        ss=' '.join(year_list)
        #if there are ten-year words already,then plot the wordcloud for this generation
        if index%10==0 and index!=0:
            plot_wordcloud(ss,index)
            year_list=[] #set the word list to empty
            
if __name__ == '__main__':
	main()

