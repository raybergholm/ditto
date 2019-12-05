# Ditto: a tiny standalone Python JSON/CSV converter

Convert JSON -> CSV or CSV -> JSON in one straightforward terminal command.

This was originally created to deal with an environment rich in both JSON and CSV data from various systems which required comparison and analysis, while also stuck with an older version of Excel that did not offer JSON parsing options.

## Quickstart Guide

### How to use Ditto from the command line

Getting help:
`python ditto.py -h`

Basic:
`python ditto.py {SOURCE_FILEPATH}`

Specify the destination:
`python ditto.py {SOURCE_FILEPATH} -o {DESTINATION_FILEPATH}`

Using comma delimiters:
`python ditto.py {SOURCE_FILEPATH} -o {DESTINATION_FILEPATH} -d ','`

### How to set up the quick shell function shortcut

1. In shell-snippets/ditto-shell.sh, change the value of `DITTO_PATH` to the root folder where this repo was copied.
2. Include the ditto-shell.sh in your `.bash_profile`, `.zshrc` or other equivalent file, e.g. `source ~/path-to-this-repo/shell-snipppets/ditto-shell.sh`

### Arguments list

Argument | Name | Default value | Description
{0}| Source filepath | N/A | Filepath of the file to be converted
-o / --output | Destination filepath | Same as source filepath | Filepath where the result will be saved
-d / --delimiter | CSV delimiter | ';' | CSV delimiter to be used when parsing/building the CSV file
-n / --newline | Newline | '\\n' | Newline used when parsing/building the CSV file
-f / --fields | Field list | None | Specified field list in semicolon delimited format (i.e. FIELD1;FIELD2;FIELD3). If set to None, use all fields. For JSON -> CSV the first entry is used as a template; if the first entry is not indicative of the desired data structure then specify the field list
