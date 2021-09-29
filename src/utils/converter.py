#!/usr/bin/env python3

import json
import csv


def check_filetype(filepath):
    JSON_FILE_FORMAT = "json"
    CSV_FILE_FORMAT = "csv"

    if filepath.endswith(".%s" % JSON_FILE_FORMAT):
        return JSON_FILE_FORMAT
    elif filepath.endswith(".%s" % CSV_FILE_FORMAT):
        return CSV_FILE_FORMAT
    else:
        return ""


# supply a field list to filter the JSON data, otherwise it will return the whole body as-is
def from_json_file(filepath, filter=None, forced_json_fields=None):
    data = None
    with open(filepath, newline="") as file_stream:
        data = json.loads(file_stream.read())
    return data


def from_csv_file(filepath, delimiter=";", quotechar="\"", has_header=True, return_dict=False):
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

    if return_dict:
        output = []
        for line in data:
            output.append(
                {header[index]: field for index, field in enumerate(line)})
        return output
    else:
        return (header, data)


def json_to_csv(data, delimiter=";", expand=False):
    # if no field_list is supplied, it will build it from the first item in the list. Doing it this way means that the key order will vary!
    header = [key for key in data[0].keys()]

    csv_data = []
    csv_data.append("%s\n" % delimiter.join(header))
    for line in data:
        entry = [str(line[field]) if field in line else "" for field in header]
        csv_data.append("%s\n" % delimiter.join(entry))
    return csv_data


def csv_to_json(header, data):
    json_data = []
    for line in data:
        entry = {field: line[index] for index, field in enumerate(header)}
        json_data.append(entry)
    return json.dumps(json_data)
