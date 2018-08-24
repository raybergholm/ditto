#!/usr/bin/env python3

import argparse

from file_handler.file_handler import read_file, save_file
from converter.converter import convert_json_to_csv, convert_csv_to_json, check_filetype

def main():
    args = parse_arguments()

    delimiter = args.delimiter if args.delimiter != None else ";"
    field_list = args.fields

    input_file_type = check_filetype(args.input_filepath)

    if input_file_type == "json":
        input_data = read_file(args.input_filepath)
        data = convert_json_to_csv(input_data, delimiter, field_list)
    elif input_file_type == "csv":
        input_data = read_file(args.input_filepath, line_delimiter="\n")
        data = convert_csv_to_json(input_data, delimiter, field_list)
    else:
        print("File extension not supported (check if it was a .json or .csv file)")
        return

    data = post_processing(data)

    save_file(args.output_filepath, data)
    print("File saved to %s" % args.output_filepath)

def post_processing(data):  # if post processing is necessary.
    # TODO: move this stuff to an optional module that can be loaded via an optional arg
    return data

def parse_arguments():
    parser = argparse.ArgumentParser(description="JSON to CSV converter")
    parser.add_argument("input_filepath", help="filepath to the input file")
    parser.add_argument("output_filepath", help="filepath to save the content")
    parser.add_argument("-d", "--delimiter", dest="delimiter", action="store", help="delimiter to use (default is semicolon)")
    parser.add_argument("-f", "--fields", dest="fields", action="store", help="fields to use as an filter (FIELD1;FIELD2;FIELD3)")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()