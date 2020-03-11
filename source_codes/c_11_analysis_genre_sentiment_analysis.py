import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import os
import re
import itertools
import matplotlib.pyplot as plt

########### FUNCTIONS

# Read data function
# Parameters
def read_combined_data(git_path = os.getcwd(), combined_path = '/data/combined_dataset/'):
    '''
    Reads combined dataset and combined the data files.
    
    Input:
        git_path: Path of the repo, str
        combined_path: path_name of combined data in repo, str
    Returns:
        combined_df: A dataframe that has song features, pandas dataframe
    '''
    assert isinstance(git_path, str)
    assert isinstance(combined_path, str)
     
    file_names = os.listdir(git_path + combined_path)
    
    combined_df = pd.DataFrame()
    
    for i in file_names:
            if '.csv' in i:
                temp_file = pd.read_csv(git_path + combined_path + i)
                combined_df = pd.concat([combined_df, temp_file], axis = 0)
                
                #print(i)
    
    combined_df = combined_df[temp_file.columns]
    combined_df.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1'], inplace = True)
    combined_df = combined_df.reset_index(drop = True)
    
    # drop 2020
    combined_df = combined_df[combined_df['date'] != 2020]
    return combined_df

# Genre prep function
def yearly_genre_prep(combined_df):
    '''
    Prepare yearly summary of genres.
    
    Input: 
        combined_df: combined dataframe of song features, pandas dataframe
    Returns:
        yearly_genres: yearly summarized genre data, pandas dataframe
    '''
    assert isinstance(combined_df, pd.core.frame.DataFrame)
    
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

    # label decades
    yearly_genres.loc[(yearly_genres['date'] >= 1960) & (yearly_genres['date'] <= 1969), 'decade'] = '60s'
    yearly_genres.loc[(yearly_genres['date'] >= 1970) & (yearly_genres['date'] <= 1979), 'decade'] = '70s'
    yearly_genres.loc[(yearly_genres['date'] >= 1980) & (yearly_genres['date'] <= 1989), 'decade'] = '80s'
    yearly_genres.loc[(yearly_genres['date'] >= 1990) & (yearly_genres['date'] <= 1999), 'decade'] = '90s'
    yearly_genres.loc[(yearly_genres['date'] >= 2000) & (yearly_genres['date'] <= 2009), 'decade'] = '00s'
    yearly_genres.loc[(yearly_genres['date'] >= 2010) & (yearly_genres['date'] <= 2019), 'decade'] = '10s'

    return yearly_genres

# genre plotter function
def single_genre_plotter(yearly_genres, genre_code, label, sub_dim, sub_order):
    '''
    Plot the time series graph of a single genre.
    
    Input:
        yearly_genres: yearly genre data, dataframe
        genre_code: name of the genre in the data, str
        label: name that you want to see in the plot, str
        sub_dim: subplot dimensions, tuple
        sub_order: order in the subplot, int
        
    Plots the desired graph.
    '''
    assert isinstance(yearly_genres, pd.core.frame.DataFrame)
    assert isinstance(genre_code, str)
    assert isinstance(label, str)
    assert isinstance(sub_dim, tuple)
    assert isinstance(sub_order, int)
    
    plt.subplot(sub_dim[0], sub_dim[1], sub_order)
    plt.plot(yearly_genres['date'], yearly_genres[genre_code])
    plt.title(label)
    plt.ylabel('Fraction of Artists')
    #plt.xlabel('Year')
    plt.ylim([0, 0.7])
    #plt.show()

# radar plot function
def radar_plotter(decade_genres, decade, subshape = (3, 2), suborder = 1):
    '''
    Create radar plots out of decade genre popularities.
    
    Input:
        decade_genres : decade average genre popularities, pandas dataframe 
        decade: code of the decade we want to plot, str 
        subshape : shape of the subplot, tuple
        suborder: order in subplot: int
    '''
    from math import pi
    
    assert isinstance(decade_genres, pd.core.frame.DataFrame)
    assert isinstance(decade, str)
    assert isinstance(subshape, tuple)
    assert isinstance(suborder, int)
    
    # number of variable
    categories=list(decade_genres[decade_genres['decade'] == decade].drop(columns = 'decade'))
    N = len(categories)
     
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=decade_genres[decade_genres['decade'] == decade].drop(columns = 'decade').values.flatten().tolist()
    values += values[:1]
    values
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
     
    # Initialise the spider plot
    ax = plt.subplot(subshape[0], subshape[1], suborder, polar=True)
    plt.subplots_adjust(left=None, bottom=.06, right=None, top=.91, wspace=0, hspace=.45)
    
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.ylim(0, 0.65)
    plt.yticks(color = 'black', size=8)
    
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')
     
    # Fill area
    colors = ['red', 'green', 'blue', 'coral', 'cyan', 'magenta']
    
    ax.fill(angles, values, colors[suborder - 1], alpha=0.3)
    
    # title
    plt.title(f'Artist Genres: {decade}', y = 1.15)

########################
# Main

def main():
    # Call Data Prep Function
    combined_df = read_combined_data(git_path = os.getcwd(), combined_path = '/data/combined_dataset/')
    
    # Call Genre Summarizer
    yearly_genres = yearly_genre_prep(combined_df)
    
    #rise or No Change
    single_genre_plotter(yearly_genres, 'pop', 'Pop', (2, 2), 1)
    single_genre_plotter(yearly_genres, 'electronic_dance_disco', 'Dance', (2, 2), 2)
    single_genre_plotter(yearly_genres, 'country', 'Country', (2, 2), 3)
    single_genre_plotter(yearly_genres, 'hip_hop', 'Rap', (2, 2), 4)
    
    #dying
    single_genre_plotter(yearly_genres, 'rock', 'Rock', (2, 2), 1)
    single_genre_plotter(yearly_genres, 'adult_standards', 'Adult Standards', (2, 2), 2)
    single_genre_plotter(yearly_genres, 'funk_soul', 'Funk & Soul', (2, 2), 3)
    single_genre_plotter(yearly_genres, 'rnb', 'R & B', (2, 2), 4)
    
    single_genre_plotter(yearly_genres, 'jazz', 'Jazz', (2, 2), 1)
    single_genre_plotter(yearly_genres, 'blues', 'Blues', (2, 2), 2)
    single_genre_plotter(yearly_genres, 'folk', 'Folk', (2, 2), 3)
    
    # long history
    
    #60s
    plt.plot(yearly_genres['date'], yearly_genres['adult_standards'], label = 'Adult standards', alpha = 1, linewidth=3.3)
    plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 1, linewidth=3.3)
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
    plt.plot(yearly_genres['date'], yearly_genres['rock'], label = 'Rock', alpha = 1, linewidth=3.3)
    plt.plot(yearly_genres['date'], yearly_genres['electronic_dance_disco'], label = 'Dance', alpha = 1, linewidth=3.3)
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
    plt.plot(yearly_genres['date'], yearly_genres['pop'], label = 'Pop', alpha = 1, linewidth=3.3)
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
    plt.plot(yearly_genres['date'], yearly_genres['hip_hop'], label = 'Rap', alpha = 1, linewidth=3.3)
    plt.legend(loc = 1, bbox_to_anchor=(1.13, 1.02))
    plt.title('Artist Genres 1960-2020')
    plt.ylabel('Fraction of Artists')
    plt.xlabel('Year')
    plt.show()
    
    # check latest year distribution
    pd.DataFrame(yearly_genres[yearly_genres['date'] == 2019].drop(columns = 'date').T).reset_index().sort_values(by = 59)
    
    # summarize genres by decade, Radar Plots
    filter_columns = ['electronic_dance_disco', 'funk_soul', 'hip_hop', 'pop', 'rock', 'country', 
                      'blues', 'folk', 'adult_standards']
    
    new_names = ['Dance', 'Funk & Soul', 'Rap', 'Pop', 'Rock', 'Country', 
                      'Blues', 'Folk', 'Adult Standards']
    
    decade_genres = yearly_genres.groupby(['decade'])[filter_columns].mean().reset_index()
    decade_genres.rename(columns = dict(zip(filter_columns, new_names)), inplace = True)
    
    radar_plotter(decade_genres, '60s', (3, 2), 1)
    radar_plotter(decade_genres, '70s', (3, 2), 2)
    radar_plotter(decade_genres, '80s', (3, 2), 3)
    radar_plotter(decade_genres, '90s', (3, 2), 4)
    radar_plotter(decade_genres, '00s', (3, 2), 5)
    radar_plotter(decade_genres, '10s', (3, 2), 6)

if __name__ == '__main__':
	main()