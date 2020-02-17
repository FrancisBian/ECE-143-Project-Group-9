import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

# read spotipy credentials (a txt file of clientid and secretid)
# refer here if you have problems https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330

# Parameters
git_path = 'C:/Users/iocak/OneDrive/Masaüstü/git/ece143project/'
credentials_path = "C:/Users/iocak/OneDrive/Masaüstü/WI20/ECE 143/Project/credentials.txt"

credentials = pd.read_csv(credentials_path)

# Connection
client_id = credentials['clientid'][0]
client_secret = credentials['clientsecret'][0]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

# Sample File
sample_file = pd.read_csv(git_path + "dataset_hot_list/lyricsHotListTop_1960.csv")

# Trial
index_val = 6
sample_file.loc[index_val, :]

query_song = sample_file.loc[index_val, :]['title']
query_artist = sample_file.loc[index_val, :]['artists']

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

song_df = pd.DataFrame(song_dict, index = [0])