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
        try:
            self._data = pd.read_csv(
                data_file,
                sep=',',
                header=None,
                index_col=0,
                usecols=[
                    0,
                    1])
            self._data = self._data[self._data[1] > int(limit)]
            self._title = "Base hashtag: " + base_hash
            self._title += "\nMost used '" + sentiment + \
                "' #hashtags (written over " + limit
            self._title += " times) in " + num + " tweets"

            if sentiment == "positive":
                self._color = "blue"
            if sentiment == "negative":
                self._color = "red"
            if sentiment == "neutral":
                self._color = "grey"

            self._data.plot(kind='bar', legend=None, color=self._color)
            plt.ylabel('Frequency')
            plt.xlabel('Hashtags')
            plt.title(self._title)
            plt.savefig(gfile)

        except BaseException:
            return


def get_args():
    parser = argparse.ArgumentParser(
        description='Script plot histograms based on analyzed tweets')
    parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV base name filename',
        required=False,
        default="tweet_search.csv")
    parser.add_argument(
        '-n',
        '--tnum',
        type=int,
        help='Number of tweets analyzed',
        required=True)
    parser.add_argument(
        '-t',
        '--hashtag',
        type=str,
        help='Base hashtag',
        required=True)
    parser.add_argument(
        '-l',
        '--limitf',
        type=int,
        help='Limit hashtag frequency for plotter',
        required=False,
        default=50)
    parser.add_argument(
        '-g',
        '--graph',
        type=str,
        help='Choose if open graph in window (y/n)',
        required=False,
        default="y")

    args = parser.parse_args()
    ifile = args.ifile
    num = int(args.tnum)
    hashtag = args.hashtag
    limit = int(args.limitf)
    sgraph = (args.graph).lower()

    return ifile, num, hashtag, limit, sgraph


if __name__ == "__main__":

    try:
        ifile, num, hashtag, limit, sgraph = get_args()
        print("[INFO] Tweet's histograms Plot tool\n")

        if os.path.exists(ifile) is False:
            print("[ERROR] Input file doesn't exists! Exit...")
            sys.exit()

        pos_graph = Plotter()
        neg_graph = Plotter()
        nt_graph = Plotter()

        p_file = ((str(ifile))[:-4]) + "_most_pos.csv"
        n_file = ((str(ifile))[:-4]) + "_most_neg.csv"
        nt_file = ((str(ifile))[:-4]) + "_most_nt.csv"

        gp_file = ((str(ifile))[:-4]) + "_pos_trend.png"
        gn_file = ((str(ifile))[:-4]) + "_neg_trend.png"
        gnt_file = ((str(ifile))[:-4]) + "_nt_trend.png"

        pos_graph.plot_data(
            p_file,
            "positive",
            str(hashtag),
            str(limit),
            str(num),
            gp_file)
        neg_graph.plot_data(
            n_file,
            "negative",
            str(hashtag),
            str(limit),
            str(num),
            gn_file)
        nt_graph.plot_data(
            nt_file,
            "neutral",
            str(hashtag),
            str(limit),
            str(num),
            gnt_file)

        if sgraph in ["y", "yes"]:
            pos_graph.show_data()
            neg_graph.show_data()
            nt_graph.show_data()

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
