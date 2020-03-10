import sys
import csv
from langdetect import detect
import nltk
from nltk.corpus import stopwords
import string
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import nltk
import pandas as pd
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
import os.path
from os import path

## Here I take songs of 1960 as an example
### Let's combine the two lists based on hotlist_100 list's id. Set features to null if not found in spotify list
### I kept the title of songs from both lists. That is because the title from spotify seems to be more accurate, while the title from hotlist seems to be easier for searching
hotlist_csv = pd.read_csv('../data/newVersionOfLyrics/lyricsHotListTopNew_{}.csv'.format(1960))
spotify_csv = pd.read_csv('../data/spotify_features_csvs/lyricsHotListTopNew_{}.csv'.format(1960))
combined_csv = pd.merge(hotlist_csv, spotify_csv, how='left', on='Unnamed: 0')


### After we do extraction of the lyrics
# For now, I skip the songs whose lyrics is not English or length is smaller than 200 characters

def extract_lyrics(combined_csv):
    combined_csv.insert(3, 'words', np.empty((len(combined_csv), 0)).tolist())
    combined_csv.insert(4, 'lyrics_length', [0]*len(combined_csv))
    for i in range(len(combined_csv)):
        lyric = combined_csv.loc[i, 'lyrics']
        if pd.isnull(combined_csv.loc[i, 'lyrics']):
            continue
        if len(lyric) < 100 or len(lyric) > 10000:
            continue
            
        if detect(lyric) != 'en':
            continue
        li = []
        combined_csv.loc[i, 'valid'] = 1
        for r in lyric.splitlines():
            # Skip sth like '[Instrument]',['Bridge']
            if '[' in r or '(' in r: 
                continue
            for w in r.split():
                combined_csv.loc[i, 'lyrics_length'] += 1
                #if w in stop_words:
                #    continue;
                word = ''.join([ch for ch in w if ch not in string.punctuation]).lower()
                word = lem.lemmatize(word,"v")
                combined_csv.loc[i, 'words'].append(word)
                
                
combined_csv.insert(1, 'valid', 0)
extract_lyrics(combined_csv)


## Let's combine all the dataset we have and save to the directory

for year in range(1960, 2021):
    hotlist_csv = pd.read_csv('../newVersionOfLyrics/lyricsHotListTopNew_{}.csv'.format(year))
    combined_csv = hotlist_csv
    # Skip 
    if path.exists('../spotify_features_csvs/lyricsHotListTopNew_{}.csv'.format(year)):
        spotify_csv = pd.read_csv('../spotify_features_csvs/lyricsHotListTopNew_{}.csv'.format(year))
        combined_csv = pd.merge(hotlist_csv, spotify_csv, how='left', on='Unnamed: 0')
    
    combined_csv.insert(1, 'valid', 0)
    extract_lyrics(combined_csv)
    combined_csv.to_csv('../combined_dataset/lyrics&features_{}.csv'.format(year)) 

