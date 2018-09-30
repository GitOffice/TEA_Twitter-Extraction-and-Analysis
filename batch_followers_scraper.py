#!/usr/bin/env python3
import sys
import csv
import random
import argparse
import subprocess


class BatchScraper:

    def __init__(self):
        self._status = ""
        self._users_file = ""
        self._users_list = ""
        self._csvfile = ""
        self._ch_row = ""
        self._fout = ""
        self._cmd = ""
        self._users = list()
        self._cnt = 0

    def batch_scraper(self, auth, fname, users_num):
        with open(fname, 'r') as self._csvfile:
            self._users_file = csv.reader(self._csvfile, delimiter=',')
            next(self._users_file, None)
            self._users_list = list(self._users_file)

            while self._cnt < users_num:
                self._ch_row = random.choice(list(self._users_list))
                self._users.append(self._ch_row[0])
                self._cnt += 1

            print(self._users)

        for self._elem in self._users:
            self._fout = self._elem + "_timeline.csv"
            self._cmd = "python3 get_timeline.py -a " + auth + " -u '" + self._elem + "'"
            self._cmd += " -o " + self._fout
            subprocess.Popen(self._cmd, shell=True)


def get_args():
    parser = argparse.ArgumentParser(
        description='Script gets more accounts timeline and filters its tweets using def. keywords')
    parser.add_argument(
        '-a',
        '--auth',
        type=str,
        help='User auth. file',
        required=True)
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        help='User list filenames',
        required=True)
    parser.add_argument(
        '-n',
        '--num',
        type=int,
        help='Number of users to process',
        required=False,
        default=10)

    args = parser.parse_args()

    return args.auth, args.user, args.num


if __name__ == "__main__":

    try:

        auth, cuser, num = get_args()
        sc = BatchScraper()
        sc.batch_scraper(auth, cuser, num)

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
        sys.exit()
