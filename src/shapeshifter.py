#!/usr/bin/env python3

import argparse
import json

from utils.file import read_file
from utils.converter import from_json, from_csv, to_json, to_csv
from utils.filter import include_fields, exclude_fields, filter_fields, filter_by_value

class Shapeshifter:
    DEFAULT_HEADERS = []
    DEFAULT_CSV_DELIMITER = ";"
    DEFAULT_CSV_QUOTECHAR = "\""

    SUPPORTED_DATA_TYPES = [
        "json",
        "csv"
    ]

    def __init__(self, config={}, delimiter=DEFAULT_CSV_DELIMITER, quotechar=DEFAULT_CSV_QUOTECHAR, headers=DEFAULT_HEADERS, paging=None):
        self.source = None
        self.workarea = None

        self.headers = Shapeshifter.DEFAULT_HEADERS
        self.delimiter = Shapeshifter.DEFAULT_CSV_DELIMITER
        self.quotechar = Shapeshifter.DEFAULT_CSV_QUOTECHAR

        self.paging = None

        if headers != Shapeshifter.DEFAULT_HEADERS:
            self.headers = json.loads(headers)
        elif "headers" in config:
            self.headers = config["headers"]

        if delimiter != Shapeshifter.DEFAULT_CSV_DELIMITER:
            self.delimiter = delimiter
        elif "delimiter" in config:
            self.delimiter = config["delimiter"]

        if quotechar != Shapeshifter.DEFAULT_CSV_QUOTECHAR:
            self.quotechar = quotechar
        elif "quotechar" in config:
            self.quotechar = config["quotechar"]

        if paging and "iterator" in paging and "min" in paging and "max" in paging:
            self.paging = paging

    def __fetch(self, data_source_path):
        if data_source_path.startswith("http://") or data_source_path.startswith("https://"):
            import requests

            if not self.paging:
                print("Fetching from URL {0}".format(data_source_path))
                response = requests.get(data_source_path, headers=self.headers)

                if response.ok:
                    self.source = response.text
                else:
                    print("Failed to fetch from {0}".format(data_source_path))
                    print("Error response: {0} {1}".format(
                        response.status_code, response.text))
                    raise Exception("Failed to fetch from {0}".format(data_source_path))
            else:
                self.source = []
                for page_number in range(self.paging["min"], self.paging["max"] + 1):
                    paging_path = "{0}&{1}={2}".format(data_source_path, self.paging["iterator"], page_number)

                    print("Fetching from URL {0}".format(paging_path))
                    response = requests.get(paging_path, headers=self.headers)
                    if response.ok:
                        self.source.append(response.text)
                    else:
                        print("Failed to fetch from {0}".format(data_source_path))
                        print("Error response: {0} {1}".format(
                            response.status_code, response.text))
                        raise Exception("Failed to fetch from {0}".format(data_source_path))
                

        else:
            self.source = read_file(data_source_path)

    def get_source(self):
        return self.source

    def from_csv(self, data_source_path):
        self.__fetch(data_source_path)
        self.workarea = from_csv(self.source, self.delimiter, self.quotechar)
        return self

    def from_json(self, data_source_path):
        self.__fetch(data_source_path)
        if not self.paging:
            self.workarea = from_json(self.source)
        else:
            accumulator = []
            for entry in self.source:
                accumulator = accumulator + from_json(entry)
            self.workarea = accumulator
        return self

    def to_csv(self):
        return to_csv(self.workarea, self.delimiter, self.quotechar)

    def to_json(self):
        return to_json(self.workarea)

    def include(self, *include_list):
        self.workarea = include_fields(self.workarea, include_list)
        return self

    def exclude(self, *exclude_list):
        self.workarea = exclude_fields(self.workarea, exclude_list)
        return self

    def only(self, *filter_list):
        self.workarea = filter_fields(self.workarea, filter_list)
        return self
    
    def filter(self, field, operator, value):
        self.workarea = filter_by_value(self.workarea, field, operator, value)
        return self
