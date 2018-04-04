
# coding: utf-8

# ### Gaurav Pareek (801020037)

# In[1]:

import tweepy
import time


# In[2]:

ACCESS_TOKEN = '151445560-31q1c7aL0sOlyBTJy2fdaceiA5bDF4I3N4ECZ72l'
ACCESS_SECRET = 'xZ6PWg2dlEymB3IRnLmSxDiPHGxpvYqJyaqVb31jD3yBw'
CONSUMER_KEY = 'hGC8cBotnf6HKf0Z5GZnjJ1jI'
CONSUMER_SECRET = 'FscvEOdJMHqPS9GQPnZJWy9ZtZC9Ez19dh4KK6joQt1n9ClROm'
SEARCH = input("Enter the search string ")
FROM = input("Enter the from date (YYYY-MM-DD format) ")
TO = input("Enter the to data (YYYY-MM-DD format) ")
INPUT_FILE_PATH = './'+SEARCH+'.txt'

num=int(input("Enter the number of tweets you want to retrieve for the search string "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
i=0;

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')

#tweets = tweepy.Cursor(api.search, q=SEARCH, rpp=100, count=20, since=FROM, until=TO, lang="en").items(num)
tweets = tweepy.Cursor(api.search, q=("{}&since:{}&until:{}").format(SEARCH,FROM,TO), rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(num)

for res in tweets:
   i+=1
   f.write(res.user.screen_name)
   f.write(' ')
   f.write('[')
   f.write(res.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"))
   f.write(']')    
   f.write(" ")
   f.write('"')
   f.write(res.text.replace('\n', ''))
   f.write('"')
   f.write(" ")
   f.write(str(res.user.followers_count))
   f.write(" ")
   f.write(str(res.retweet_count))
   f.write('\n')
f.close
print("Tweets retrieved ", i)


# #### References
# https://stackoverflow.com/questions/12703842/how-to-tokenize-natural-english-text-in-an-input-file-in-python
# https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
# https://stackoverflow.com/questions/12703842/how-to-tokenize-natural-english-text-in-an-input-file-in-python
# https://stackoverflow.com/questions/12070193/why-is-datetime-strptime-not-working-in-this-simple-example

# In[3]:

import nltk
from nltk import word_tokenize
import pandas as pd
import numpy as np
from datetime import datetime


# In[4]:

with open(INPUT_FILE_PATH,encoding='utf8') as f:
    contentData = f.readlines()


# In[5]:

contentData


# In[6]:

tweets = []
for item in contentData:
    temp=[]
    tokens = word_tokenize(item)
    # fetching data according to the columns
    user = tokens[0]
    time = datetime.strptime(tokens[2],"%d/%b/%Y:%H:%M:%S")
    tweetText = ' '.join(tokens[5:len(tokens)-3])
    followers = (tokens[len(tokens)-2])
    retweetCount = (tokens[len(tokens)-1])
    # appending data into array so that I can read into dataframe
    temp.append(user)
    temp.append(time)
    temp.append(tweetText)
    temp.append(followers)
    temp.append(retweetCount)
    tweets.append(temp)


# In[7]:

dataframe = pd.DataFrame(tweets, columns=['User', 'Time','TweetText','Followers','RetweetCount'])
dataframe.head()


# ### a.	The top n users who have tweeted the most for the entire timeline.

# #### References : 
# https://stackoverflow.com/questions/19384532/how-to-count-number-of-rows-in-a-group-in-pandas-group-by-object
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html

# In[8]:

tp = dataframe.groupby(['User']).size().reset_index(name='no_of_tweet_counts')
tp = tp.sort_values(by = tp.columns[1],ascending = False)
tp.to_csv('topNusers.csv')
tp.head()


# ### b. The top n users who have tweeted the most for every hour.

# #### References : 
# https://stackoverflow.com/questions/16923281/pandas-writing-dataframe-to-csv-file
# https://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/

# In[9]:

# Here I have used python lamda function to fetch hour from datatime object and appended same to the dataframe
dataframe["Hour"] = dataframe["Time"].apply(lambda time:time.hour).astype(int).astype(str)

# fetching all hours from data then interative through for loop for each hour data

totalHours = dataframe['Hour']
totalHours.head()

hoursData = []
for dayhour in totalHours:
    hoursData.append(str(dayhour))

for everyHour in hoursData:
    tp1 = dataframe.loc[dataframe['Hour'] == everyHour]
    tp1 = dataframe.groupby(['User']).size().reset_index(name='no_of_tweet_counts')
    tp1 = tp.sort_values(by = tp1.columns[1],ascending = False)
    tp1.to_csv('HourNo'+everyHour+'.csv')
tp1.head()


# ### c.	The top n users who have the maximum followers.

# #### References
# https://stackoverflow.com/questions/39173813/pandas-convert-dtype-object-to-int
# 

# In[14]:

tp2 = dataframe.groupby(['User','Followers']).size().reset_index()
val = tp2['Followers']
# Here followers data type is object so we need to convert it to int to sort values for it
tp2['Followers'] = tp2['Followers'].astype(str).astype(int)
tp2 = tp2.sort_values(by = ['Followers'],ascending=False).head()
tp2.to_csv('topNUser_MaxFollowers.csv')
tp2.head()


# ### d.	The top n tweets which have the maximum retweet count

# In[15]:

# Here we need to do it tweet wise
tp3 = dataframe.groupby(['TweetText','RetweetCount']).size().reset_index()
tp3['RetweetCount'] = tp3['RetweetCount'].astype(str).astype(int)
result = tp3.sort_values(by = ['RetweetCount'],ascending=False)
result.to_csv('topNtweets_MaxRetweetCount.csv')
result.head()

