#!/usr/bin/env python3

import json

from csv_handler import from_csv_file to_csv_file
from json_handler import from_json_file, to_json_file

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
    return to_csv_file(data, delimiter, newline)

def convert_csv_to_json(input_data, delimiter=";", newline="\n", fieldnames=None):
    data = from_csv_file(input_data, delimiter, newline)
    return to_json_file(data, field_names)