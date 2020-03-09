#!/usr/bin/env python
# coding: utf-8

# In[157]:


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wordcloud
from nltk.corpus import stopwords
from  plotly.offline import plot
import plotly.graph_objs as go


# In[179]:


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
    
    return uw_list# return the median of yearly-danceability

def get_speechiness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    sp_list= [df.loc[i, 'speechiness'] for i in range(len(df)) if np.isnan(df.loc[i, 'speechiness'])==0 and df.loc[i, 'valid']==1]

    return sp_list# return the median of yearly-speechiness
def get_acousticness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    ac_list= [df.loc[i, 'acousticness'] for i in range(len(df)) if np.isnan(df.loc[i, 'acousticness'])==0 and df.loc[i, 'valid']==1]

    return ac_list# return the median of yearly-speechiness
def get_valence_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    vl_list= [df.loc[i, 'valence'] for i in range(len(df)) if np.isnan(df.loc[i, 'valence'])==0 and df.loc[i, 'valid']==1]

    return vl_list# return the median of yearly-speechiness


# In[153]:



def get_valence_list(df):
    """
    find the median of yearly danceability
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    vl_list= sorted([df.loc[i, 'valence'] for i in range(len(df)) if np.isnan(df.loc[i, 'valence'])==0 and df.loc[i, 'valid']==1])

    return vl_list[len(vl_list)//2]# return the median of yearly-danceability
def get_speechiness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    sp_list= sorted([df.loc[i, 'speechiness'] for i in range(len(df)) if np.isnan(df.loc[i, 'speechiness'])==0 and df.loc[i, 'valid']==1])

    return sp_list[len(sp_list)//2]# return the median of yearly-speechiness
def get_acousticness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    ac_list= sorted([df.loc[i, 'acousticness'] for i in range(len(df)) if np.isnan(df.loc[i, 'acousticness'])==0 and df.loc[i, 'valid']==1])

    return ac_list[len(ac_list)//2]# return the median of yearly-speechiness
def get_loudness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    ld_list= sorted([abs(df.loc[i, 'loudness']) for i in range(len(df)) if np.isnan(df.loc[i, 'loudness'])==0 and df.loc[i, 'valid']==1])

    return ld_list[len(ld_list)//2]# return the median of yearly-speechiness

def get_instrumentalness_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    ist_list= sorted([abs(df.loc[i, 'instrumentalness']) for i in range(len(df)) if np.isnan(df.loc[i, 'instrumentalness'])==0 and df.loc[i, 'valid']==1])

    return ist_list[len(ist_list)//2]# return the median of yearly-speechiness


# In[6]:


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
    return cnt# return the key_count


# In[5]:


def plot_acous_curve(acous_dict1,basic_line1,curve_name):
    """
    plot the yearly duration seconds
    input:duration_dict
    """
    assert isinstance(acous_dict1,dict)
    trace0 = go.Scatter(
    x=[k for k,v in acous_dict1.items() if k != 2020],
    y=[basic_line1 for k,v in acous_dict1.items() if k != 2020],
    name='basic line',
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
    name='average '+curve_name,
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
    title = curve_name+' trend',
    plot_bgcolor='rgb(255, 255, 255)',
    yaxis=dict(
        title ='song '+curve_name,
        gridcolor='rgb(233, 233, 233)',
    ),
    xaxis=dict(
        title = 'year',
        gridcolor='rgb(233, 233, 233)',
    )
)
    data = [trace0, trace1]
    fig = go.Figure(data=data, layout=layout)
    plot(fig)
    


# In[140]:


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


# In[182]:


def main():
    danceability_dict={}
    speechiness_dict={}
    liveness_dict={}
    acousticness_dict={}
    genre_dict={}
    acous_data={}
    valence_dict={}
    loudness_dict={}
    energy_dict={}
    instrumentalness_dict={}
    unique_words_dict={}
    
    for year in range(1960, 2020):
        df = pd.read_csv('../data/combined_dataset/lyrics&features_{}.csv'.format(year))        
        danceability_dict[year] = get_danceability_list(df)
        speechiness_dict[year] = get_speechiness_list(df)
        #liveness_dict[year] = get_liveness_list(df)
        acousticness_dict[year] = get_acousticness_list(df)
        valence_dict[year]=get_valence_list(df)
        loudness_dict[year]=get_loudness_list(df)
        unique_words_dict[year]=get_unique_words(df)
        energy_dict[year]=get_energy_list(df)
        instrumentalness_dict[year]=get_instrumentalness_list(df)
        genre_dict[year]=get_genre_count(df,"blues")
        
    #plot_acous_curve(danceability_dict,0.6,'daceability') 
    #plot_acous_curve(speechiness_dict,0.05,'speechiness') 
    #plot_acous_curve(valence_dict,0.6,'valence') 
    #plot_acous_curve(liveness_dict,0.14,'liveness')
    plot_acous_curve(unique_words_dict,70,'unique words')
    
    #plot_genre_curve(genre_dict,"hip_hop")
    #plot_bubble(genre_dict,instrumentalness_dict,"blues","instrumentalness")

    
if __name__ == '__main__':
	main()

