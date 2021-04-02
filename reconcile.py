#boilerplate

import pandas as pd
import datetime
import numpy as np

datetoday = str(datetime.date.today())

#import dataframes

df1 = pd.read_csv('weeks/df'+datetoday+'.csv', na_values=True)
mdb = pd.read_csv('mdb.csv')
weektracker = pd.read_csv('weektracker.csv')

#search incomplete entries in df1 for complete entries in mdb - OBSOLETE

#for row in df1.index:
#    if df1.Lyrics[row] == 'None':
#        for entry in mdb.index:
#            if mdb.Song[entry] == df1.Song[row] and mdb.Artist[entry] == df1.Artist[row]:
#                df1.at[row, 'Lyrics'] = mdb.Lyrics[entry]
#                df1.at[row, 'Sentiment'] = mdb.Sentiment[entry]

#generate weekly sentiment and song data, add to sentiweek

maxindex = df1.Valence.idxmax()
minindex = df1.Valence.idxmin()

newweek = {'Week':datetoday,'Mean':round(df1.Valence.mean(), 4),'Median':round(df1.Valence.median(), 4),
           'SD':round(df1.Valence.std(),4), 'MaxValence':round(df1.Valence.max(),4), 'MaxSong':df1['Song'][maxindex],
           'MaxArtist':df1['Artist'][maxindex], 'MinValence':round(df1.Valence.min(), 4), 'MinSong':df1['Song'][minindex],
           'MinArtist':df1['Artist'][minindex]}

weektracker = weektracker.append(newweek, ignore_index=True)

#add all songs from df1 to mdb, remove duplicates, and export

newentries = df1[df1['Valence'] != None]
mdb = mdb.append(newentries, ignore_index=True)
mdb = mdb.drop_duplicates()

#export all dataframes

df1.to_csv('weeks/df'+datetoday+'.csv', index=False)
weektracker.to_csv('weektracker.csv', index=False)
mdb.to_csv('mdb.csv', index=False)
