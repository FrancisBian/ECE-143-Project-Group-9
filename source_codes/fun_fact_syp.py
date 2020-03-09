import math
import pandas as pd

yearly_song_list = {} # key: year, value: key:song  value: features

def extract(title, artist, rank, dict):
    l = len(title) 
    for i in range(l):
        dict[title[i]] = {}
        dict[title[i]]["artist"] = artist[i]
        dict[title[i]]["rank"] = rank[i]


                
def traverse_dataset():
    yearly_feature = {}
    for year in range(1960, 2021):
        df = pd.read_csv('/Users/shenyuepeng/Desktop/ece143/ece143project-master/ece143project/data/combined_dataset/lyrics&features_{}.csv'.format(year))
        yearly_feature[year] = {}
        extract(df['title'], df['artists'], df['rank'], yearly_feature[year])
    return yearly_feature

res = traverse_dataset()

# dataframe = pd.DataFrame(res)

# dataframe.to_csv("test.csv",index=True,sep=',')
# print("success")

eachsong = {}
for year in res:
    for song in res[year]:
        temp = song + " by " + res[year][song]['artist']
        if not temp in eachsong:
            eachsong[temp] = eval(res[year][song]['rank'])[::-1]
        else:
            eachsong[temp] = eachsong[temp] + eval(res[year][song]['rank'])[::-1]
print(eachsong)

cnt_two = {}
for song in eachsong:
    cnt = 0
    for rank in eachsong[song]:
        if rank == 1:
            cnt = -1
            break
        if rank == 2:
            cnt += 1
    if cnt <= 0:
        continue
    cnt_two[song] = cnt
ans = sorted(cnt_two, key=lambda x: cnt_two[x], reverse=True)[:10]
print(ans)
for i in ans:
    print(i, cnt_two[i])

merge_two_years = {}
for year in res:
    if not (year+2) in res:
        continue
    merge_two_years[year] = {}
    for song in res[year]:
        temp = song + " by " + res[year][song]['artist']
        merge_two_years[year][temp] = eval(res[year][song]['rank'])[::-1]
        if song in res[year+1] and res[year][song]['artist'] == res[year+1][song]['artist']:
            merge_two_years[year][temp] = merge_two_years[year][temp] + eval(res[year+1][song]['rank'])[::-1]
#print(merge_two_years)

song_jump = {}
for year in merge_two_years:
    for song in merge_two_years[year]:
        hasone = 0
        min = 1
        jump = 1
        for rank in merge_two_years[year][song]:
            if rank == 1:
                hasone = 1
                jump = min
            if rank > min:
                min = rank
        if jump == 1 or hasone == 0:
            continue
        song_jump[song + " " + str(year)] = jump
ans_jump = sorted(song_jump, key=lambda x: song_jump[x], reverse=True)[:30]
for i in ans_jump:
    print(i, song_jump[i])
    print(merge_two_years[int(i[-4:])][i[:-5]])


song_jump = {}
for year in merge_two_years:
    for song in merge_two_years[year]:
        hasone = 0
        min = 1
        jump = 1
        last = 0
        for rank in merge_two_years[year][song]:
            if rank == 1 and last != 0:
                hasone = 1
                if jump < last:
                    jump = last
            last = rank
        if jump == 1 or hasone == 0:
            continue
        song_jump[song + " " + str(year)] = jump
ans_jump = sorted(song_jump, key=lambda x: song_jump[x], reverse=True)[:30]
for i in ans_jump:
    print(i, song_jump[i])
    print(merge_two_years[int(i[-4:])][i[:-5]])


years = {}
for year in res:
    if not (year+1) in res:
        continue
    years[year] = {}
    for song in res[year]:
        temp = song + " by " + res[year][song]['artist']
        years[year][temp] = eval(res[year][song]['rank'])[::-1]
        

song_drop = {}
for year in years:
    for song in years[year]:
        hasone = 0
        min = 1
        drop = 1
        last = 0
        for rank in years[year][song]:
            if last == 1:
                hasone = 1
                if drop < rank:
                    drop = rank
            last = rank
        if drop == 1 or hasone == 0:
            continue
        song_drop[song + " " + str(year)] = drop
ans_drop = sorted(song_drop, key=lambda x: song_drop[x], reverse=True)[:30]
for i in ans_drop:
    print(i, song_drop[i])
    print(years[int(i[-4:])][i[:-5]])