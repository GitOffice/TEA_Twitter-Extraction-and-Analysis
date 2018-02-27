import multiprocessing
import csv
import common_utils as cu
import os
import re
from collections import Counter
import sys
try:
    import geocoder
except ImportError:
    print("[ERROR] Unable to import Geocoder module: cant'run! Exit...")
    sys.exit()


class CountryProcessor():

    def __init__(self):
        self._status = ""

    def clean_name(self, tweet):
        return ' '.join(
            re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                " ",
                tweet).split())

    def parse_countries(self, fname):
        if os.name == "nt":
            with open(fname, 'r', encoding='utf-8') as self._myFile:
                self._reader = csv.reader(self._myFile, delimiter=',')
                next(self._reader, None)
                self._myList = list(
                    self.clean_name(
                        self._i[1]) for self._i in self._reader)
        else:
            with open(fname, 'r') as self._myFile:
                self._reader = csv.reader(self._myFile, delimiter=',')
                next(self._reader, None)
                self._myList = list(
                    self.clean_name(
                        self._i[1]) for self._i in self._reader)

        return self._myList


def geocoder_worker(location):
    try:
        _country_elem = geocoder.komoot(location)
        _country_name = _country_elem.country
        if _country_name is None:
            return
        else:
            print(_country_name)
            return _country_name
    except KeyboardInterrupt:
        return
