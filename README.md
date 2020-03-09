# Analyzing Trends of Music Lyrics and Features Throughout the Decades

- This is the ECE 143 final project managed by Ismail Ocak, Siyi Wang, Yucheng Bian and Yuepeng Shen.
- In this project we: 
	- analyzed the most popular songs of the last decades
	- understood how the songs change throughout the years in terms of genres, features, generations, lyrics, etc. 
	- found trends, changes, and interesting facts about the world's music taste in the last 60 years.
	
- In this project, our analyses are based on Billboard Hot 100 charts of the years between 1960-2020. We also analyzed lyrics and song characteristics. To build our dataset we used these packages:
	- billboard
	- lyricsgenius
	- spotipy

## Codes:

1- Data Extraction and Preparation:
	- 01_data_data_extract.py - Get Billboard Hot 100 and Lyrics Genius Data
	- 02_data_spotify_song_features.py - Get Spotify song features using Billboard hotlist
	- 03_data_combine_hotlist_and_spotify.py - Combine Billboard and Spotify data
	- 04_data_dataprep_genre_sentiment.py - Extract genres, create genre mapping, create sentiment feature

2 - Analysis:
	- 05_analysis_hotlist_analysis.py
	- 06_analysis_artist_popularity.py
	- 07_analysisfun_fact_syp.py
	- 08_analysis_get_top_genre.py
	- 09_analysis_genre&acous.py
	- 10_analysis_generation_wordcloud.py
	- 11_analysis_genre_sentiment_analysis.py - plots about genre and sentiment analyses
