#!/usr/bin/env python3

import os
import sys
import argparse
import csv

try:
    import auth_check as ack
except ImportError:
    print("[ERROR] Unable to import Auth. module: can't run!")
    sys.exit()
try:
    import scraper as scr
except ImportError:
    print("[ERROR] Unable to import Scraper module: can't run!")
    sys.exit()
try:
    import post_processing as pp
except ImportError:
    print("[ERROR] Unable to import Post processing module: can't run!")
    sys.exit()
try:
    import common_utils as cu
except ImportError:
    print("[ERROR] Unable to import Common Utils module: can't run!")
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser(
        description='Script retrieves tweets with one/more hashtags')
    parser.add_argument(
        '-a',
        '--auth',
        type=str,
        help='User auth. file',
        required=True)
    parser.add_argument(
        '-o',
        '--ofile',
        type=str,
        help='CSV output filename',
        required=False,
        default="tweet_search.csv")
    parser.add_argument(
        '-n',
        '--tnum',
        type=int,
        help='Number of tweets to get',
        required=True,
        default=500)
    parser.add_argument(
        '-t',
        '--hashtag',
        type=str,
        help='Hashtag to search',
        required=True)

    args = parser.parse_args()
    uauth = args.auth
    outfile = args.ofile
    num = int(args.tnum)
    hashtag = args.hashtag

    return uauth, outfile, num, hashtag


if __name__ == "__main__":

    try:

        fwriter = cu.FastWriter()

        uauth, outfile, num, hashtag = get_args()
        parsed_data = ((str(outfile))[:-4]) + "_sentiment.csv"

        print("[INFO] Twitter extraction tool\n")

        auth = ack.Authenticator()
        auth = auth.auth_setup(uauth)

        tweets = scr.Scraper()
        tweets = tweets.get_tweets(auth, outfile, num, hashtag)

        ptweets = [
            tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [
            tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        neutral = len(tweets) - len(ntweets) - len(ptweets)

        try:
            print("\n[ANALYSIS] 'Tweet sentiment' data processing")
            print("[POSITIVE | NEGATIVE | NEUTRAL  ]")
            print("[ {:.2f} %".format(100 * len(ptweets) / len(tweets)),
                  "|  {:.2f} %".format(100 * len(ntweets) / len(tweets)),
                  "|  {:.2f} %".format(100 * neutral / len(tweets)),
                  "]")

            elem = pp.PostProcessor()

            pos_map = elem.evaluate_text(
                parsed_data, str(hashtag), "positive")
            neg_map = elem.evaluate_text(
                parsed_data, str(hashtag), "negative")
            nt_map = elem.evaluate_text(
                parsed_data, str(hashtag), "neutral")

            pos_list = list()
            neg_list = list()
            nt_list = list()

            [pos_list.append(pos_map[key]) for key in pos_map]
            [neg_list.append(neg_map[key]) for key in neg_map]
            [nt_list.append(nt_map[key]) for key in nt_map]

            final_pos = dict()
            final_neg = dict()
            final_nt = dict()

            for _z in pos_list:
                for e in _z:
                    final_pos[e] = int(final_pos.get(e, 0) + 1)

            for x in neg_list:
                for y in x:
                    final_neg[y] = int(final_neg.get(y, 0) + 1)

            for w in nt_list:
                for t in w:
                    final_nt[t] = int(final_nt.get(t, 0) + 1)

            p_file = ((str(outfile))[:-4]) + "_most_pos.csv"
            n_file = ((str(outfile))[:-4]) + "_most_neg.csv"
            nt_file = ((str(outfile))[:-4]) + "_most_nt.csv"

            fwriter.fast_writer(
                p_file,
                final_pos
            )

            fwriter.fast_writer(
                n_file,
                final_neg
            )

            fwriter.fast_writer(
                nt_file,
                final_nt
            )
        except ZeroDivisionError:
            print("[ERROR] Zero Results for requested search! Exit...")
            sys.exit()

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
        sys.exit()
