#!/usr/bin/env python3

import argparse
import json

from utils.converter import from_json, from_csv, to_json, to_csv
from utils.file import check_filetype, read_file, save_file

CONFIG_FILEPATH = "./config.json"

ARG_DELIMITER = ","

DEFAULT_HEADERS = []
DEFAULT_CSV_DELIMITER = ";"
DEFAULT_CSV_QUOTECHAR = "\""


def main():
    args = parse_arguments()

    data_source_path = args.data_source_path

    config = load_config()

    if not "headers" in config or args.headers != DEFAULT_HEADERS:
        config["headers"] = json.loads(args.headers)
    if not "delimiter" in config or args.delimiter != DEFAULT_CSV_DELIMITER:
        config["delimiter"] = args.delimiter
    if not "quotechar" in config or args.quotechar != DEFAULT_CSV_QUOTECHAR:
        config["quotechar"] = args.quotechar

    # Fetch data
    if data_source_path.startswith("http://") or data_source_path.startswith("https://"):
        source_data = fetch_from_web(
            data_source_path, config["headers"])

        # initial use case: just support JSON -> CSV
        input_datatype = "json"
        output_datatype = "csv"

        output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
            "web_datasource", output_datatype)
    else:
        input_datatype = check_filetype(args.data_source_path)
        if input_datatype not in ["json", "csv"]:
            print("File extension not supported (check if it was a .json or .csv file)")
            return

        output_datatype = "json" if input_datatype == "csv" else "csv"
        # If no output filepath was supplied, use the same filepath as the input and just switch the filetype
        output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
            args.data_source_path.split(".")[0], output_datatype)

        source_data = fetch_from_file(data_source_path)

    if not source_data:
        print("No data received after fetching from source")
        return

    data = None
    if input_datatype == "json":
        data = from_json(source_data)
    elif input_datatype == "csv":
        data = from_csv(source_data, config["delimiter"], config["quotechar"])
    else:
        print("Whatever you did to get here was definitely not supported")
        return

    if len(args.include) > 0:
        include_list = args.include.split(ARG_DELIMITER)
        data = include_fields(data, include_list)

    if len(args.exclude) > 0:
        exclude_list = args.exclude.split(ARG_DELIMITER)
        data = exclude_fields(data, exclude_list)

    if len(args.only) > 0:
        filter_list = args.only.split(ARG_DELIMITER)
        data = filter_fields(data, filter_list)

    if output_datatype == "json":
        output_data = to_json(data)
    elif output_datatype == "csv":
        output_data = to_csv(data, config["delimiter"], config["quotechar"])
    else:
        print("Whatever you did to get here was definitely not supported")
        return
    # Save to file
    save_file(output_filepath, output_data)
    print("File saved to %s" % output_filepath)


def load_config():
    try:
        return json.loads(read_file(CONFIG_FILEPATH))
    except FileNotFoundError:
        print("No config file found, check if {0} exists".format(CONFIG_FILEPATH))
        return {}
    except json.decoder.JSONDecodeError:
        print("Parsing error when loading the config file, check if {0} is formatted correctly".format(CONFIG_FILEPATH))
        return {}


def fetch_from_web(url, headers):
    import requests
    print("Fetching from URL {0}".format(url))

    response = requests.get(url, headers=headers)

    if response.ok:
        return response.text
    else:
        print("Failed to fetch from {0}".format(url))
        print("Error response: {0} {1}".format(response.status_code, response.text))
        return None


def fetch_from_file(filepath):
    print("Fetching from filepath {0}".format(filepath))
    return read_file(filepath)


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
    parser.add_argument(
        "data_source_path", help="Path to the data source. Web sources start with http:// or https://, otherwise this script will try to fetch from a local file")
    parser.add_argument("-f", "--filepath", dest="output_filepath", action="store",
                        help="filepath to save the content (default is to use the same path and name as the input)")

    parser.add_argument("-i", "--include", dest="include", action="store",
                        default="", help="always include these fields (populate as empty values if they don't exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-e", "--exclude", dest="exclude", action="store",
                        default="", help="always exclude these fields (remove these fields if they exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-o", "--only", dest="only", action="store",
                        default="", help="copy only these fields (only these fields will appear in the output file). Use the format FIELD1,FIELD2,FIELD3")

    parser.add_argument("--headers", dest="headers", action="store",
                        default=DEFAULT_HEADERS, help="Include these headers in a HTTPS request. This argument is only used when fetching from a URL")

    parser.add_argument("--delimiter", dest="delimiter", action="store",
                        default=DEFAULT_CSV_DELIMITER, help="CSV delimiter to use when reading (default: {0} )".format(repr(DEFAULT_CSV_DELIMITER)))
    parser.add_argument("--quotechar", dest="quotechar", action="store",
                        default=DEFAULT_CSV_QUOTECHAR, help="CSV quotechar (default: {0} )".format(repr(DEFAULT_CSV_QUOTECHAR)))

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
