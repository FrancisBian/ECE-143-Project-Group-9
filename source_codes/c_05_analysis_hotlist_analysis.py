import sys
import csv
from langdetect import detect
import nltk
from nltk.corpus import stopwords
import string
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
lem = WordNetLemmatizer()
from  plotly.offline import plot
import plotly.graph_objs as go
import plotly.io as pio

import c_09_analysis_genreacous
from c_09_analysis_genreacous import *


csv.field_size_limit(sys.maxsize)
print(string.punctuation)
stop_words = set(stopwords.words('english'))
additional_word = set(['im', 'get', 'say', 'go', 'dont', 'know'])
with open('../banned_words_list.txt', 'r') as f:
    banned_word = [line.strip() for line in f]
#Create the banned words list
stop_words = stop_words.union(additional_word).union(banned_word)

# # For the hot100 dataset
# ## In general:
# #### 1) Artist owns the most songs that appears in billboard?
# #### 2) Artist appears most in billboard (by cnt)?
# #### 3) How many songs will be in the 52 weekly hot100 list per year? - around 400 - 800
# #### 4) Songs that appear in the hot100 list most.
# #### 5) Artist whose song always achieved a high rank on the list.
# #### 6) Song appears/gaps in most years
# 
# 
# ## Changes through years:
# #### 1) commonly used words of lyrics - How they differed and how aligned?
# #### 2) What is the average (highest) rank of songs?
# #### 3) How many artists show up in the billboard ever year?
# #### 4) Does the average number of occurrence of the hot100 songs increase/decrease each year?
# #### 5) How about the length of lyrics?
# 
# ## Interesting things:
# #### 1) Songs/Artists that appear again in the hotlist after a long period. 
# #### 2) Songs become hot way later than its release date.
# #### 3) Songs are popular until nowadays

# Extract the bag of words for an entire year. Then we could do TF-IDF or text-based analysis.
def get_yearly_word_list(df):
    '''
    Get the yearly words list of each songs' lyric
    '''
    assert isinstance(df, pd.DataFrame)

    yearly_word_list = []
    for i in range(len(df)):
        li = df.loc[i,'words'].replace('\'', '')
        li = li.strip('][').split(', ') 
        if len(li) != 0:
            yearly_word_list += [w for w in li if w not in stop_words]
    return yearly_word_list


def get_yearly_length(df, exclude=3):
    '''
    Get the yearly length each songs' lyric
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(exclude, int) and exclude >= 0

    sorted_valid_length = sorted([df.loc[i, 'lyrics_length'] for i in range(len(df)) if df.loc[i, 'lyrics_length'] != 0])
    sorted_valid_length = sorted_valid_length[exclude: len(sorted_valid_length) - exclude]
    return sorted_valid_length

def get_yearly_duration(df,exclude=2):
    '''
    Get the yearly duration of each songs
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(exclude, int) and exclude >= 0
    
    sorted_valid_du = sorted([df.loc[i, 'duration_seconds'] for i in range(len(df)) if not pd.isna(df.loc[i, 'duration_seconds'])])
    sorted_valid_du = sorted_valid_du[exclude: len(sorted_valid_du) - exclude]
    return sorted_valid_du


# Get average occurrence of songs in this year's billboard 
def get_average_occ(df):
    '''
    Get the yearly occurrence each songs in billboard
    '''
    assert isinstance(df, pd.DataFrame)
   
    return sum([df.loc[i, 'cnt'] for i in range(len(df))])/len(df)

# Get average highest rank
def get_average_highest_rank(df):
    '''
    Get the yearly average highest rank of each songs
    '''
    assert isinstance(df, pd.DataFrame)
    
    rank_list = []
    for i in range(len(df)):
        rk = df.loc[i,'rank'].replace('\'', '')
        rk = rk.strip('][').split(', ') 
        rk = [int(i) for i in rk] 
        if len(rk) != 0:
            rank_list.append(min(rk))
    return sum(rank_list)/len(rank_list)

# Get the artists of this year
def get_yearly_artists(df):
    '''
    Get the yearly number of artists show up in Billboard
    '''
    assert isinstance(df, pd.DataFrame)

    artists = set()
    for i in range(len(df)):
        artists.add(df.loc[i,'artists'])
    return artists

