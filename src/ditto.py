#!/usr/bin/env python3

import argparse

from utils.converter import check_filetype, from_json_file, from_csv_file, json_to_csv, to_json
from utils.file import read_file, save_file

ARG_DELIMITER = ","

DEFAULT_CSV_DELIMITER = ";"
DEFAULT_CSV_NEW_LINE = "\n"


def convert_and_save():
    args = parse_arguments()

    input_filetype = check_filetype(args.input_filepath)
    output_filetype = "json" if input_filetype == "csv" else "csv"

    if input_filetype == "json":
        data = convert_json_to_csv(args.input_filepath, delimiter=args.delimiter,
                                   newline=args.newline, include_string=args.include, exclude_string=args.exclude, filter_string=args.only)
    elif input_filetype == "csv":
        data = convert_csv_to_json(args.input_filepath, delimiter=args.delimiter,
                                   newline=args.newline, include_string=args.include, exclude_string=args.exclude, filter_string=args.only)
    else:
        print("File extension not supported (check if it was a .json or .csv file)")
        return

    # If no output filepath was supplied, use the same filepath as the input and just switch the filetype
    output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
        args.input_filepath.split(".")[0], output_filetype)

    save_file(output_filepath, data)
    print("File saved to %s" % output_filepath)


def convert_json_to_csv(filepath, delimiter=";", newline="\n", include_string="", exclude_string="", filter_string=""):
    data = from_json_file(filepath)

    if len(include_string) > 0:
        include_list = include_string.split(ARG_DELIMITER)
        data = include_fields(data, include_list)

    if len(exclude_string) > 0:
        exclude_list = exclude_string.split(ARG_DELIMITER)
        data = exclude_fields(data, exclude_list)

    if len(filter_string) > 0:
        filter_list = filter_string.split(ARG_DELIMITER)
        data = filter_fields(data, filter_list)

    return json_to_csv(data)


def convert_csv_to_json(filepath, delimiter=";", newline="\n", include_string="", exclude_string="", filter_string=""):
    data = from_csv_file(filepath, delimiter, newline)

    if len(include_string) > 0:
        include_list = include_string.split(ARG_DELIMITER)
        data = include_fields(data, include_list)

    if len(exclude_string) > 0:
        exclude_list = exclude_string.split(ARG_DELIMITER)
        data = exclude_fields(data, exclude_list)

    if len(filter_string) > 0:
        filter_list = filter_string.split(ARG_DELIMITER)
        data = filter_fields(data, filter_list)

    # print(data)
    return to_json(data)


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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ditto: a tiny standalone JSON/CSV converter")
    parser.add_argument("input_filepath", help="filepath to the input file")
    parser.add_argument("-f", "--filepath", dest="output_filepath", action="store",
                        help="filepath to save the content (default is to use the same path and name as the input)")

    parser.add_argument("-i", "--include", dest="include", action="store",
                        default="", help="always include these fields (populate as empty values if they don't exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-e", "--exclude", dest="exclude", action="store",
                        default="", help="always exclude these fields (remove these fields if they exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-o", "--only", dest="only", action="store",
                        default="", help="copy only these fields (only these fields will appear in the output file). Use the format FIELD1,FIELD2,FIELD3")

    parser.add_argument("-d", "--delimiter", dest="delimiter", action="store",
                        default=DEFAULT_CSV_DELIMITER, help="CSV delimiter to use when reading (default: semicolon)")
    parser.add_argument("-n", "--newline", dest="newline", action="store",
                        default=DEFAULT_CSV_NEW_LINE, help="newline type (default: \"\\n\")")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    convert_and_save()
