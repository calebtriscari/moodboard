#boilerplate

import lyricsgenius
import pandas as pd
from geniuskey import geniuskey
import datetime

genius = lyricsgenius.Genius(geniuskey)
datetoday = str(datetime.date.today())

#import dataframe

df1 = pd.read_csv('weeks/df'+datetoday+'.csv')
mdb = pd.read_csv('mdb.csv')

#find lyrics, add to df1

for row in df1.index:
    if ((mdb['Song'] == df1.Song[row]) & (mdb['Artist'] == df1.Artist[row])).any():
        try:
            entry = mdb[mdb['Song'].str.match(df1.Song[row]) & mdb['Artist'].str.match(df1.Artist[row])]
            entryind = entry.index[0]
            df1.at[row, 'Lyrics'] = mdb.Lyrics[entryind]
        except:
            df1.at[row, 'Lyrics'] = 'None'
    else:
        songtitle = df1['Song'][row]
        artistname = df1['Artist'][row]
        trycount = 0

        while trycount < 3:
            try:
                song = genius.search_song(songtitle, artistname)
                lyrics = song.lyrics
                df1.at[row, 'Lyrics'] = lyrics
                trycount = 3

            except:
                lyrics = 'None'
                df1.at[row, 'Lyrics'] = lyrics
                trycount = trycount + 1
    
#export data frame for later use

df1.to_csv('weeks/df'+datetoday+'.csv', index=False)
