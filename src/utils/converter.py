#!/usr/bin/env python3

import json
import csv

from io import StringIO


def from_json(data):
    return json.loads(data)


def from_csv(data, delimiter, quotechar):
    fs_string = StringIO(data)
    reader = csv.DictReader(
        StringIO(data), delimiter=delimiter, quotechar=quotechar)
    output_data = [row for row in reader]
    return output_data


def to_json(data):
    return json.dumps(data)


def to_csv(data, delimiter, quotechar):
    fields = [key for key in data[0].keys()]

    file_stream = StringIO()
    writer = csv.DictWriter(file_stream, fieldnames=fields,
                            delimiter=delimiter, quotechar=quotechar, extrasaction="ignore")

    writer.writeheader()
    writer.writerows(data)

    return file_stream.getvalue()
