import csv
import os
import sys


class FastWriter:

    def __init__(self):
        self._status = ""
        self._csv_file = ""
        self._writer = ""
        self._db_file = ""

    def fast_writer(self, f_name, text_dict):
        try:
            # Windows
            if os.name == "nt":
                with open(f_name, 'w', newline='') as self._csv_file:
                    self._writer = csv.writer(self._csv_file)
                    for self._key, self._value in text_dict.items():
                        self._writer.writerow([self._key, self._value])

            # Unix/Linux
            else:
                with open(f_name, 'w') as self._csv_file:
                    self._writer = csv.writer(self._csv_file)
                    for self._key, self._value in text_dict.items():
                        self._writer.writerow([self._key, self._value])

        except Exception as e:
            print("[ERROR] Unable to write file on disk. Exit...")
            print("\n[Details]: ", e)
            sys.exit()

    def backup_db(self, elem, fout):
        try:
            if os.name == "nt":
                with open(fout, 'a', newline='') as self._db_file:
                    self._writer = csv.writer(
                        self._db_file
                    )
                    self._writer.writerow(elem.split(","))
            else:
                with open(fout, 'a') as self._db_file:
                    self._writer = csv.writer(
                        self._db_file
                    )
                    self._writer.writerow(elem.split(","))

        except Exception as e:
            print("[ERROR] Unable to write file on disk. Exit...")
            print("\n[Details]: ", e)
            sys.exit()
