#boilerplate

import tweepy
import datetime
import pandas as pd
import random
from twitterkeys import *

datetoday = str(datetime.date.today())

#TWITTER API Keys

#import dataframe

df1 = pd.read_csv('weeks/df'+datetoday+'.csv', na_values = True)
tracker = pd.read_csv('weektracker.csv')

#define vibes

depressed = ['depressing', 'grim', 'despondent', 'upsetting', 'awful','terrible']
glum = ['not great', 'bleh', 'gloomy','down', 'glum']
chill = ['chill', 'groovy', 'pretty fine', 'upbeat', 'nice', 'pretty sweet']
thrilled = ['lit', 'over the top', 'thrilling', 'next level', 'wild']

#assign variables

maxindex = df1.Sentiment.idxmax()
minindex = df1.Sentiment.idxmin()
senti = df1.Sentiment.mean()
maxsong = df1.Song[maxindex]
maxartist = df1.Artist[maxindex]
minsong = df1.Song[minindex]
minartist = df1.Artist[minindex]
q1 = tracker.Mean.quantile(0.25)
med = tracker.Mean.median()
q3 = tracker.Mean.quantile(0.75)

#find vibe

if senti <= q1:
    x = random.randint(0, len(depressed)-1)
    mood = depressed[x]
elif q1 < senti <= med:
    x = random.randint(1, len(glum)-1)
    mood = glum[x]
elif med < senti <= q3:
    x = random.randint(0, len(chill)-1)
    mood = chill[x]
elif senti > q3:
    x = random.randint(0, len(thrilled)-1)
    mood = thrilled[x]

#construct grammar

phrase = 'Hey. The vibe for this week was '+mood+'.\nThe most positive song this week was '+maxsong+' by '+maxartist+'.\nThe most negative song this week was '+minsong+' by '+minartist+'.'

#tweet

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status(phrase)
