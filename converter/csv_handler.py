#!/usr/bin/env python3

import csv

def from_csv_file(filepath, delimiter=";", quotechar="\"", has_header=True):
    try:
        header = None
        data = []
        with open(filepath, mode="r", newline="") as file_stream:
            reader = csv.reader(file_stream, delimiter=delimiter, quotechar=quotechar)
            if has_header:
                for i, row in enumerate(reader):
                    if i == 0:
                        header = row
                    else:
                        data.append(row)
            else:
                data = [row for row in reader]
        return (header, data)
    except OSError as error:
        print("OSError thrown in from_csv_file(): %s" % str(error))
    except TypeError as error:
        print("TypeError thrown in from_csv_file(): %s" % str(error))
    except Exception as error:
        print("General exception thrown in from_csv_file(): %s" % str(error))

def to_csv_file(filepath, data, header=None, delimiter=";", quotechar="\""):
    try:
        with open(filepath, mode="w+", newline="") as file_stream:
            writer = csv.writer(file_stream, delimiter=delimiter, quotechar=quotechar)

            if header != None:
                writer.writerow(header)
            
            for entry in data:
                writer.writerow(entry)

    except OSError as error:
        print("OSError thrown in to_csv_file(): %s" % str(error))
    except TypeError as error:
        print("TypeError thrown in to_csv_file(): %s" % str(error))
    except Exception as error:
        print("General exception thrown in to_csv_file(): %s" % str(error))