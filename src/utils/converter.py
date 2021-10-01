#!/usr/bin/env python3

import json
import csv

from io import StringIO


def from_json(data):
    return json.loads(data)


def from_csv(data, delimiter, quotechar):
    fs_string = StringIO(data)
    reader = csv.DictReader(StringIO(data), delimiter=delimiter, quotechar=quotechar)
    output_data = [row for row in reader]
    return output_data


def to_json(data):
    return json.dumps(data)


def to_csv_old(data, delimiter, newline):
    header = [key for key in data[0].keys()]
    output_data = []

    output_data.append("{0}{1}".format(delimiter.join(header), newline))
    for row in data:
        # This kind of looks superfluous when filtering happens before this step, but this is actually more about enforcing a set field order if you get objects with different key ordering
        entry = [str(row[field]) if field in row else "" for field in header]
        output_data.append("{0}{1}".format(delimiter.join(entry), newline))
    return output_data


def to_csv(data, delimiter, quotechar):
    fields = [key for key in data[0].keys()]

    file_stream = StringIO()
    writer = csv.DictWriter(file_stream, fieldnames=fields, delimiter=delimiter, quotechar=quotechar, extrasaction="ignore")

    writer.writeheader()
    writer.writerows(data)

    return file_stream.getvalue()
