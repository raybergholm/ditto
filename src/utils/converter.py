#!/usr/bin/env python3

import json
import csv


def check_filetype(filepath):
    JSON_FILE_FORMAT = "json"
    CSV_FILE_FORMAT = "csv"

    if filepath.endswith(".{0}".format(JSON_FILE_FORMAT)):
        return JSON_FILE_FORMAT
    elif filepath.endswith(".{0}".format(CSV_FILE_FORMAT)):
        return CSV_FILE_FORMAT
    else:
        return ""


# supply a field list to filter the JSON data, otherwise it will return the whole body as-is
def from_json_file(filepath, filter=None, forced_json_fields=None):
    data = None
    with open(filepath, newline="") as file_stream:
        data = json.loads(file_stream.read())
    return data


def from_csv_file(filepath, delimiter=";", quotechar="\"", has_header=True):
    header = None
    data = []
    with open(filepath, mode="r", newline="") as file_stream:
        reader = csv.reader(
            file_stream, delimiter=delimiter, quotechar=quotechar)
        if has_header:
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                else:
                    data.append(row)
        else:
            data = [row for row in reader]

    output = []
    for line in data:
        output.append(
            {header[index]: field for index, field in enumerate(line)})
    return output

def to_json(data):
    return json.dumps(data)

def to_csv(data, delimiter, newline):
    header = [key for key in data[0].keys()]
    output_data = []
    
    output_data.append("{0}{1}".format(delimiter.join(header), newline))
    for row in data:
        # This kind of looks superfluous when filtering happens before this step, but this is actually more about enforcing a set field order if you get objects with different key ordering
        entry = [str(row[field]) if field in row else "" for field in header]
        output_data.append("{0}{1}".format(delimiter.join(entry), newline))
    return output_data
