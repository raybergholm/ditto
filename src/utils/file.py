#!/usr/bin/env python3


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
