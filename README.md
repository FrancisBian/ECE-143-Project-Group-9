<a href="https://www.billboard.com/charts/hot-100"><img src="img/billboard_snippet.png" alt="Italian Trulli"></a>

# Analyzing Trends of Music Lyrics and Features Throughout the Decades

> analyzed the most popular songs of the last decades

> understood how the songs change throughout the years in terms of genres, features, generations, lyrics, etc. 

> found trends, changes, and interesting facts about the world's music taste in the last 60 years.

---

## Data Source
In this project, our analyses are based on Billboard Hot 100 charts of the years between 1960-2020. 
We also analyzed lyrics and song characteristics. To build our dataset we used these Python packages:

- billboard
	
- lyricsgenius
	
- spotipy

---

## Installation

```shell
$ pip3 install billboard.py
```

```javascript
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials

#Connect to LyricsGenius
genius = lyricsgenius.Genius("Your_ID_goes_here")

#Connect to Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
```

---

## Codes:

### Data Extraction and Preparation:
 - 01_data_data_extract.py - Get Billboard Hot 100 and Lyrics Genius Data
 - 02_data_spotify_song_features.py - Get Spotify song features using Billboard hotlist
 - 03_data_combine_hotlist_and_spotify.py - Combine Billboard and Spotify data
 - 04_data_dataprep_genre_sentiment.py - Extract genres, create genre mapping, create sentiment feature

### Analysis:
 - 05_analysis_hotlist_analysis.py
 - 06_analysis_artist_popularity.py
 - 07_analysisfun_fact_syp.py
 - 08_analysis_get_top_genre.py
 - 09_analysis_genre&acous.py
 - 10_analysis_generation_wordcloud.py
 - 11_analysis_genre_sentiment_analysis.py - plots about genre and sentiment analyses

### Plot Snippet:
![Recordit GIF](http://g.recordit.co/GiVH5fq5LX.gif)

---

## Features

---

## Contributors
| <a href="https://github.com/FrancisBian" target="_blank">**Yucheng Bian**</a> | <a href="https://github.com/Eva-SiyiW" target="_blank">**Siyi Wang**</a> | <a href="https://github.com/ShYuPe" target="_blank">**Yuepeng Shen**</a> | <a href="https://github.com/iocak28" target="_blank">**Ismail Ocak**</a> |
| :---: |:---:| :---:| :---:|
| [![Yucheng Bian](https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](https://github.com/FrancisBian)    | [![Siyi Wang](https://avatars1.githubusercontent.com/u/55155879?s=400&v=4)](https://github.com/Eva-SiyiW) | [![Yuepeng Shen](https://avatars1.githubusercontent.com/u/28599459?s=400&v=4)](https://github.com/ShYuPe)  | [![Ismail Ocak](https://avatars0.githubusercontent.com/u/14804342?s=400&v=4)](https://github.com/iocak2)    |
| <a href="https://github.com/FrancisBian" target="_blank">`github.com/FrancisBian`</a> | <a href="https://github.com/Eva-SiyiW" target="_blank">`github.com/Eva-SiyiW`</a> | <a href="https://github.com/ShYuPe" target="_blank">`github.com/ShYuPe`</a> | <a href="https://github.com/iocak28" target="_blank">`github.com/iocak28`</a> |

---

## Support
Reach out to us at one of the following places!
- email to 'y2bian@ucsd.edu'
- email to 'iocak28@gmail.com'
