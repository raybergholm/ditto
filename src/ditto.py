#!/usr/bin/env python3

import argparse

from utils.converter import check_filetype, from_json_file, from_csv_file, json_to_csv, csv_to_json
from utils.file import read_file, save_file


def convert_and_save():
    args = parse_arguments()

    delimiter = args.delimiter if args.delimiter != None else ";"
    field_list = args.fields

    input_filetype = check_filetype(args.input_filepath)
    output_filetype = "json" if input_filetype == "csv" else "csv"

    if input_filetype == "json":
        # input_data = read_file(args.input_filepath)
        data = convert_json_to_csv(args.input_filepath, delimiter, field_list)
    elif input_filetype == "csv":
        # input_data = read_file(args.input_filepath, line_delimiter=args.newline)
        data = convert_csv_to_json(args.input_filepath, delimiter, field_list)
    else:
        print("File extension not supported (check if it was a .json or .csv file)")
        return

    output_filepath = args.output_filepath if args.output_filepath else "%s.%s" % (
        args.input_filepath.split(".")[0], output_filetype)

    save_file(output_filepath, data)
    print("File saved to %s" % output_filepath)


def convert():
    pass

def convert_json_to_csv(filepath, delimiter=";", newline="\n", fieldnames=None):
    data = from_json_file(filepath, fieldnames)
    return json_to_csv(data)


def convert_csv_to_json(filepath, delimiter=";", newline="\n", fieldnames=None):
    (header, data) = from_csv_file(filepath, delimiter, newline)
    return csv_to_json(header, data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ditto: a tiny standalone JSON/CSV converter")
    parser.add_argument("input_filepath", help="filepath to the input file")
    parser.add_argument("-o", "--out", dest="output_filepath", action="store",
                        help="filepath to save the content (default is to use the same path and name as the input)")
    parser.add_argument("-d", "--delimiter", dest="delimiter", action="store",
                        default=";", help="delimiter to use (default: semicolon)")
    parser.add_argument("-n", "--newline", dest="newline", action="store",
                        default="\n", help="newline type (default: \"\\n\")")
    parser.add_argument("-f", "--fields", dest="fields", action="store",
                        help="fields to use as an filter (FIELD1;FIELD2;FIELD3)")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    convert_and_save()
