#!/usr/bin/env python3

import csv
import sys
import argparse
import os.path
import os
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("[ERROR] Unable to import MatPlotLib module! Exit...")
    sys.exit()
try:
    import pandas as pd
except ImportError:
    print("[ERROR] Unable to import Pandas module! Exit...")
    sys.exit()

class Plotter(object):

    def __init__(self):
        self._status = ""

    def show_data(self):
        plt.show()

    def plot_data(self, data_file, sentiment, base_hash, limit, num, gfile):
        self._data_file = data_file
        self._sentiment = sentiment
        self._base_hash = base_hash
        self._limit = limit
        self._num = num
        self._gfile = gfile

        try:
            self._data = pd.read_csv(self._data_file, sep=',',header=None, index_col =0)
            self._title = "Base hashtag: " + self._base_hash
            self._title += "\nMost used '" +self._sentiment + "' #hashtags (written over " + self._limit
            self._title += " times) in " + self._num + " tweets"

            #Re-read the file
            self._data = pd.read_csv(self._data_file, sep=',',header=None, index_col =0)

            if self._sentiment == "positive":
                self._color = "blue"
            if self._sentiment == "negative":
                self._color = "red"
            if self._sentiment == "neutral":
                self._color = "grey"

            self._data.plot(kind='bar', legend=None, color=self._color)
            plt.ylabel('Frequency')
            plt.xlabel('Hashtags')
            plt.title(self._title)
            plt.savefig(self._gfile)

        except:
            return

def get_args():
    _parser = argparse.ArgumentParser(description='Script plot histograms based on analyzed tweets')
    _parser.add_argument('-i', '--ifile', type=str, help='CSV base name filename', required=False, default="tweet_search.csv")
    _parser.add_argument('-n', '--tnum', type=int, help='Number of tweets analyzed', required=True)
    _parser.add_argument('-t', '--hashtag', type=str, help='Base hashtag', required=True)
    _parser.add_argument('-l', '--limitf', type=int, help='Limit hasht. frequency for plotter', required=False, default=50)

    _args = _parser.parse_args()
    _ifile = _args.ifile
    _num = int(_args.tnum)
    _hashtag = _args.hashtag
    _limit = int(_args.limitf)

    return _ifile, _num, _hashtag, _limit


if __name__ == "__main__":

    try:
        _ifile, _num, _hashtag, _limit = get_args()
        print("[INFO] Tweet's histograms Plot tool\n")

        if os.path.exists(_ifile) is False:
            print("[ERROR] Input file doesn't exists! Exit...")
            sys.exit()

        _pos_graph = Plotter()
        _neg_graph = Plotter()
        _nt_graph = Plotter()

        _p_file = ((str(_ifile))[:-4]) + "_most_pos.csv"
        _n_file = ((str(_ifile))[:-4]) + "_most_neg.csv"
        _nt_file = ((str(_ifile))[:-4]) + "_most_nt.csv"

        _g_p_file = ((str(_ifile))[:-4]) + "_pos_trend.png"
        _g_n_file = ((str(_ifile))[:-4]) + "_neg_trend.png"
        _g_nt_file = ((str(_ifile))[:-4]) + "_nt_trend.png"

        _pos_graph.plot_data(_p_file, "positive", str(_hashtag), str(_limit), str(_num), _g_p_file)
        _neg_graph.plot_data(_n_file, "negative", str(_hashtag), str(_limit), str(_num), _g_n_file)
        _nt_graph.plot_data(_nt_file, "neutral", str(_hashtag), str(_limit), str(_num), _g_nt_file)

        _pos_graph.show_data()
        _neg_graph.show_data()
        _nt_graph.show_data()

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
