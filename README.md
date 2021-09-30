# Ditto: a tiny standalone Python JSON/CSV converter

Convert JSON -> CSV or CSV -> JSON in one straightforward terminal command.

This was originally created to deal with an environment rich in both JSON and CSV data from various systems which required comparison and analysis, while also stuck with an older version of Excel that did not offer JSON parsing options.

## Quickstart Guide

### How to use Ditto from the command line

Getting help:
`python ditto.py -h`

Basic:
`python ditto.py {SOURCE_FILEPATH}`
The output filepth will be the same as source filepath, with .csv/.json swapped

Specify the destination:
`python ditto.py {SOURCE_FILEPATH} -o {DESTINATION_FILEPATH}`

Using comma delimiters:
`python ditto.py {SOURCE_FILEPATH} -o {DESTINATION_FILEPATH} -d ','`

### How to set up the quick shell function shortcut

1. In shell-snippets/ditto-shell.sh, change the value of `DITTO_PATH` to the root folder where this repo was copied.
2. Include the ditto-shell.sh in your `.bash_profile`, `.zshrc` or other equivalent file, e.g. `source ~/path-to-this-repo/shell-snippets/ditto-shell.sh`

## Documentation

This converter works in four stages:

* Fetch the data source, convert it to Python lists/dictionaries
* Apply field filtering or data modification actions
* Convert the data to the target datatype
* Save the file

### Modifying the output with include, exclude and only

#### --include

Fields defined in the --include argument will always be included in the output.

This can be useful if your data source is e.g. a NoSQL database forwarding data to a API which returns JSON. Since the data source is NoSQL, the field you're looking for may not even be there, and if the REST API doesn't handle this, then you'd need to do it yourself. If you need your output in CSV, you'll want your output to have the same fields on all entries so --include will cover this case.

#### --exclude

Fields defined in the --exclude argument will be excluded from the output.

If your data source is unnecessarily verbose for your purpose, use the --exclude argument to strip specific fields out of the output. This can support scenarios when your data source has variable structure, but you also know there are specific fields you do not want in the output.

#### --only

Fields defined in the --only argument will be the only fields in the output.

Just like the exclude case, if your data source is unnecessarily verbose for your purpose you may want to remove some fields. There may be some more extreme cases like getting a raw dump of a 20 column table filled with stuff you have no clue about when you only need two fields. In this scenario you can use the --only argument to strip out everything else.
