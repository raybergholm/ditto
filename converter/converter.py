#!/usr/bin/env python3

import json

from lazeesnake.csv_handler import from_csv_file, to_csv_file, csv_to_json
from lazeesnake.json_handler import from_json_file, to_json_file, json_to_csv

def check_filetype(filepath):
    JSON_FILE_FORMAT = "json"
    CSV_FILE_FORMAT = "csv"

    if filepath.endswith(".%s" % JSON_FILE_FORMAT):
        return JSON_FILE_FORMAT
    elif filepath.endswith(".%s" % CSV_FILE_FORMAT):
        return CSV_FILE_FORMAT
    else:
        return ""

def convert_json_to_csv(input_data, delimiter=";", newline="\n", fieldnames=None):
    data = from_json_file(input_data, fieldnames)
    csv_data = json_to_csv(data)

def convert_csv_to_json(input_data, delimiter=";", newline="\n", fieldnames=None):
    (header, data) = from_csv_file(input_data, delimiter, newline)
    json_data = csv_to_json(header, data)
    return json.dumps(json_data)