import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import os
import re
import itertools
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
from newspaper import Article

# read spotipy credentials (a txt file of clientid and secretid)
# refer here if you have problems https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330

# Parameters
git_path = 'C:/Users/iocak/OneDrive/Masaüstü/git/ece143project/'
credentials_path = "C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/credentials.txt"
hot_list_path = 'newVersionOfLyrics/'
target_path = 'spotify_features_csvs/'

# read combined data
combined_df = pd.read_parquet('C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/combined_data_with_genres_v2.parquet')

# genre names
genre_names = ['classical', 'electronic_dance_disco', 'funk_soul', 'hip_hop', 'jazz', 'latin',
               'other', 'pop', 'rnb', 'reggae', 'rock', 'world', 'country', 'blues',
               'religious', 'folk', 'indie', 'adult_standards', 'unclassified']

# genre analysis
yearly_genres = combined_df.groupby('date')[genre_names].sum().reset_index()
yearly_counts = combined_df.groupby('date')['classical'].count().reset_index()
yearly_counts.rename(columns = {'classical' : 'count'}, inplace = True)

yearly_genres[list(yearly_genres.columns[1:])] = np.array(yearly_genres[list(yearly_genres.columns[1:])]) / np.array(yearly_counts['count'])[:, None]

# plot
# plt.plot(yearly_genres['date'], yearly_genres['classical'], label = 'classical')
plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'electronic_dance_disco')
plt.plot(yearly_genres['date'], yearly_genres['funk_soul'], label = 'funk_soul')
plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'hip_hop')
plt.plot(yearly_genres['date'], yearly_genres['jazz'], label = 'jazz')
# plt.plot(yearly_genres['date'], yearly_genres['latin'], label = 'latin')
# plt.plot(yearly_genres['date'], yearly_genres['other'], label = 'other')
plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'pop')
plt.plot(yearly_genres['date'], yearly_genres['rnb'], label = 'rnb')
# plt.plot(yearly_genres['date'], yearly_genres['reggae'], label = 'reggae')
plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'rock')
# plt.plot(yearly_genres['date'], yearly_genres['world'], label = 'world')
plt.plot(yearly_genres['date'], yearly_genres['country'], label = 'country')
plt.plot(yearly_genres['date'], yearly_genres['blues'], label = 'blues')
# plt.plot(yearly_genres['date'], yearly_genres['religious'], label = 'religious')
plt.plot(yearly_genres['date'], yearly_genres['folk'], label = 'folk')
# plt.plot(yearly_genres['date'], yearly_genres['indie'], label = 'indie')
plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'adult_standards')
# plt.plot(yearly_genres['date'], yearly_genres['unclassified'], label = 'unclassified')

plt.legend()


# sentiment analysis
#combined_df['sentiment'] = combined_df['lyrics'].apply(lambda x: TextBlob(x).sentiment.polarity)
sid = SentimentIntensityAnalyzer()

combined_df['sentiment'] = 0
combined_df[combined_df['valid'] == 1, 'sentiment'] = combined_df[combined_df['valid'] == 1]['lyrics'].apply(lambda x: sid.polarity_scores(x)['neg'] + sid.polarity_scores(x)['pos'])

combined_df.to_parquet('C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/combined_data_with_genres_v2.parquet')

yearly_sentiment = combined_df.groupby('date')['sentiment'].mean().reset_index()
plt.plot(yearly_sentiment['date'], yearly_sentiment['sentiment'])

# trial 
temp = combined_df[combined_df['artists'].str.contains('Britney Spears')].groupby('date')['sentiment'].mean().reset_index()
plt.plot(temp['date'].astype(str), temp['sentiment'])

