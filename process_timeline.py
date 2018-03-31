#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import sys
import csv
import argparse
import collections

class TimelineProcessor():

    def __init__(self):
        dataset = dict()
        data_elem = list()

    def dict_writer(self, f_name, data_dict):
        try:
            # Windows
            if os.name == "nt":
                with open(f_name, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data_dict.items():
                        writer.writerow([key, value])
            # Unix/Linux
            else:
                with open(f_name, 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data_dict.items():
                        writer.writerow([key, value[0], value[1]])
        except Exception as err:
            print(err)
            sys.exit()

    def build_dataset(self, f_name):
        elem = pd.read_csv(
            f_name, 
            usecols=[0,3],
            names=["created_at", "polarity"]
            )

        g = elem.groupby('created_at')

        for _, g in elem.groupby('created_at'):
            data_elem = []
            group_date = str(g['created_at'].values[0])
            mean = g.mean()
            mean = str(mean.values[0].round(4))
            pol_max = (g['polarity'].max().round(4))
            pol_min = (g['polarity'].min().round(4))
            max_err = str(((pol_max - pol_min)/2).round(4))
            data_elem.append(mean)
            data_elem.append(max_err)
            dataset[group_date] = data_elem

            ordered = collections.OrderedDict(sorted(dataset.items(), key=lambda t: t[0]))

        return ordered

def get_args():
    parser = argparse.ArgumentParser(
        description='Process filtered timeline to get avg sentiment per day.')
    parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV input filename',
        required=True
        )
    parser.add_argument(
        '-o',
        '--ofile',
        type=str,
        help='Processed CSV output filename',
        required=True
        )

    args = parser.parse_args()
    ifile = args.ifile
    ofile = args.ofile
    return ifile, ofile

if __name__ == "__main__":

    try:
        dataset = dict()
        ifile, ofile = get_args()
        elem = TimelineProcessor()
        dataset = elem.build_dataset(ifile)
        elem.dict_writer(ofile, dataset) 

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
        sys.exit()
