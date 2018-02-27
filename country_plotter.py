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
import common_utils as cu
import multiprocessing
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

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


class CountryPlotter():

    def __init__(self):
        self._status = ""

    def plot_graph(self, fname, limit, num, bhash, gfile, sgraph):
        self._base_hash = bhash
        self._t_data_file = fname
        self._limit = int(limit)
        self._num = str(num)
        self._gfile = gfile

        self._title = "Countries Analysis for " + self._num + \
            " tweets including '" + self._base_hash + "' "
        self._title += "hashtag \n(frequency over " + str(self._limit)
        self._title += ") "

        self._outfile = open(self._t_data_file, "r")
        self._rfile = csv.reader(self._outfile)

        self._countries = []
        self._freq = []

        for self._row in self._rfile:
            if self._row[0] != '':
                if int(self._row[1]) > self._limit:
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
        plt.savefig(self._gfile)
        
        if sgraph in ["y", "yes"]:
            plt.show()


def get_args():
    _parser = argparse.ArgumentParser(
        description='Script plot countries pie graph from tweets dataset')
    _parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV input filename',
        required=True)
    _parser.add_argument(
        '-n',
        '--tnum',
        type=int,
        help='Number of tweets to get',
        required=True,
        default=500)
    _parser.add_argument(
        '-t',
        '--hashtag',
        type=str,
        help='Hashtag to search',
        required=True)
    _parser.add_argument(
        '-l',
        '--limitf',
        type=int,
        help='Limit hasht. frequency for plotter',
        required=False,
        default=50)
    _parser.add_argument(
    '-g',
    '--graph',
    type=str,
    help='Choose if open graph in window (y/n)',
    required=False,
    default="y")

    _args = _parser.parse_args()
    _ifile = _args.ifile
    _num = int(_args.tnum)
    _hashtag = _args.hashtag
    _limit = int(_args.limitf)
    _sgraph = (_args.graph).lower()
    _fout = ((str(_ifile))[:-4]) + "_countries.csv"

    return _ifile, _num, _hashtag, _limit, _sgraph, _fout


if __name__ == "__main__":

    _t_data = []
    _addresses = []

    _ifile, _num, _hashtag, _limit, _sgraph, _outfile = get_args()
    print("[INFO] Tweet's Countries Analyzing Tool\n")

    _gfile = ((str(_ifile))[:-4]) + "_countries.png"

    if os.path.exists(_ifile) is False:
        print("[ERROR] Input file doesn't exists! Exit...")
        sys.exit()

    _t_datac = cp.CountryProcessor()
    _plotter = CountryPlotter()

    if os.name != "nt":
        _f_path = "./" + _outfile
    else:
        _f_path = _outfile

    if os.path.exists(_f_path) is True:
        _plotter.plot_graph(_outfile, _limit, _num, _hashtag, _gfile, _sgraph)
    else:
        print("[NOTICE] Parsing countries data...")
        print("[*] Please, wait...")
        print("[NOTICE] Using Komoot Geocoder Database")

        _t_data = _t_datac.parse_countries(_ifile)
        _pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        
        try:
            _addresses = _pool.map(cp.geocoder_worker, _t_data)
            _pool.close()

            _res = dict(Counter(_addresses))
            _f_writer = cu.FastWriter()
            _f_writer.fast_writer(
                _outfile,
                _res,
                str(os.name)
                )

            _plotter.plot_graph(_outfile, _limit, _num, _hashtag, _gfile, _sgraph)

        except KeyboardInterrupt:
            _pool.terminate()
            print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
            print("Exit...")
            sys.exit()