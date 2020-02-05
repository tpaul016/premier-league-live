import secrets
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
import json
import csv
import re # regular epression
# import preprocessor as p
import os
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string

auth = OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_key, secrets.access_secret)
api = API(auth)

# declare file paths for csv files
premier_league_tweets = "data/premier_league_tweets.csv"

# columns of the csv file
COLS = ['id', 'created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang',
        'original_author', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
])

# Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

# combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)

    # after tweepy preprocessing the colon left remain after removing mentions
    # or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    # filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []

    # looping through conditions
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)

def get_tweets(keyword, file):
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        # df = pd.DataFrame(columns=COLS)
        df = pd.DataFrame(columns=["tweet"])

    for page in Cursor(api.search, q=keyword, count=200, include_rts=False).pages(2):
        for item in page:
            new_entry = []
            tweet = item._json

            # check if language is english
            if tweet['lang'] != 'en':
                continue

            new_entry.append(tweet['text'])
            # clean_text = p.clean(tweet['text'])
            # filtered_tweet = clean_tweets(clean_text)
            # print(filtered_tweet)
            #
            # blob = TextBlob(filtered_tweet)
            # sentiment = blob.sentiment
            # polarity = sentiment.polarity
            # subjectivity = sentiment.subjectivity
            #
            # new_entry += [tweet['id'], tweet['created_at'], tweet['source'], tweet['text'], filtered_tweet, sentiment, polarity, subjectivity, tweet['lang']]
            #
            # new_entry.append(tweet['user']['screen_name'])
            #
            # try:
            #     is_sensitive = tweet['possibly_sensitive']
            # except KeyError:
            #     is_sensitive = None
            # new_entry.append(is_sensitive)
            #
            # hashtags = ", ".join([hashtag_item['text'] for hashtag_item in tweet['entities']['hashtags']])
            # new_entry.append(hashtags)
            # mentions = ", ".join([mention['screen_name'] for mention in tweet['entities']['user_mentions']])
            # new_entry.append(mentions)
            #
            # try:
            #     location = tweet['user']['location']
            # except TypeError:
            #     location = ''
            # new_entry.append(location)
            #
            # try:
            #     coordinates = [coord for loc in tweet['place']['bounding_box']['coordinates'] for coord in loc]
            # except TypeError:
            #     coordinates = None
            # new_entry.append(coordinates)

            # single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            single_tweet_df = pd.DataFrame([new_entry], columns=["tweet"])
            df = df.append(single_tweet_df, ignore_index=True)
            csvFile = open(file, 'a', encoding="utf-8")
            print('tweet processed')
    # df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")
    df.to_csv(csvFile, mode='a', columns=["tweet"], index=False, encoding="utf-8")

get_tweets("TOTMCI",premier_league_tweets)