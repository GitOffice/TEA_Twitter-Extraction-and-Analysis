#!/usr/bin/env python3

import sys
import argparse
import os

class TimelineFilter():

    def __init__(self):
        self._status = ""

    def filter_lines(self, filename, keywords):
        self._keywords = keywords.split(",")
        self._filtered_file = filename[:-4] + "_filtered.csv"

        try:
            with open(filename) as self._old_file, open(self._filtered_file, 'w') as self._new_file:
                for self._line in self._old_file:
                    if any(self._kword in self._line for self._kword in self._keywords):
                        self._new_file.write(self._line)
            if os.path.exists(self._filtered_file): 
                print("[*] Filtered file '", self._filtered_file, "' created.")        
        except Exception as err:
            print("[ERROR]: ", err)
            sys.exit()

def get_args():
    parser = argparse.ArgumentParser(
        description='Read a Twitter user timeline and filter arguments.')
    parser.add_argument(
        '-i',
        '--ifile',
        type=str,
        help='CSV input filename',
        required=False,
        default="user_timeline.csv")
    parser.add_argument(
        '-k',
        '--keywords',
        type=str,
        help='keywords for filtering',
        required=True)

    args = parser.parse_args()
    ifile = args.ifile
    keywords = args.keywords

    return ifile, keywords

if __name__ == "__main__":

    try:

        ifile, keywords = get_args()

        elem = TimelineFilter()
        elem.filter_lines(ifile, keywords) 

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
        sys.exit()