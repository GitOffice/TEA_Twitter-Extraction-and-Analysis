import os
import datetime
import sys
import csv
import re
import time
import datetime
from datetime import datetime
from collections import OrderedDict
try:
    import tweepy
except ImportError:
    print("[ERROR] Unable to import Tweepy module: can't run!")
    sys.exit()

class TimelineScraper():

    def __init__(self):
        self._status = ""

    def get_timeline(self, api, analyzer, target, data):
        try:
            if os.name == "nt":
                self._csv_tweet = open(
                    data, 'w', encoding='utf-8', newline='')
            else:
                self._csv_tweet = open(data, 'w')

            self._csv_tweet_writer = csv.writer(self._csv_tweet)
            self._csv_tweet_writer.writerow(
                ["created_at", "location", "full_text", "polarity", "subjectivity"])

        except BaseException:
            print("[ERROR] Unable to prepare CSV files!")
            sys.exit()

        try:
            print("[*] Downloading '", target, "' timeline")
            print("[*] Please, wait...")
            for self._tweet in tweepy.Cursor(
                    api.user_timeline,
                    id=target,
                    tweet_mode="extended").items():

                self._curr_date = (datetime.strptime(
                    str(self._tweet.created_at), "%Y-%m-%d %H:%M:%S")).date()

                self._tweet_dec_text = self._tweet.full_text.encode(
                    'ascii',
                    errors='ignore')

                self._curr_elem = analyzer.get_tweet_sentiment_data(
                    self._tweet.full_text)
                self._curr_polarity = self._curr_elem[0]
                self._curr_subjectivity = self._curr_elem[1]

                try:
                    self._csv_tweet_writer.writerow([
                        self._curr_date,
                        self._tweet.user.location,
                        self._tweet_dec_text,
                        self._curr_polarity,
                        self._curr_subjectivity
                    ])

                except Exception as e:
                    print(
                        "[ERROR] Unable to write tweets on file: ",
                        data, ", details: ", e)
                    sys.exit()

        except tweepy.TweepError as e:
            if e.api_code == 429:
                print("[ERROR: TWEEPY API] Too many requests. Wait some minutes.")
            else:
                print("[ERROR: TWEEPY API] " + str(e.text))
            sys.exit()
        except Exception as e:
            print("[ERROR]: ", e)
            sys.exit()