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

# Parameters
git_path = 'C:/Users/iocak/OneDrive/Masaüstü/git/ece143project/'
credentials_path = "C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/credentials.txt"
hot_list_path = 'data/newVersionOfLyrics/'
combined_path = 'data/combined_dataset/'

# read data
file_names = os.listdir(git_path + combined_path)

combined_df = pd.DataFrame()

for i in file_names:
        if '.csv' in i:
            temp_file = pd.read_csv(git_path + combined_path + i)
            combined_df = pd.concat([combined_df, temp_file], axis = 0)
            
            print(i)

combined_df = combined_df[temp_file.columns]
combined_df.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace = True)
combined_df = combined_df.reset_index(drop = True)

# drop 2020
combined_df = combined_df[combined_df['date'] != 2020]

# read combined data
#combined_df = pd.read_parquet('C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/combined_data_with_genres.parquet')

# genre names
genre_names = ['classical', 'electronic_dance_disco', 'funk_soul', 'hip_hop', 'jazz', 'latin',
               'other', 'pop', 'rnb', 'reggae', 'rock', 'world', 'country', 'blues',
               'religious', 'folk', 'indie', 'adult_standards', 'unclassified']

# genre analysis
yearly_genres = combined_df.groupby('date')[genre_names].sum().reset_index()
yearly_counts = combined_df.groupby('date')['classical'].count().reset_index()
yearly_counts.rename(columns = {'classical' : 'count'}, inplace = True)

# scale the genre count sums, find what percentage of year that belongs to that genre
yearly_genres[list(yearly_genres.columns[1:])] = np.array(yearly_genres[list(yearly_genres.columns[1:])]) / np.array(yearly_counts['count'])[:, None]

# melted yearly_genres
yearly_genres_melted = pd.melt(yearly_genres, 
                               id_vars = 'date', 
                               var_name = 'genre', 
                               value_name = 'percentage_in_year')

yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 1960) & (yearly_genres_melted['date'] <= 1969), 'decade'] = '60s'
yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 1970) & (yearly_genres_melted['date'] <= 1979), 'decade'] = '70s'
yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 1980) & (yearly_genres_melted['date'] <= 1989), 'decade'] = '80s'
yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 1990) & (yearly_genres_melted['date'] <= 1999), 'decade'] = '90s'
yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 2000) & (yearly_genres_melted['date'] <= 2009), 'decade'] = '00s'
yearly_genres_melted.loc[(yearly_genres_melted['date'] >= 2010) & (yearly_genres_melted['date'] <= 2019), 'decade'] = '10s'

yearly_genres_melted.to_csv(git_path + 'data/genre_summary/yearly_genres_melted.csv', index = False)

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
plt.show()
# plot of genres throughout the years

def single_genre_plotter(genre_code, label, sub_dim, sub_order):
    plt.subplot(sub_dim[0], sub_dim[1], sub_order)
    plt.plot(yearly_genres['date'], yearly_genres[genre_code])
    plt.title(label)
    plt.ylabel('Fraction of Artists')
    #plt.xlabel('Year')
    plt.ylim([0, 0.7])
    plt.show()

#rise or No Change
single_genre_plotter('pop', 'Pop', (2, 2), 1)
single_genre_plotter('electronic_dance_disco', 'Dance', (2, 2), 2)
single_genre_plotter('country', 'Country', (2, 2), 3)
single_genre_plotter('hip_hop', 'Rap', (2, 2), 4)

#dying
single_genre_plotter('rock', 'Rock', (2, 2), 1)
single_genre_plotter('adult_standards', 'Adult Standards', (2, 2), 2)
single_genre_plotter('funk_soul', 'Funk & Soul', (2, 2), 3)
single_genre_plotter('rnb', 'R & B', (2, 2), 4)

single_genre_plotter('jazz', 'Jazz', (2, 2), 1)
single_genre_plotter('blues', 'Blues', (2, 2), 2)
single_genre_plotter('folk', 'Folk', (2, 2), 3)

# long history

#60s
plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'Adult standards', alpha = 1)
plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 1)
plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'Dance', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'Pop', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'Rap', alpha = 0.35)
plt.legend(loc = 1, bbox_to_anchor=(1.13, 1.02))
plt.title('Artist Genres 1960-2020')
plt.ylabel('Fraction of Artists')
plt.xlabel('Year')
plt.show()

#70s 80s
plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'Adult standards', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 1)
plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'Dance', alpha = 1)
plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'Pop', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'Rap', alpha = 0.35)
plt.legend(loc = 1, bbox_to_anchor=(1.13, 1.02))
plt.title('Artist Genres 1960-2020')
plt.ylabel('Fraction of Artists')
plt.xlabel('Year')
plt.show()

#90s 00s
plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'Adult standards', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'Dance', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'Pop', alpha = 1)
plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'Rap', alpha = 0.35)
plt.legend(loc = 1, bbox_to_anchor=(1.13, 1.02))
plt.title('Artist Genres 1960-2020')
plt.ylabel('Fraction of Artists')
plt.xlabel('Year')
plt.show()

#10s
plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'Adult standards', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'Dance', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'Pop', alpha = 0.35)
plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'Rap', alpha = 1)
plt.legend(loc = 1, bbox_to_anchor=(1.13, 1.02))
plt.title('Artist Genres 1960-2020')
plt.ylabel('Fraction of Artists')
plt.xlabel('Year')
plt.show()

# check latest year distribution
pd.DataFrame(yearly_genres[yearly_genres['date'] == 2019].drop(columns = 'date').T).reset_index().sort_values(by = 59)

# sentiment analysis
yearly_sentiment = combined_df.groupby('date')['sentiment'].mean().reset_index()
plt.plot(yearly_sentiment['date'], yearly_sentiment['sentiment'])

# trial 
trial_1 = combined_df[combined_df['artists'].str.contains('Britney Spears')].groupby('date')['sentiment'].mean().reset_index()
plt.plot(trial_1['date'].astype(str), trial_1['sentiment'])

# trial rap
trial_2 = combined_df.loc[combined_df['hip_hop'] == 1].groupby('date')['sentiment'].mean().reset_index()
plt.plot(trial_2['date'], trial_2['sentiment'])


#### Sentiment Analysis Plotly
####################

#### Define functions
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import wordcloud
from nltk.corpus import stopwords
from  plotly.offline import plot
import plotly.graph_objs as go

def get_sentiment_list(df):
    """
    find the median of yearly speechiness
    df: input dataframe for one year
    """
    assert isinstance(df,pd.DataFrame)
    ac_list= [df.loc[i, 'sentiment'] for i in range(len(df)) if np.isnan(df.loc[i, 'sentiment'])==0 and df.loc[i, 'valid']==1]
    return ac_list# return the median of yearly-speechiness

def plot_acous_curve(acous_dict1,basic_line1,curve_name):
    """
    plot the yearly duration seconds
    input:duration_dict
    """
    assert isinstance(acous_dict1,dict)
    trace0 = go.Scatter(
    x=[k for k,v in acous_dict1.items() if k != 2020],
    y=[basic_line1 for k,v in acous_dict1.items() if k != 2020],
    name='Reference',
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


## Call functions and plot sentiment analysis
sentiment_dict={}

for year in range(1960, 2020):
        df = pd.read_csv(git_path + '/data/combined_dataset/lyrics&features_{}.csv'.format(year))        
        sentiment_dict[year] = get_sentiment_list(df)
        print(year)

        

plot_acous_curve(sentiment_dict, 0.115, 'sentiment')




