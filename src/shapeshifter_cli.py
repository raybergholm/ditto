#!/usr/bin/env python3

import argparse
import os
import json

from utils.file import check_filetype, read_file, save_file
from shapeshifter import Shapeshifter


CONFIG_FILENAME = "config.json"

ARG_DELIMITER = ","


def shapeshifter_cli():
    args = parse_arguments()

    data_source_path = args.data_source_path

    config_filepath = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILENAME)
    config = load_config(config_filepath)

    paging_config = None
    if args.page_iterator and args.page_range:
        [min_range, max_range] = args.page_range.split(",")
        paging_config = {
            "iterator": args.page_iterator,
            "min": int(min_range),
            "max": int(max_range)
        }

    shapeshifter = Shapeshifter(config=config, delimiter=args.delimiter, quotechar=args.quotechar, headers=args.headers, paging=paging_config)

    if data_source_path.startswith("http://") or data_source_path.startswith("https://"):
        input_datatype = "json"

        if args.keep_datatype:
            output_datatype = input_datatype
        else:
            output_datatype = "csv"
        
        output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
            "web_datasource", output_datatype)
    else:
        input_datatype = check_filetype(args.data_source_path)
        if input_datatype not in Shapeshifter.SUPPORTED_DATA_TYPES:
            print("File extension not supported (check if it was a .json or .csv file)")
            return

        if args.keep_datatype:
            output_datatype = input_datatype
        else:
            output_datatype = "json" if input_datatype == "csv" else "csv"

        # If no output filepath was supplied, use the same filepath as the input and just switch the filetype
        output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
            args.data_source_path.split(".")[0], output_datatype)

    if input_datatype == "json":
        shapeshifter.from_json(data_source_path)
    elif input_datatype == "csv":
        shapeshifter.from_csv(data_source_path)
    else:
        print("Whatever you did to get here was definitely not supported")
        return

    if len(args.include) > 0:
        include_list = args.include.split(ARG_DELIMITER)
        shapeshifter.include(*include_list)

    if len(args.exclude) > 0:
        exclude_list = args.exclude.split(ARG_DELIMITER)
        shapeshifter.exclude(*exclude_list)

    if len(args.only) > 0:
        only_list = args.only.split(ARG_DELIMITER)
        shapeshifter.only(*only_list)
    
    if args.filter_by_value:
        [filter_field, filter_operator, filter_value] = args.filter_by_value.split(" ")
        shapeshifter.filter(filter_field, filter_operator, filter_value)

    if output_datatype == "json":
        output_data = shapeshifter.to_json()
    elif output_datatype == "csv":
        output_data = shapeshifter.to_csv()
    else:
        print("Whatever you did to get here was definitely not supported")
        return

    save_file(output_filepath, output_data)
    print("File saved to %s" % output_filepath)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Shapeshifter: a tiny standalone JSON/CSV converter")
    parser.add_argument(
        "data_source_path", help="Path to the data source. Web sources start with http:// or https://, otherwise this script will try to fetch from a local file")
    parser.add_argument("-f", "--filepath", dest="output_filepath", action="store",
                        help="filepath to save the content (default is to use the same path and name as the input)")
    parser.add_argument("-k", "--keep-datatype", dest="keep_datatype", action="store_true",
                        help="Keep the same datatype. Use this to create a copy or filtered copy of the data source")

    parser.add_argument("-i", "--include", dest="include", action="store",
                        default="", help="always include these fields (populate as empty values if they don't exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-e", "--exclude", dest="exclude", action="store",
                        default="", help="always exclude these fields (remove these fields if they exist in the source). Use the format FIELD1,FIELD2,FIELD3")
    parser.add_argument("-o", "--only", dest="only", action="store",
                        default="", help="copy only these fields (only these fields will appear in the output file). Use the format FIELD1,FIELD2,FIELD3")

    parser.add_argument("--headers", dest="headers", action="store",
                        default=Shapeshifter.DEFAULT_HEADERS, help="Include these headers in a HTTPS request. This argument is only used when fetching from a URL")
    
    parser.add_argument("--page-iterator", dest="page_iterator", action="store",
                        default=None, help="Include these headers in a HTTPS request. This argument is only used when using the page iteration functionality")
    parser.add_argument("--page-range", dest="page_range", action="store",
                        default=None, help="Include these headers in a HTTPS request. Use the format MIN,MAX. This argument is only used when using the page iteration functionality")


    parser.add_argument("--delimiter", dest="delimiter", action="store",
                        default=Shapeshifter.DEFAULT_CSV_DELIMITER, help="CSV delimiter to use when reading (default: {0} )".format(repr(Shapeshifter.DEFAULT_CSV_DELIMITER)))
    parser.add_argument("--quotechar", dest="quotechar", action="store",
                        default=Shapeshifter.DEFAULT_CSV_QUOTECHAR, help="CSV quotechar (default: {0} )".format(repr(Shapeshifter.DEFAULT_CSV_QUOTECHAR)))

    parser.add_argument("--filter", dest="filter_by_value", action="store",
                        default="", help="filter the output based on this argument. Expects a FIELD = VALUE format")


    args = parser.parse_args()
    return args


def load_config(config_filepath):
    try:
        return json.loads(read_file(config_filepath))
    except FileNotFoundError:
        print("No config file found, check if {0} exists".format(
            config_filepath))
        return {}
    except json.decoder.JSONDecodeError:
        print("Parsing error when loading the config file, check if {0} is formatted correctly".format(
            config_filepath))
        return {}


if __name__ == "__main__":
    shapeshifter_cli()
