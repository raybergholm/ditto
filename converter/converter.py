#!/usr/bin/env python3

import json

JSON_TYPE = "json"
CSV_TYPE = "csv"

def check_filetype(filepath):
    if filepath.endswith(".%s" % JSON_TYPE):
        return JSON_TYPE
    elif filepath.endswith(".%s" % CSV_TYPE):
        return CSV_TYPE
    else:
        return ""

def convert_json_to_csv(input_data, delimiter, field_list):
    json_data = json.loads(input_data)

    fields = field_list if field_list != None else json_data[0].keys()
    header = "%s\n" % delimiter.join(fields)

    content = []
    for entry in json_data:
        filtered = [str(entry[field]) if field in entry else "" for field in fields]
        content.append("%s\n" % delimiter.join(filtered))

    output_data = [header]

    for entry in content:
        output_data.append(entry)

    return output_data

def convert_csv_to_json(input_data, delimiter, field_list):

    content = []
    for i, line in enumerate(input_data):
        if i == 0:
            header = line.split(delimiter)
        else:
            content.append(line.split(delimiter))

    output_data = []
    for line in content:
        entry = { header[i]: field for i, field in enumerate(line) }
        output_data.append(entry)

    output_data = json.dumps(output_data)

    return output_data