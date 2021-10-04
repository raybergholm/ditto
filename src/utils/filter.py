#!/usr/bin/env python3


def include_fields(data, field_list):
    filtered_output = []
    for entry in data:
        extra_fields = {key: "" for key in field_list}
        filtered_output.append({**extra_fields, **entry})
    return filtered_output


def exclude_fields(data, field_list):
    filtered_output = []
    for entry in data:
        filtered_entry = {key: value for key,
                          value in entry.items() if key not in field_list}
        filtered_output.append(filtered_entry)
    return filtered_output


def filter_fields(data, field_list):
    filtered_output = []
    for entry in data:
        filtered_entry = {key: value for key,
                          value in entry.items() if key in field_list}
        filtered_output.append(filtered_entry)
    return filtered_output
