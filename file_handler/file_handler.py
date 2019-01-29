#!/usr/bin/env python3

def read_file(filepath, line_delimiter=None):
    try:
        with open(filepath, "r") as file_stream:
            data = file_stream.read()
            if line_delimiter != None:
                data = data.split(line_delimiter)
        return data
    except OSError as error:
        print(str(error))

def save_file(filepath, data):
    try:
        with open(filepath, "w+") as file_stream:
            try:
                for entry in data:
                    file_stream.write(str(entry))
            except TypeError:
                file_stream.write(entry)
    except OSError as error:
        print(str(error))