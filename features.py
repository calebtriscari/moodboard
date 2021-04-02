#boilerplate

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
# from spotifykeys import *
import datetime

client_id = '192811e553a94d6ea5e7a11a27266b56'
client_secret = '1b03b99e7150493c8447f722b800bcfe'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

datetoday = str(datetime.date.today())

#import dataframe

df1 = pd.read_csv('weeks/df'+datetoday+'.csv')
df1['Date'] = df1['Date'].astype('string')
mdb = pd.read_csv('mdb.csv')

#find features, add to df1

for row in df1.index:
    if ((mdb['Song'] == df1.Song[row]) & (mdb['Artist'] == df1.Artist[row])).any():
        try:
            entry = mdb[mdb['Song'].str.match(df1.Song[row]) & mdb['Artist'].str.match(df1.Artist[row])]
            entryind = entry.index[0]
            df1.at[row, 'Valence'] = mdb.Valence[entryind]
            df1.at[row, 'Key'] = mdb.Key[entryind]
            df1.at[row, 'Mode'] = mdb.Mode[entryind]
            df1.at[row, 'Danceability'] = mdb.Danceability[entryind]
            df1.at[row, 'Date'] = mdb.Date[entryind]
        except:
            df1.at[row, 'Valence'] = None
    else:
        songtitle = df1['Song'][row]
        artistname = df1['Artist'][row]
        artist_words = artistname.split(' ')
        artist_first = artist_words[0]
        trycount = 0

        print(songtitle)

        while trycount < 2:
            try:
                results = sp.search(q = songtitle + ' ' + artist_first, type = 'track', limit = 1)
                t_id = results['tracks']['items'][0]['id']
                r_date = results['tracks']['items'][0]['album']['release_date']
                t_features = sp.audio_features(t_id)

                t_val = t_features[0]['valence']
                t_key = t_features[0]['key']
                t_mode = t_features[0]['mode']
                t_dance = t_features[0]['danceability']

                print(t_val)

                df1.at[row, 'Valence'] = t_val
                df1.at[row, 'Key'] = t_key
                df1.at[row, 'Mode'] = t_mode
                df1.at[row, 'Danceability'] = t_dance
                df1.at[row, 'Date'] = r_date

                trycount = 3
                print(t_val)

            except Exception as e:
                df1.at[row, 'Valence'] = None
                df1.at[row, 'Key'] = None
                df1.at[row, 'Mode'] = None
                df1.at[row, 'Danceability'] = None
                df1.at[row, 'Date'] = None

                trycount = trycount + 1

                print(e)

#export data frame for later use

df1.to_csv('weeks/df'+datetoday+'.csv', index=False)
