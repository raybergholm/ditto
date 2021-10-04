#!/usr/bin/env python3

import argparse
import json

from utils.file import check_filetype, read_file, save_file
from ditto import Ditto


CONFIG_FILEPATH = "./config.json"

ARG_DELIMITER = ","


def ditto_cli():
    args = parse_arguments()

    data_source_path = args.data_source_path

    config = load_config()

    ditto = Ditto(data_source_path, config=config, delimiter=args.delimiter, quotechar=args.quotechar, headers=args.headers)

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
        if input_datatype not in Ditto.SUPPORTED_DATA_TYPES:
            print("File extension not supported (check if it was a .json or .csv file)")
            return

        if args.keep_datatype:
            output_datatype = input_datatype
        else:
            output_datatype = "json" if input_datatype == "csv" else "csv"

        # If no output filepath was supplied, use the same filepath as the input and just switch the filetype
        output_filepath = args.output_filepath if args.output_filepath else "{0}.{1}".format(
            args.data_source_path.split(".")[0], output_datatype)

    ditto.fetch()

    if input_datatype == "json":
        ditto.from_json()
    elif input_datatype == "csv":
        ditto.from_csv()
    else:
        print("Whatever you did to get here was definitely not supported")
        return

    if len(args.include) > 0:
        ditto.include(args.include)

    if len(args.exclude) > 0:
        ditto.exclude(args.exclude)

    if len(args.only) > 0:
        ditto.only(args.only)
    
    if output_datatype == "json":
        ditto.to_json()
    elif output_datatype == "csv":
        ditto.to_csv()
    else:
        print("Whatever you did to get here was definitely not supported")
        return
    
    output_data = ditto.get_output()

    save_file(output_filepath, output_data)
    print("File saved to %s" % output_filepath)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ditto: a tiny standalone JSON/CSV converter")
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
                        default=Ditto.DEFAULT_HEADERS, help="Include these headers in a HTTPS request. This argument is only used when fetching from a URL")

    parser.add_argument("--delimiter", dest="delimiter", action="store",
                        default=Ditto.DEFAULT_CSV_DELIMITER, help="CSV delimiter to use when reading (default: {0} )".format(repr(Ditto.DEFAULT_CSV_DELIMITER)))
    parser.add_argument("--quotechar", dest="quotechar", action="store",
                        default=Ditto.DEFAULT_CSV_QUOTECHAR, help="CSV quotechar (default: {0} )".format(repr(Ditto.DEFAULT_CSV_QUOTECHAR)))

    args = parser.parse_args()
    return args


def load_config():
    try:
        return json.loads(read_file(CONFIG_FILEPATH))
    except FileNotFoundError:
        print("No config file found, check if {0} exists".format(
            CONFIG_FILEPATH))
        return {}
    except json.decoder.JSONDecodeError:
        print("Parsing error when loading the config file, check if {0} is formatted correctly".format(
            CONFIG_FILEPATH))
        return {}


if __name__ == "__main__":
    ditto_cli()
