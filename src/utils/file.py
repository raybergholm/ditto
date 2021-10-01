#!/usr/bin/env python3

def check_filetype(filepath):
    JSON_FILE_FORMAT = "json"
    CSV_FILE_FORMAT = "csv"

    if filepath.endswith(".{0}".format(JSON_FILE_FORMAT)):
        return JSON_FILE_FORMAT
    elif filepath.endswith(".{0}".format(CSV_FILE_FORMAT)):
        return CSV_FILE_FORMAT
    else:
        return ""


def read_file(filepath):
    with open(filepath, "r") as file_stream:
        data = file_stream.read()
    return data

def save_file(filepath, data):
    with open(filepath, "w+") as file_stream:
        for entry in data:
            file_stream.write(entry)
