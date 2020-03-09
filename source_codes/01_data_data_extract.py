! pip install billboard.py
import billboard
hot_list_100 = {}

# chart = billboard.ChartData('hot-100', '1998-02-01')
chart = billboard.ChartData('hot-100')


# Try to get the previous top100 list
# You may not want to run this part of code, it's just a test and will never stop
while chart.previousDate:
    year = chart.date.split("-")[0]
    if(year == "1959"):
        break
    if not year in hot_list_100:
        print(year)
        hot_list_100[year] = {}
    for i in chart:
        if i in hot_list_100[year]:
            hot_list_100[year][i]['cnt'] += 1
            hot_list_100[year][i]['rank'].append(i.rank)
        else:
#             print(i.title)
#             print(i)
            hot_list_100[year][i] = {}
            hot_list_100[year][i]['cnt'] = 1
            hot_list_100[year][i]['rank'] = [i.rank]
            hot_list_100[year][i]['artist'] = i.artist
            hot_list_100[year][i]['title'] = i.title
        

    # print(chart)
    while True:
        try:
            chart = billboard.ChartData('hot-100', chart.previousDate)
        except:
            print("error")
        else:
            break


import pandas as pd

dataframe = pd.DataFrame({'hot_list_100':hot_list_100})

dataframe.to_csv("songlist.csv",index=True,sep=',')
print("success")
# Save the data in csv file


import lyricsgenius
# This is my lyricsgenius id
genius = lyricsgenius.Genius("lISrOoq8wD1T9e_Ta1ggsWuEnf9eeHfTWR-pSSV5puvg5ZYh-K9J9tX515Xg4wL8")


# Try to get the lyrics and some other information of a song
# title, lyrics, artist, date
for i in range(1999, 2021):
    title = []
    lyrics = []
    artists = []
    artists_from_list = []
    rank = []
    cnt = []
    date = []
    for year in hot_list_100:
        if year != str(i):
            continue
        hotlist = hot_list_100[year]
        # print(hotlist)
        for song in hotlist:
            try:
                s = genius.search_song(song + ' by ' + hotlist[song]['artist'])
                if s == None:
                    continue
            except:
                continue
            else:
                title.append(song)
                lyrics.append(s.lyrics)
                artists.append(s.artist)
                artists_from_list.append(hotlist[song]['artist'])
                date.append(year)
                rank.append(hotlist[song]['rank'])
                cnt.append(hotlist[song]['cnt'])
    # there's a small part of song cannot be found, about 3%

    dataframe = pd.DataFrame({'title':title, 'lyrics':lyrics, 'artistsFromLyrics':artists, 'artists':artists_from_list, 'date':date, 'rank':rank, 'cnt': cnt})

    dataframe.to_csv("lyricsHotListTopNew_" + str(date[0]) + ".csv",index=True,sep=',')
    print("success" + str(i))
# Save the data in csv file