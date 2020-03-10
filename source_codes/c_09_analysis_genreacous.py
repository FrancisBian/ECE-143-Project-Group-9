#!/usr/bin/env python
# coding: utf-8

# In[12]:


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wordcloud
from nltk.corpus import stopwords
from  plotly.offline import plot
import plotly.graph_objs as go


# In[13]:


def get_unique_words(df):
    """
    find the median of yearly danceability
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    uw_list=[]
    for i in range(len(df)):
        if len(df.loc[i, 'words'])!=0 and df.loc[i, 'valid']==1:
            cur_list = df.loc[i,'words'].replace('\'', '')
            cur_list = cur_list.strip('][').split(', ')
            uw_list.append(len(set(cur_list)))
    
    return uw_list


# In[16]:


def get_acous_list(acous_name,df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    acous_list=[df.loc[i, acous_name] for i in range(len(df)) if np.isnan(df.loc[i, acous_name])==0 and df.loc[i, 'valid']==1]
    
    return acous_list


# In[17]:


def get_acous_median(acous_name,df):
    """
    find the median of yearly danceability
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    acous_list= sorted([df.loc[i, acous_name] for i in range(len(df)) if np.isnan(df.loc[i, acous_name])==0 and df.loc[i, 'valid']==1])

    return acous_list[len(acous_list)//2]


# In[18]:


def get_genre_count(df,genre_name):
    """
    find the count of keys of one year
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    cnt=0
    for i in range(len(df)):
        if np.isnan(df.loc[i, genre_name])==0 and df.loc[i, 'valid']==1:
            c=int(df.loc[i, genre_name])
            cnt+=c
    return cnt


# In[34]:


def plot_acous_curve(acous_dict1, ref_val, yaxis_label, ref_legend, legend, ref = False):
    """
    plot the yearly duration seconds
    input:duration_dict
    """
    assert isinstance(acous_dict1,dict)
    
    if ref:
        trace0 = go.Scatter(
            x=[k for k,v in acous_dict1.items() if k != 2020],
            y=[ref_val for k,v in acous_dict1.items() if k != 2020],
            name=ref_legend,
            line=dict(
                color = 'rgb(245, 154,145)',
                width = 3
            )
        )
    
    
    trace1 = go.Scatter(
        x=[k for k,v in acous_dict1.items() if k != 2020],
        #y=[sum(v)/len(v) for k,v in acous_dict1.items() if k != 2020],
        y=[sorted(v)[len(v)//2] for k,v in acous_dict1.items() if k != 2020],
        mode='markers',
        name=legend,
        error_y=dict(
            type='data',
            array = [np.std(v) for k,v in acous_dict1.items() if k != 2020],
            thickness=2,
            width=2,
            color='rgb(57, 119, 175)',
        ),
        marker=dict(color='darkblue',size=10)
    )

    layout = go.Layout(
        plot_bgcolor='rgb(255, 255, 255)',
        yaxis=dict(
            title = yaxis_label,
            gridcolor='rgb(233, 233, 233)',
        ),
        xaxis=dict(
            title = 'Year',
            gridcolor='rgb(233, 233, 233)',
        )
    )
    data = [trace0,trace1]
    fig = go.Figure(data=data, layout=layout)
    plot(fig)
    


# In[20]:


def plot_bubble(genre_dict,acous_dict,genre_name,acous_name):
    fig = go.Figure()
    size = [v for k,v in acous_dict.items() if k != 2020]
    fig.add_trace(go.Scatter(
            x=[k for k,v in genre_dict.items() if k != 2020], y=[v for k,v in genre_dict.items() if k != 2020],
            mode='markers', 
           # marker_size=20,
            name=acous_name,
        
            ))
    fig.update_traces(mode='markers', marker=dict(
                size=size,
                color = 'Orange',
                sizemode='area',
                sizeref=2.*max(size)/(40.**2),
                sizemin=4            
                
    ))
# Tune marker appearance and layout
    

    fig.update_layout(
        title=genre_name+' Trend v.s.'+acous_name,
        xaxis=dict(
            title='Year',
            gridcolor='white',
            gridwidth=2,
    ),
        yaxis=dict(
        title=genre_name+' Song Count',
        gridcolor='white',
        gridwidth=2,
    ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True,
        legend={'bordercolor':'rgb(57, 119, 175)'}
)


    plot(fig)
    #fig.show()


# In[35]:



def main():
    speechiness_dict={}
    acousticness_dict={}
    genre_dict={}
    acous_data={}
    valence_dict={}
    loudness_dict={}
    unique_words_dict={}
    
    for year in range(1960, 2020):
        df = pd.read_csv('../data/combined_dataset/lyrics&features_{}.csv'.format(year))        
        #speechiness_dict[year] = get_acous_list('speechiness',df)
        #acousticness_dict[year] = get_acous_list('acousticness',df)
        valence_dict[year]=get_acous_list('valence',df)
        #loudness_dict[year]=get_acous_list('loudness',df)
        #unique_words_dict[year]=get_unique_words(df)
        #genre_dict[year]=get_genre_count(df,"blues")
        
    #plot_acous_curve(speechiness_dict,0.05,'speechiness') 
    plot_acous_curve(valence_dict,0.6,'song valence','reference line','average valence',ref=True) 
    #plot_acous_curve(unique_words_dict,70,'unique words')

    #plot_bubble(genre_dict,acousticness_dict,"Blues","Acousticness")

    
if __name__ == '__main__':
	main()


# In[ ]:




