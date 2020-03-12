import math
import pandas as pd

yearly_tempo = {} # key: year, value: average tempo of songs

def statgenre(genre_of_year, genre_dict):
    ''' statistic the genre of all 60 years '''
    assert isinstance(genre_of_year, list)
    for genres in genre_of_year:
        if isinstance(genres, float):
            continue
        for genre in eval(genres):
            if not genre in genre_dict:
                genre_dict[genre] = 1
            else:
                genre_dict[genre] += 1
                
def traverse_dataset():
    ''' get all the genres from the dataset '''
    yearly_genre = {}
    for year in range(1960, 2021):
        df = pd.read_csv('/data/combined_dataset/lyrics&features_{}.csv'.format(year))
        yearly_genre[year] = {}
        statgenre(df['artist_genres'], yearly_genre[year])
    return yearly_genre

res = traverse_dataset()

dataframe = pd.DataFrame(res)

dataframe.to_csv("test.csv",index=True,sep=',')
print("success")

for i in res:
    sorted_genre = sorted(res[i], key=lambda x: res[i][x], reverse=True)
    print(i, sorted_genre[:5])
# get top 5 genres appeared most in the past 60 years