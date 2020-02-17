import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import os
import re

# read spotipy credentials (a txt file of clientid and secretid)
# refer here if you have problems https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330

# Parameters
git_path = 'C:/Users/iocak/OneDrive/Masaüstü/git/ece143project/'
credentials_path = "C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/credentials.txt"
hot_list_path = 'dataset_hot_list/'
target_path = 'spotify_features_csvs/'

credentials = pd.read_csv(credentials_path)
hotlist_files = os.listdir(git_path + hot_list_path)
hotlist_files = [i for i in hotlist_files if '.csv' in i]

# Connection
client_id = credentials['clientid'][0]
client_secret = credentials['clientsecret'][0]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

def spotify_feature_extractor(query_song, query_artist, index_val):
    '''
    Extracts features for a given song and artist name.
    
    Inputs:
        query_song : song name, str 
        query_artist : artist name, str
        index_val : number of queried row in hots list, int
    
    Returns a pandas dataframe of 1 row.
    '''
    
    assert isinstance(query_song, str)
    assert isinstance(query_artist, str)
    assert isinstance(index_val, int)
    assert index_val >= 0
    query_string = '{%s, %s}' % (query_song, query_artist) #keywords for query: song name, artist
    result = sp.search(query_string) #search query
    
    # Song Features
    song_dict = {}
    
    # name and id
    song_dict['song_name'] = result['tracks']['items'][0]['name']
    song_dict['song_link'] = result['tracks']['items'][0]['external_urls']['spotify']
    song_dict['song_id'] = result['tracks']['items'][0]['id']
    song_dict['song_uri'] = result['tracks']['items'][0]['uri']
    song_dict['album_name'] = result['tracks']['items'][0]['album']['name']
    song_dict['album_id'] = result['tracks']['items'][0]['album']['id']
    song_dict['album_uri'] = result['tracks']['items'][0]['album']['uri']
    song_dict['artist_name'] = result['tracks']['items'][0]['artists'][0]['name']
    song_dict['artist_id'] = result['tracks']['items'][0]['artists'][0]['id']
    song_dict['artist_uri'] = result['tracks']['items'][0]['artists'][0]['uri']
    
    # analysis features
    song_dict['duration_seconds'] = result['tracks']['items'][0]['duration_ms'] / 1000
    song_dict['album_song_count'] =  result['tracks']['items'][0]['album']['total_tracks']
    song_dict['song_popularity'] = result['tracks']['items'][0]['popularity']
    song_dict['album_release_date'] = result['tracks']['items'][0]['album']['release_date']
    
    audio_features_dict = sp.audio_features(song_dict['song_uri'])[0]
    artist_features_dict = sp.artist(song_dict['artist_id'])
    album_features_dict = sp.album(song_dict['album_id'])
    
    song_dict['danceability'] = audio_features_dict['danceability']
    song_dict['energy'] = audio_features_dict['energy']
    song_dict['key'] = audio_features_dict['key']
    song_dict['loudness'] = audio_features_dict['loudness']
    song_dict['mode'] = audio_features_dict['mode']
    song_dict['speechiness'] = audio_features_dict['speechiness']
    song_dict['acousticness'] = audio_features_dict['acousticness']
    song_dict['instrumentalness'] = audio_features_dict['instrumentalness']
    song_dict['liveness'] = audio_features_dict['liveness']
    song_dict['valence'] = audio_features_dict['valence']
    song_dict['tempo'] = audio_features_dict['tempo']
    
    song_dict['artist_genres'] = str(artist_features_dict['genres'])
    song_dict['album_genres'] = str(album_features_dict['genres'])
    
    song_df = pd.DataFrame(song_dict, index = [index_val])
    
    return song_df

# Problem Points:
# Song Name might not - mismatch with something on Spotify
# We need to double check after code runs

for i in hotlist_files:
    
    hot_csv = pd.read_csv(git_path + hot_list_path + i)
    hot_year_features = pd.DataFrame()
    
    for j in range(len(hot_csv)):
        
        try:
            temp = spotify_feature_extractor(query_song = hot_csv.loc[j, :]['title'], 
                                             query_artist = hot_csv.loc[j, :]['artists'],
                                             index_val = j)
            hot_year_features = hot_year_features.append(temp)
            print(f'{j}/{len(hot_csv)} of file {i}')
        except:
            print(f'!!!ERROR!!! {j}/{len(hot_csv)} of file {i}')
        
    hot_year_features.to_csv(git_path + target_path + i)
            
    
    
