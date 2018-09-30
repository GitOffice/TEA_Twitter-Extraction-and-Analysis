import csv
import os
import re
import sys
import pandas as pd
try:
    import geocoder
except ImportError:
    print("[ERROR] Unable to import Geocoder module: cant'run! Exit...")
    sys.exit()
try:
    import common_utils as cu
except ImportError:
    print("[ERROR] Unable to import 'common_utils' module! Exit...")
    sys.exit()


class CountryProcessor:

    def __init__(self):
        self._status = ""
        self._myFile = ""
        self._myList = ""
        self._reader = ""

    @staticmethod
    def clean_name(tweet):
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


db = cu.FastWriter()

if os.path.exists("./geo_db.db") is True:
    status = True
    df = pd.read_csv("geo_db.db", names=["loc", "country"], comment='#')
else:
    status = False


def geocoder_worker(location):
    try:
        # if cache exists
        if status is True:
            res = df[df["loc"].str.match(location)]['country']

            if len(res) != 0:
                print("[Cached]", res.iloc[0])
                return str(res.iloc[0])
            else:
                country_elem = geocoder.komoot(location)
                country_name = country_elem.country

            if country_name is None:
                return
            else:
                print(country_name)
                temp = location + "," + country_name
                db.backup_db(temp, "geo_db.db")
                return country_name

        # if cache doesn't exists
        else:
            country_elem = geocoder.komoot(location)
            country_name = country_elem.country

        if country_name is None:
            return
        else:
            print(country_name)
            temp = location + "," + country_name
            db.backup_db(temp, "geo_db.db")
            return country_name

    except KeyboardInterrupt:
        return
