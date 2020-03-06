import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import os
import re
import itertools

# read spotipy credentials (a txt file of clientid and secretid)
# refer here if you have problems https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330

# Parameters
git_path = 'C:/Users/iocak/OneDrive/Masaüstü/git/ece143project/'
credentials_path = "C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/credentials.txt"
hot_list_path = 'newVersionOfLyrics/'
target_path = 'spotify_features_csvs/'

credentials = pd.read_csv(credentials_path)
hotlist_files = os.listdir(git_path + hot_list_path)
hotlist_files = [i for i in hotlist_files if '.csv' in i]


# read combined data

file_names = os.listdir(git_path + 'combined_dataset/')

combined_df = pd.DataFrame()

for i in file_names:
        if '.csv' in i:
            temp_file = pd.read_csv(git_path + 'combined_dataset/' + i)
            combined_df = pd.concat([combined_df, temp_file], axis = 0)
            
            print(i)
    
    
combined_df.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace = True)
combined_df = combined_df.reset_index(drop = True)

# Genre Analysis
all_genres = list(combined_df['artist_genres'])

all_genres = [i.strip("[]").replace("'", "").replace(" ", "").split(',') for i in all_genres if not isinstance(i, float)]

all_genres_unique = []

for i in all_genres:
    for j in i:
        all_genres_unique.append(str(j))
        
all_genres_unique = pd.DataFrame({'original_genre' : list(set(all_genres_unique))})

# a simple approach
all_genres_unique['classical'] = 0
all_genres_unique['electronic_dance_disco'] = 0
all_genres_unique['funk_soul'] = 0
all_genres_unique['hip_hop'] = 0
all_genres_unique['jazz'] = 0
all_genres_unique['latin'] = 0
all_genres_unique['other'] = 0
all_genres_unique['pop'] = 0
all_genres_unique['rnb'] = 0
all_genres_unique['reggae'] = 0
all_genres_unique['rock'] = 0
all_genres_unique['world'] = 0
all_genres_unique['country'] = 0
all_genres_unique['blues'] = 0
all_genres_unique['religious'] = 0
all_genres_unique['world'] = 0
all_genres_unique['folk'] = 0
all_genres_unique['indie'] = 0
all_genres_unique['adult_standards'] = 0
all_genres_unique['unclassified'] = 0

all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('classical'), 'classical'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('techno|electronic|edm|house|dance|deepbigroom|moombahton|eurohi-nrg|post-disco|disco|deep chill|electro|trance|aussietronica|upliftingtrance|darkelectro|deepdubstep|bubbletrance|progressivetrance|tropical'), 'electronic_dance_disco'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('funk|soul'), 'funk_soul'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('rap|hiphop|k-hop|oldschoolnederhop|boombap|beats|chillhop|freestyle'), 'hip_hop'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('jazz|saxophone|dixieland|bossanova|xhosa|contemporarypost-bop|hardbop'), 'jazz'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('latin|salsa|cuba|rumba|reggaeton|samba'), 'latin'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('other'), 'other'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('pop|chamberpsych'), 'pop'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('r&b|rnb|motown|rhythmandblues'), 'rnb'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('reggae|nyahbinghi'), 'reggae'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('rock|metal|punk|canterburyscene|corrosion|neo-progressive|moog|minneapolissound|skarevival'), 'rock'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('country|redneck|fingerstyle|cowboywestern|nashville sound'), 'country'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('blues'), 'blues'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('religious|gospel|christian|church|worship|christmas'), 'religious'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('world|enka|dansktop'), 'world'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('folk|traditionalbluegrass|balkanbrass|old-time|nativeamerican|instrumentalbluegrass'), 'folk'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('indie'), 'indie'] = 1
all_genres_unique.loc[all_genres_unique['original_genre'].str.contains('adultstandards'), 'adult_standards'] = 1

all_genres_unique['genre_count'] = all_genres_unique[list(all_genres_unique.columns[1:])].sum(axis = 1)

all_genres_unique.loc[all_genres_unique['genre_count'] == 0, 'unclassified'] = 1

# fix nans
combined_df.loc[combined_df['artist_genres'] == '[]', 'artist_genres'] = '[empty]'
combined_df.loc[combined_df['artist_genres'].isnull(), 'artist_genres'] = '[nan]'

# loop on main data frame to classify
combined_df_genres = pd.DataFrame(columns = list(all_genres_unique.columns[1:][:-1]))

for i in range(len(combined_df)):
    temp_genres = pd.DataFrame(dict(zip(list(all_genres_unique.columns[1:][:-1]), [0 for i in range(len(all_genres_unique.columns[1:][:-1]))])), index = [0])
    temp_genre_list = combined_df['artist_genres'][i].strip("[]").replace("'", "").replace(" ", "").split(',')
    for j in temp_genre_list:
        #all_genres_unique[all_genres_unique['original_genre'] == j][all_genres_unique.columns[1:][:-1]]
        if len(all_genres_unique[all_genres_unique['original_genre'] == j][all_genres_unique.columns[1:][:-1]]) > 0:
            temp_genres = np.add(temp_genres, all_genres_unique[all_genres_unique['original_genre'] == j][all_genres_unique.columns[1:][:-1]])
    temp_genres = pd.DataFrame(np.where(temp_genres > 0, 1, 0))
    temp_genres.rename(columns = dict(zip(list(range(len(list(all_genres_unique.columns[1:][:-1])))), list(all_genres_unique.columns[1:][:-1]))), inplace = True)
    combined_df_genres = pd.concat([combined_df_genres, temp_genres], axis = 0)
    print(i)
    
combined_df_genres = combined_df_genres.reset_index(drop = True)

# If an artists one genre is unclassified and rest is OK dont count it unclassified
combined_df_genres.loc[combined_df_genres[combined_df_genres.columns[:-1]].sum(axis = 1) > 0, 'unclassified'] = 0

combined_df_genres.sum() # looks good, low number of unclassified

# merge main df and genres
    
combined_df = pd.concat([combined_df, combined_df_genres], axis = 1)

# save the final table (too large, cannot  upload to github)
combined_df.to_parquet('C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/combined_data_with_genres_v2.parquet')

