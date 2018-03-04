#!/usr/bin/env python3

import csv
import re
from itertools import chain
import sys
import uuid
from collections import Counter
import argparse
import time
import os.path
import os
import warnings
import multiprocessing
try:
    import matplotlib.cbook
except ImportError:
    print("[ERROR] Unable to import MatPlotLib module! Exit...")
    sys.exit()
try:
    import geocoder
except ImportError:
    print("[ERROR] Unable to import Geocoder module: cant'run! Exit...")
    sys.exit()
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("[ERROR] Unable to import MatPlotLib module! Exit...")
    sys.exit()
try:
    import country_processor as cp
except ImportError:
    print("[ERROR] Unable to import country_processing module! Exit...")
    sys.exit()
try:
    import common_utils as cu
except ImportError:
    print("[ERROR] Unable to import 'common_utils' module! Exit...")
    sys.exit()

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


class CountryPlotter():

    def __init__(self):
        self._status = ""

    def plot_graph(self, fname, limit, num, bhash, gfile, sgraph):
        self._title = "Countries Analysis for " + str(num) + \
            " tweets including '" + bhash + "' "
        self._title += "hashtag \n(frequency over " + str(limit)
        self._title += ") "

        self.outfile = open(fname, "r")
        self._rfile = csv.reader(self.outfile)

        self._countries = list()
        self._freq = list()

        for self._row in self._rfile:
            if self._row[0] != '':
                if int(self._row[1]) > limit:
                    try:
                        self._countries.append(self._row[0])
                        self._freq.append(int(self._row[1]))
                    except TypeError:
                        pass

        plt.title(self._title)
        plt.pie(
            self._freq,
            labels=self._countries,
            autopct='%1.0f%%',
            pctdistance=1.1,
            labeldistance=1.2)
        plt.axes().set_aspect('equal')
        plt.savefig(gfile)

        if sgraph in ["y", "yes"]:
            plt.show()


def get_args():
    parser = argparse.ArgumentParser(
        description='Script plot countries pie graph from tweets dataset')
    parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV input filename',
        required=True)
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
    parser.add_argument(
        '-l',
        '--limitf',
        type=int,
        help='Limit hasht. frequency for plotter',
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
    fout = ((str(ifile))[:-4]) + "_countries.csv"

    return ifile, num, hashtag, limit, sgraph, fout


if __name__ == "__main__":

    t_data = list()
    addresses = list()

    ifile, num, hashtag, limit, sgraph, outfile = get_args()
    print("[INFO] Tweet's Countries Analyzing Tool\n")

    gfile = ((str(ifile))[:-4]) + "_countries.png"

    if os.path.exists(ifile) is False:
        print("[ERROR] Input file doesn't exists! Exit...")
        sys.exit()

    t_data_c = cp.CountryProcessor()
    plotter = CountryPlotter()

    if os.name != "nt":
        f_path = "./" + outfile
    else:
        f_path = outfile

    if os.path.exists(f_path) is True:
        plotter.plot_graph(
            outfile,
            limit,
            num,
            hashtag,
            gfile,
            sgraph)
    else:
        print("[NOTICE] Parsing countries data...")
        print("[*] Please, wait...")
        print("[NOTICE] Using Komoot Geocoder Database")

        t_data = t_data_c.parse_countries(ifile)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        try:
            addresses = pool.map(cp.geocoder_worker, t_data)
            pool.close()

            res = dict(Counter(addresses))
            f_writer = cu.FastWriter()
            f_writer.fast_writer(
                outfile,
                res
            )

            plotter.plot_graph(
                outfile,
                limit,
                num,
                hashtag,
                gfile,
                sgraph)

        except KeyboardInterrupt:
            pool.terminate()
            print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
            print("Exit...")
            sys.exit()
