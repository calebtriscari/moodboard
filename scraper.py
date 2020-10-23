#boilerplate

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import datetime

datetoday = str(datetime.date.today())

#get the chart entries for a particular week

chartURL = 'https://www.billboard.com/charts/hot-100/'
chartPage = requests.get(chartURL)
chartSoup = BeautifulSoup(chartPage.content, 'html.parser')
chartBlock = chartSoup.find(class_='chart-list container')
chartEntries = chartBlock.find_all(class_='chart-element__information')

#establish data frame

schema = {'Song':[],'Artist':[],'Lyrics':[],'Sentiment':[]}
df1 = pd.DataFrame(schema)

#hone in on song titles and artist name(s)

for chartEntry in chartEntries:
    songtitle = chartEntry.find(class_='chart-element__information__song text--truncate color--primary')
    artistname = chartEntry.find(class_='chart-element__information__artist text--truncate color--secondary')
    songtitle = songtitle.text
    artistname = artistname.text

    newdata = {'Song':songtitle,'Artist':artistname,'Lyrics':[],'Sentiment':[]}
    df1 = df1.append(newdata, ignore_index=True)

#export data frame for later use

df1.to_csv('weeks/df'+datetoday+'.csv', index=False)
