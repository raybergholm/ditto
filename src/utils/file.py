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


def read_file(filepath, line_delimiter="\n", do_for_each_line=None, do_after_file_read=None):
    with open(filepath, "r") as file_stream:
        data = file_stream.read()
        if line_delimiter != None:
            data = data.split(line_delimiter)
            if do_for_each_line and callable(do_for_each_line):
                data = [do_for_each_line(line) for line in data]

    if do_after_file_read and callable(do_after_file_read):
        return do_after_file_read(data)
    else:
        return data


def save_file(filepath, data):
    with open(filepath, "w+") as file_stream:
        for entry in data:
            file_stream.write(entry)
