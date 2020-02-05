import secrets
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import pandas as pd

auth = OAuthHandler(secrets.twitter_consumer_key, secrets.twitter_consumer_secret)
auth.set_access_token(secrets.twitter_access_key, secrets.twitter_access_secret)
api = API(auth)

def get_tweets(keyword, date):
    df = pd.DataFrame(columns=["tweet"])
    for page in Cursor(api.search, q=keyword, count=200, include_rts=False).pages(15):
        for item in page:
            new_entry = []

            tweet = item._json

            # check if language is english
            if tweet['lang'] != 'en':
                continue

            tweet_text = tweet['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            # join the the array of words from the tweet with a white-space
            tweet_text = " ".join(tweet_text.split())
            new_entry.append(tweet_text)
            # blob_text += clean_text + ' '

            single_tweet_df = pd.DataFrame([new_entry], columns=["tweet"])
            df = df.append(single_tweet_df, ignore_index=True)
            print('tweet processed')
    return df
