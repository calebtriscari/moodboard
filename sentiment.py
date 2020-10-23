#boilerplate

import pandas as pd
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

datetoday = str(datetime.date.today())
analysis = SentimentIntensityAnalyzer()

#import dataframes

df1 = pd.read_csv('weeks/df'+datetoday+'.csv')

#break up lyrics into list and analyse sentiment

for row in df1.index:
    if df1['Lyrics'][row] != 'None':
        lyrics = df1['Lyrics'][row]
        lyricslist = lyrics.split('\n')
        sentisum = 0.0
        sentin = 0

        for sentence in lyricslist:
            senti = analysis.polarity_scores(sentence)

            if senti['compound'] != 0.0:
                sentisum = sentisum = senti['compound']
                sentin = sentin + 1

        if sentin != 0:
            sentiavg = round(sentisum/sentin, 4)
            
        else:
            sentiavg = np.nan

        #add to dataframe

        df1.at[row, 'Sentiment'] = sentiavg

    else:
        df1.at[row, 'Sentiment'] = np.nan

#export dataframe

df1.to_csv('weeks/df'+datetoday+'.csv', index=False)
