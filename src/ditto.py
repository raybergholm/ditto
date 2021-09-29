#!/usr/bin/env python3

import argparse

from utils.converter import check_filetype, from_json_file, from_csv_file, json_to_csv, csv_to_json
from utils.file import read_file, save_file


def convert_and_save():
    args = parse_arguments()

    input_filetype = check_filetype(args.input_filepath)
    output_filetype = "json" if input_filetype == "csv" else "csv"

    if input_filetype == "json":
        data = convert_json_to_csv(args.input_filepath, delimiter=args.delimiter,
                                   newline=args.newline, filter_fields=args.filter.split(";"), forced_output_fields=args.forced_output_fields.split(";"))
    elif input_filetype == "csv":
        data = convert_csv_to_json(args.input_filepath, delimiter=args.delimiter,
                                   newline=args.newline, filter_fields=args.filter.split(";"), forced_output_fields=args.forced_output_fields.split(";"))
    else:
        print("File extension not supported (check if it was a .json or .csv file)")
        return

    # If no output filepath was supplied, use the same filepath as the input and just switch the filetype
    output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
        args.input_filepath.split(".")[0], output_filetype)

    save_file(output_filepath, data)
    print("File saved to %s" % output_filepath)


def convert_json_to_csv(filepath, delimiter=";", newline="\n", filter_fields=[], forced_output_fields=[]):
    data = from_json_file(filepath)

    if forced_output_fields:
        for entry in data:
            for field in forced_output_fields:
                if field not in entry:
                    entry[field] = ""

    if filter_fields:
        filtered_data = []
        for entry in data:
            filtered_entry = {key: value for key,
                                value in entry.items() if key in filter_fields}
            filtered_data.append(filtered_entry)
        data = filtered_data

    return json_to_csv(data)


def convert_csv_to_json(filepath, delimiter=";", newline="\n", filter_fields=None):
    (header, data) = from_csv_file(filepath, delimiter, newline)

    if filter_fields:
        pass
    return csv_to_json(header, data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ditto: a tiny standalone JSON/CSV converter")
    parser.add_argument("input_filepath", help="filepath to the input file")
    parser.add_argument("-o", "--out", dest="output_filepath", action="store",
                        help="filepath to save the content (default is to use the same path and name as the input)")
    parser.add_argument("-d", "--delimiter", dest="delimiter", action="store",
                        default=";", help="CSV delimiter to use when reading (default: semicolon)")
    parser.add_argument("-n", "--newline", dest="newline", action="store",
                        default="\n", help="newline type (default: \"\\n\")")
    parser.add_argument("-f", "--filter", dest="filter", action="store",
                        default="", help="fields to use as an filter in FIELD1;FIELD2;FIELD3 format. Only these fields will appear in the output file")
    parser.add_argument("--force-output-fields", dest="forced_output_fields",
                        action="store", default="", help="on JSON->CSV conversion, always include these fields (use comma delimited lists)")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    convert_and_save()
