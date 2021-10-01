#!/usr/bin/env python3

import json
import csv

from io import StringIO


def from_json(data):
    return json.loads(data)


def from_csv(data, delimiter):
    fs_string = StringIO(data)
    reader = csv.DictReader(StringIO(data), delimiter=delimiter)
    output_data = [row for row in reader]
    return output_data


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
