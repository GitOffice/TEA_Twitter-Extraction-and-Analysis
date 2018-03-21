#!/usr/bin/env python3

import csv
import sys
from datetime import datetime
import os
import argparse
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("[ERROR] Unable to import MatPlotLib module! Exit...")
    sys.exit()
try:
    import pandas as pd
except ImportError:
    print("[ERROR] Unable to import Pandas module! Exit...")
    sys.exit

class PolarityPlotter():

    def __init__(self):
        self._status = ""

    def show_data(self):
        plt.show()

    def plot_data(self, fname, account, keywords, gfile, start, end):
        self._x = list()
        self._y = list()
        
        self._title = str(account) + " polarity graph regarding: "
        self._title += str(keywords)
        self._title += "\nbetween " + start + " and " + end
        plt.title(self._title)

        self._start = datetime.strptime(start, "%Y-%m-%d").date()
        self._end = datetime.strptime(end, "%Y-%m-%d").date()

        try:
            with open(fname, 'r') as self._csvfile:
                self._plots = csv.reader(self._csvfile, delimiter=',')
                next(self._plots, None)
                
                for self._row in self._plots:
                    self._curr_date = datetime.strptime((self._row[0])[0:10], 
                        "%Y-%m-%d").date() 
                    self._curr_pol = float(self._row[1])

                    if self._curr_date >= self._start and self._curr_date <= self._end:
                            self._x.append((self._curr_date))
                            self._y.append(self._curr_pol)
            
            plt.plot(self._x, self._y)
            plt.axhline(0, color='grey', lw=1, linestyle="dashed")
            plt.set_xlim(xmin=self._start, xmax=self._end)
            plt.xlabel('x')
            plt.xticks(rotation=90)
            plt.ylabel('y')
            plt.savefig(gfile, dpi=200)
        
        except Exception:
            return

def get_args():
    parser = argparse.ArgumentParser(
        description='Script plot account polarity graph regarding keywords')
    parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV base name filename',
        required=False,
        default="user_timeline.csv")
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        help='Account followed',
        required=True)
    parser.add_argument(
        '-k',
        '--keywords',
        type=str,
        help='search keywords',
        required=False,
        default="'keywords'")
    parser.add_argument(
        '-g',
        '--graph',
        type=str,
        help='Choose if open graph in window (y/n)',
        required=False,
        default="y")
    parser.add_argument(
        '-s',
        '--start',
        type=str,
        help='Starting date for plot',
        required=False,
        default="2015-01-01")
    parser.add_argument(
        '-e',
        '--end',
        type=str,
        help='Ending date for plot',
        required=False,
        default="2020-01-01")

    args = parser.parse_args()
    ifile = args.ifile
    cuser = args.user
    ckeywords = args.keywords
    sgraph = (args.graph).lower()
    start = args.start
    end = args.end

    return ifile, cuser, ckeywords, sgraph, start, end

if __name__ == "__main__":

    try:
        ifile, cuser, ckeywords, sgraph, start, end = get_args()
        print("[INFO] Tweet's Polarity Plot tool\n")

        if os.path.exists(ifile) is False:
            print("[ERROR] Input file doesn't exists! Exit...")
            sys.exit()

        pol_graph = PolarityPlotter()

        pol_file = ((str(ifile))[:-4]) + "_polarity.png"

        pol_graph.plot_data(
            str(ifile),
            str(cuser),
            str(ckeywords),
            str(pol_file),
            str(start),
            str(end))

        if sgraph in ["y", "yes"]:
            pol_graph.show_data()

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