def update_songs(df, year, songs_years_ranks):
    '''
    Get the song's dictionary
    '''
    assert isinstance(df, pd.DataFrame)

    for i in range(len(df)):
        title = df.loc[i, 'title']
        key = title + " by " + df.loc[i, 'artists']
        rk = df.loc[i,'rank'].replace('\'', '')
        rk = rk.strip('][').split(', ') 
        rk = [int(i) for i in rk]
        if len(rk) == 0:
            continue
        
        if key not in songs_years_ranks:
            songs_years_ranks[key] = defaultdict(list)
            songs_years_ranks[key][year] = rk
        else:
            songs_years_ranks[key][year] = rk


# key: year, val: Bags of word in this year
yearly_words_dict = {}
# key: year, val: list of length of lyrics in this year
yearly_length_dict = defaultdict(list)
# key: year, val: list of duration in this year
yearly_duration_dict = defaultdict(list)
# key: year, val: average occurrence in this year's billboard for songs
yearly_average_occ = {}
# key: year, val: artists that are in the billboard in this year
yearly_artists_dict = {}
# key: song_title, val:{key: year, val: ranks of this song is this year}
songs_years_ranks = {}
# key: year, val: average rank of each song is this year
yearly_average_highest_rank = {}
# key: artist, val: songs by this artist that in the billboard hotlist
artist_songs_dict = defaultdict(set)
# key: artist, val: number of occurrence in billboard
artist_occ_dict = defaultdict(int)
# key: year, val: # songs
yearly_songs_dict = defaultdict(list)

artist_set = set()
song_set = set()


for year in range(1960, 2021):
    df = pd.read_csv('../data/combined_dataset/lyrics&features_{}.csv'.format(year))
    for i in range(len(df)):
        # artist_set.add(df.loc[i, 'artist_name'])
        artist_set.add(df.loc[i, 'artists'])
        song_set.add(df.loc[i, 'title'])
        yearly_songs_dict[year].append(df.loc[i, 'title'])
        
        artist_songs_dict[df.loc[i, 'artists']].add(df.loc[i, 'title'])
        artist_occ_dict[df.loc[i, 'artists']] += (int)(df.loc[i, 'cnt'])
        
    yearly_length_dict[year] = get_yearly_length(df)
    yearly_duration_dict[year] = get_yearly_duration(df)
    yearly_artists_dict[year] = get_yearly_artists(df)
    yearly_words_dict[year] = get_yearly_word_list(df)
    yearly_average_occ[year] = get_average_occ(df)
    update_songs(df, year, songs_years_ranks)
    yearly_average_highest_rank[year] = get_average_highest_rank(df)
    #yearly_released_month[year] = get_released_month(df)
    
def plotAverageLength():
    '''
    plot the average length of each song
    '''
    plt.title("Average length")
    plt.plot([sum(v)/len(v) for k,v in yearly_length_dict.items()])
    positions = [i for i in range(0, 61, 10)]
    labels = [(str)(i + 1960) for i in range(0, 61, 10)]
    plt.xticks(positions, labels)
    plt.locator_params(axis='x', nbins=8)

def plotExpectancy(yearly_average_occ):
    '''
    plot
    '''
    assert isinstance(yearly_average_occ, dict)

    plt.title("Average expectancy of each song in the billboard")
    plt.plot([v for k,v in yearly_average_occ.items()])
    positions = [i for i in range(0, 61, 10)]
    labels = [(str)(i + 1960) for i in range(0, 61, 10)]
    plt.xticks(positions, labels)
    plt.locator_params(axis='x', nbins=8)

def plotAvgNumSongs(yearly_songs_dict):
    '''
    plot
    '''
    assert isinstance(yearly_songs_dict, dict)

    plt.title("Average number of songs on the billboard HOT 100")
    plt.plot([len(s) for y,s in yearly_songs_dict.items()])
    positions = [i for i in range(0, 61, 10)]
    labels = [(str)(i + 1960) for i in range(0, 61, 10)]
    plt.xticks(positions, labels)
    plt.locator_params(axis='x', nbins=8)


def plotAvgHighestRank(yearly_average_highest_rank):
    '''
    plot
    '''
    assert isinstance(yearly_average_highest_rank, dict)

    plt.title("Average highest rank of each song in the billboard")
    plt.plot([v for k,v in yearly_average_highest_rank.items()])
    positions = [i for i in range(0, 61, 10)]
    labels = [(str)(i + 1960) for i in range(0, 61, 10)]
    plt.xticks(positions, labels)
    plt.locator_params(axis='x', nbins=8)


def plotNumArtistsYearly(yearly_artists_dict):
    '''
    plot
    '''
    assert isinstance(yearly_artists_dict, dict)

    plt.title("Number of artists showing in the billboard each year")
    plt.plot([len(v) for k,v in yearly_artists_dict.items()])
    positions = [i for i in range(0, 61, 10)]
    labels = [(str)(i + 1960) for i in range(0, 61, 10)]
    plt.xticks(positions, labels)
    plt.locator_params(axis='x', nbins=8)

