import csv
import os
import sys


class FastWriter():

    def __init__(self):
        self._status = ""

    def fast_writer(self, f_name, text_dict, os_name):
        self._fout = f_name
        self._res = text_dict

        try:
            # Windows
            if os_name == "nt":
                with open(self._fout, 'w', newline='') as self._csv_file:
                    self._writer = csv.writer(self._csv_file)
                    for self._key, self._value in self._res.items():
                        self._writer.writerow([self._key, self._value])

            # Unix/Linux
            else:
                with open(self._fout, 'w') as self._csv_file:
                    self._writer = csv.writer(self._csv_file)
                    for self._key, self._value in self._res.items():
                        self._writer.writerow([self._key, self._value])

        except BaseException:
            print("[ERROR] Unable to write file on disk. Exit...")
            sys.exit()


    def backup_db(self, elem, fout):
        self._fout = fout
        self._mylist = elem
        self._mylist = self._mylist.split(",")
        try:
            if os.name == "nt":
                with open(self._fout, 'a', newline='') as self._db_file:
                    self._writer = csv.writer(
                        self._db_file 
                        )
                    self._writer.writerow(self._mylist)
            else:
                with open(self._fout, 'a') as self._db_file:
                    self._writer = csv.writer(
                        self._db_file 
                        )
                    self._writer.writerow(self._mylist)

        except BaseException:
            print("[ERROR] Unable to write file on disk. Exit...")
            sys.exit()
