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

### Arguments list

| Argument | Optional arg shortcut | Name | Default value | Description |
| --- | --- | --- | --- | --- |
| {0} |  | Source filepath | N/A | Filepath of the file to be converted |
| --output | -o | Destination filepath | Same as source filepath | Filepath where the result will be saved |
| --include | -i | Include fields | "" | Always include these fields (populate as empty values if they don't exist in the source). Use the format FIELD1,FIELD2,FIELD3 |
| --exclude | -e | Exclude fields | "" | Always exclude these fields (remove these fields if they exist in the source). Use the format FIELD1,FIELD2,FIELD3 |
| --only | -i | Only fields | "" | Copy only these fields (only these fields will appear in the output file). Use the format FIELD1,FIELD2,FIELD3 |
| --delimiter | -d | CSV delimiter | ';' | CSV delimiter to be used when parsing/building the CSV file |
| --newline | -n | Newline | '\n' | Newline used when parsing/building the CSV file |