def tfldf_analysis():
    '''
    TF-IDF Analysis
    '''
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([' '.join(yearly_words_dict[year]) for year in range(1960, 2021)])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    for index, row in df.iterrows():
        df = df.sort_values(by=index, axis=1, ascending=False)
        print(df.columns[0:10])


# ### General and interesting findings

artist_songs_count = {a:len(b) for a,b in artist_songs_dict.items()}
sorted_artists = sorted(artist_songs_count.items(), key=lambda x: x[1], reverse=True)
#print(sorted_artists[:5])


# #### 2) Artist appears most in billboard (by cnt)?



sorted_artists_occ = sorted(artist_occ_dict.items(), key=lambda x: x[1], reverse=True)
#print(sorted_artists_occ[:10])


# #### 4) Songs that appear in the hot100 list most.

songs_top100 = defaultdict(int)
songs_top10 = defaultdict(int)
songs_top1 = defaultdict(int)

for k,v in songs_years_ranks.items():
    for y, ranks in v.items():
        songs_top100[k] += len(ranks)
        for r in ranks:
            if r <= 10:
                songs_top10[k] += 1
                if r is 1:
                    songs_top1[k] += 1
        
sorted_songs_top100 = sorted(songs_top100.items(), key=lambda x: x[1], reverse=True)
sorted_songs_top10 = sorted(songs_top10.items(), key=lambda x: x[1], reverse=True)
sorted_songs_top1 = sorted(songs_top1.items(), key=lambda x: x[1], reverse=True)
#print(sorted_songs_top100[:5],'\n')
#print(sorted_songs_top10[:5], '\n')
#print(sorted_songs_top1[:5], '\n')


# #### 5) Artist whose song always achieved a high rank on the list.


artist_average_rank = {}
for artist, songs in artist_songs_dict.items():
    for song in songs:
        ranks = []
        minRank = 101
        for year, ranks in songs_years_ranks[song + " by " + artist].items():
            minRank = min(minRank, min(ranks))
        ranks.append(minRank)
    artist_average_rank[artist] = sum(ranks)/len(ranks)
sorted_songs_count = sorted(artist_average_rank.items(), key=lambda x: x[1])
#print(sorted_songs_count[:5])


# #### 6) Song appears/gaps in most years

songs_appears = {a:len(b) for a,b in songs_years_ranks.items()}
sorted_songs_appears = sorted(songs_appears.items(), key=lambda x: x[1], reverse=True)
#print("Songs that shows in the billboard in most years")
#print(sorted_songs_appears[:5])

songs_years = {a:sorted(b)[len(b) - 1] - sorted(b)[0] for a,b in songs_years_ranks.items()}
sorted_songs_years = sorted(songs_years.items(), key=lambda x: x[1], reverse=True)
#print("Songs that covers most years")
#print(sorted_songs_years[:5])

d = songs_years_ranks["Rockin' Around The Christmas Tree by Brenda Lee"]
subject = ['(1960)', '(1960)', '(1960)', '(1961)', '(1961)','(1961)', '(1961)','(1962)', '(1962)', '(1962)', '(1962)','(2014)', '(2015)', '(2016)', 
          '(2016)', '(2016)', '(2016)', '(2017)', '(2017)', '(2017)', '(2018)', '(2018)', '(2018)', '(2018)', '(2018)', '(2018)', '(2019)', '(2019)', 
           '(2019)', '(2019)', '(2019)', '(2020)']
score = []
for k,v in d.items():
    score += v

def song_rank_plotly(score, subject):
    data = [dict(
        type = 'scatter',
        x = score,
        y = subject,
        mode = 'markers',
        transforms = [dict(
            type = 'groupby',
            groups = subject,
        )]
        )
    ]

    layout = dict(
        title = "Rockin' Around The Christmas Tree by Brenda Lee",
        plot_bgcolor='rgb(255, 255, 255)',
        yaxis=dict(
            title = "Year",
            size=5,
        ),
        xaxis=dict(
            title = 'RANK',
            gridcolor='rgb(233, 233, 233)',
        )
    )

    fig_dict = dict(data=data, layout = layout)
    pio.show(fig_dict, validate=False)

'''
def main():
    plot_acous_curve(yearly_length_dict, 200, 'Lyric Length[words]', '200 Words', 'Lyric Length', ref = True)


if __name__ == '__main__':
	main()
'''
