import os
import sys
import csv
import time

try:
    import tweepy
except ImportError:
    print("[ERROR] Unable to import Tweepy module: can't run!")
    sys.exit()


class FollowerScraper:

    def __init__(self):
        self._status = ""
        self._followers = list()
        self._csv_tweet = ""
        self._csv_tweet_writer = ""
        self._curr_follower = ""

    def get_followers(self, api, target, data):
        try:
            if os.name == "nt":
                self._csv_tweet = open(
                    data, 'w', encoding='utf-8', newline='')
            else:
                self._csv_tweet = open(data, 'w')

            self._csv_tweet_writer = csv.writer(self._csv_tweet)
            self._csv_tweet_writer.writerow(
                ["username"])

        except Exception as e:
            print("[ERROR] Unable to prepare CSV files!")
            print("\n[Details]: ", e)
            sys.exit()

        while True:
            try:
                print("[*] Downloading '", target, "' followers list")
                print("[*] Please, wait...")
                for self._tweet in tweepy.Cursor(
                        api.followers,
                        screen_name=target,
                        count=200
                ).items():

                    self._curr_follower = self._tweet.screen_name
                    print(self._curr_follower)

                    try:
                        self._csv_tweet_writer.writerow([
                            self._curr_follower
                        ])

                    except Exception as e:
                        print(
                            "[ERROR] Unable to write tweets on file: ",
                            data, ", details: ", e)
                        sys.exit()

            except tweepy.error.RateLimitError as e:
                print("[ERROR: TWEEPY API] Too many requests. Wait some minutes.")
                time.sleep(15 * 60)
            except tweepy.TweepError as e:
                if e.api_code == 429:
                    print("[ERROR: TWEEPY API] Too many requests. Wait some minutes.")
                    time.sleep(15 * 60)
                else:
                    print("[ERROR: TWEEPY API] " + str(e.text))
                sys.exit()
            except Exception as e:
                print("[ERROR]: ", e)
                sys.exit()
