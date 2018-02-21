import os
import datetime
import sys
import csv
import re
import time, datetime
try:
    import text_sentiment as sc
except ImportError:
    print("[ERROR] Unable to import text_sentiment module: can't run!")
    sys.exit()
try:
    from textblob import TextBlob
except ImportError:
    print("[ERROR] Unable to import TextBlob module: can't run!")
    sys.exit()
try:
    import tweepy
except ImportError:
    print("[ERROR] Unable to import Tweepy module: can't run!")
    sys.exit()

class Scraper():

    def __init__(self):
        self._api = ""

    def get_tweets(self, api, data, num, targets):
        self._api = api
        self._data = data
        self._num = int(num)
        self._targets = targets
        self._tweets = []

        self._analyzer = sc.TweetSentiment()

        try:
            if os.name == "nt":
                self._csv_tweet = open(self._data, 'w', encoding='utf-8', newline='')
            else:
                self._csv_tweet = open(self._data, 'w')
            self._csv_tweet_writer = csv.writer(self._csv_tweet)
            self._csv_tweet_writer.writerow(["created_at", "location", "user", "full_text"])

            self._parsed_data = ((str(self._data))[:-4])+"_sentiment.csv"
            self._csv_data = open(self._parsed_data, 'w')
            self._csv_data_writer = csv.writer(self._csv_data)
            self._csv_data_writer.writerow(["tweet", "sentiment"])

        except:
            print("[ERROR] Unable to prepare CSV files!")
            sys.exit()


        print("[*] Fetching tweets and processing 'tweets sentiment' data")
        print("[*] Please, wait...\n")

        try:

            for self._tweet in tweepy.Cursor(self._api.search, q=self._targets, count=self._num,
                    lang="en", tweet_mode="extended").items(self._num):

                try:
                    self._csv_tweet_writer.writerow([
                            self._tweet.created_at,
                            self._tweet.user.location,
                            self._tweet.user.screen_name.encode('utf-8'),
                            self._tweet.full_text.encode('ascii', errors='ignore'),
                            ])
                except:
                    print("[ERROR] Unable to write tweets on file: ", self._data)
                    sys.exit()

                try:
                    self._parsed_tweet = {}
                    self._parsed_tweet['user'] = self._tweet.user.screen_name.encode('utf-8')
                    self._parsed_tweet['text'] = self._tweet.full_text.encode('ascii', 'ignore')
                    self._parsed_tweet['sentiment'] = self._analyzer.get_tweet_sentiment(self._tweet.full_text)

                    if self._tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if self._parsed_tweet not in self._tweets:
                            self._tweets.append(self._parsed_tweet)
                    else:
                        self._tweets.append(self._parsed_tweet)

                    self._csv_data_writer.writerow([
                            self._tweet.full_text.encode('ascii', 'ignore'),
                            self._parsed_tweet['sentiment']
                            ])
                except:
                    print("[ERROR] Unable to write analysis on file: ", self._parsed_data)
                    sys.exit()

            print("[SUCCESS] Tweets written on file: ", self._data)
            print("[SUCCESS] Tweets sentiment analysis written on: ", self._parsed_data)

            return self._tweets

        except tweepy.TweepError as e:
            print("[ERROR: TWEEPY API] " + str(e))
            sys.exit()
        except:
            print("[ERROR] Unable to get/save tweets!")
            sys.exit()
