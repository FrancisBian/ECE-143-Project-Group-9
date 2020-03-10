#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wordcloud
from nltk.corpus import stopwords


# In[3]:


def get_top4_artist(start,end):
    """
    find the top 4 artist for one generation
    """
    assert isinstance(start,int) and isinstance(end,int)
    at_pl_dict={}
    for year in range(start,end+1):
        df = pd.read_csv('data/combined_dataset/lyrics&features_{}.csv'.format(year)) 
        assert isinstance(df,pd.DataFrame)
        for i in range(len(df)):
            assert isinstance(df.loc[i, 'artists'],str)
            if df.loc[i, 'artists'] in at_pl_dict:
                if np.isnan(df.loc[i, 'song_popularity'])==0 and df.loc[i, 'artists']!='Glee Cast':
                    at_pl_dict[df.loc[i, 'artists']]+=df.loc[i, 'song_popularity']
            else:
                if np.isnan(df.loc[i, 'song_popularity'])==0:
                    at_pl_dict[df.loc[i, 'artists']]=df.loc[i, 'song_popularity']
    at_pl_list=sorted(at_pl_dict.items(), key=lambda e:e[1], reverse=True) 
    top4_artist=[at_pl_list[i][0] for i in range(len(at_pl_list))if i<4]
    return top4_artist


# In[4]:


def get_popularity_artist(artist_list):
    """
    get the yearly popularity of artists in the list
    """
    assert isinstance(artist_list,list)
    year_dict={}
    for year in range(1960, 2020):
        popularity_list=[0 for i in range(len(artist_list))]
        df = pd.read_csv('data/combined_dataset/lyrics&features_{}.csv'.format(year))   
        for index,art in enumerate(artist_list):
            a = df[df['artists']==art].index.tolist()
            for i in a:
                if np.isnan(df.loc[i, 'song_popularity'])==0:
                    popularity_list[index]+=df.loc[i, 'song_popularity']
        year_dict[year]=popularity_list
                    
    return year_dict     


# In[5]:


def plot_artist_popularity(year_dict,top4_artist_list,generation):
    """
    plot the yearly popularity of artists in the list
    year_dict:yearly popularity infomation
    top4_artist_list:name list
    generation:decade info
    """
    assert isinstance(year_dict,dict)
    assert isinstance(top4_artist_list,list)
    assert isinstance(generation,int)
    plt.figure()
    plt.title("artist popularity - "+str(1960+generation*10)+"s")
    for i in range(len(top4_artist_list)):
        plt.plot([k for k,v in year_dict.items()],[v[i] for k,v in year_dict.items()])
           
    plt.xlabel('year')
    plt.ylabel('yearly popularity of artists')
    plt.ylim(ymin=0)
    #plt.grid(True)
    plt.legend(top4_artist_list)
    plt.savefig('ap'+str(1960+generation*10)+"s.jpg")


# In[6]:


def main():
    top4_artist_list=[]
    start=1960
    for g in range(6):
        top4_artist_list=get_top4_artist(start+g*10,start+g*10+10)        
        year_dict=get_popularity_artist(top4_artist_list)
    #print(year_dict)
        plot_artist_popularity(year_dict,top4_artist_list,g)
if __name__ == '__main__':
	main()


# In[ ]:




