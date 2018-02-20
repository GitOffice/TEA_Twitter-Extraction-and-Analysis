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


def get_args():
  _parser = argparse.ArgumentParser(description='Script retrieves tweets with one/more hashtags')
  _parser.add_argument('-a', '--auth', type=str, help='User auth. file', required=True)
  _parser.add_argument('-o', '--ofile', type=str, help='CSV output filename', required=False, default="tweet_search.csv")
  _parser.add_argument('-n', '--tnum', type=int, help='Number of tweets to get', required=True, default=500)
  _parser.add_argument('-t', '--hashtag', type=str, help='Hashtag to search', required=True)
  _parser.add_argument('-l', '--limitf', type=int, help='Limit hasht. frequency for plotter', required=False, default=50)

  _args = _parser.parse_args()
  _u_auth = _args.auth
  _outfile = _args.ofile
  _num = int(_args.tnum)
  _hashtag = _args.hashtag
  _limit = int(_args.limitf)

  return _u_auth, _outfile, _num, _hashtag, _limit


if __name__ == "__main__":

  try:

    _u_auth, _outfile, _num, _hashtag, _limit = get_args()
    _parsed_data = ((str(_outfile))[:-4])+"_sentiment.csv"

    print("[INFO] Twitter extraction tool\n")

    _auth = ack.Authenticator()
    _auth = _auth.auth_setup(_u_auth)

    _tweets = scr.Scraper()
    _tweets = _tweets.get_tweets(_auth, _outfile, _num, _hashtag)

    print("\n[ANALYSIS] 'Tweet sentiment' data processing")

    _ptweets = [_tweet for _tweet in _tweets if _tweet['sentiment'] == 'positive']
    _ntweets = [_tweet for _tweet in _tweets if _tweet['sentiment'] == 'negative']
    _neutral = len(_tweets) - len(_ntweets) - len(_ptweets)

    print("[POSITIVE | NEGATIVE | NEUTRAL  ]")
    print("[ {:.2f} %".format(100*len(_ptweets)/len(_tweets)),
        "|  {:.2f} %".format(100*len(_ntweets)/len(_tweets)),
        "|  {:.2f} %".format(100*_neutral/len(_tweets)),
        "]")

    _elem = pp.PostProcessor()

    _pos_map = _elem.evaluate_text(_parsed_data, str(_hashtag), "positive")
    _neg_map = _elem.evaluate_text(_parsed_data, str(_hashtag), "negative")
    _nt_map = _elem.evaluate_text(_parsed_data, str(_hashtag), "neutral")

    _pos_list = []
    _neg_list = []
    _nt_list = []

    for _key in _pos_map:
      _pos_list.append(_pos_map[_key])

    for _key in _neg_map:
      _neg_list.append(_neg_map[_key])  

    for _key in _nt_map:
      _nt_list.append(_nt_map[_key])

    _final_pos = dict()
    _final_neg = dict()
    _final_nt = dict()

    for _z in _pos_list:
      for _e in _z:
        _final_pos[_e] = int(_final_pos.get(_e, 0) + 1)

    for _x in _neg_list:
      for _y in _x:
        _final_neg[_y] = int(_final_neg.get(_y, 0) + 1)

    for _w in _nt_list:
      for _t in _w:
        _final_nt[_t] = int(_final_nt.get(_t, 0) + 1)

    _p_file = ((str(_outfile))[:-4]) + "_most_pos.csv"
    _n_file = ((str(_outfile))[:-4]) + "_most_neg.csv"
    _nt_file = ((str(_outfile))[:-4]) + "_most_nt.csv"

    with open(_p_file, 'w') as _csv_file:
      _writer = csv.writer(_csv_file)
      for _key, _value in _final_pos.items():
        if _final_pos[_key] > int(_limit):
          _writer.writerow([_key, _value])

    with open(_n_file, 'w') as _csv_file:
      _writer = csv.writer(_csv_file)
      for _key, _value in _final_neg.items():
        if _final_neg[_key] > int(_limit):
          _writer.writerow([_key, _value])

    with open(_nt_file, 'w') as _csv_file:
      _writer = csv.writer(_csv_file)
      for _key, _value in _final_nt.items():
        if _final_nt[_key] > int(_limit):
          _writer.writerow([_key, _value])

  except KeyboardInterrupt:
    print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
    print("Exit...")
    sys.exit()
