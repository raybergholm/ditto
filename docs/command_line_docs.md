# Shapeshifter from the command line

Use shapeshifter_cli.py for a simple, no-nonsense command line script that fetches data from a local file or a web URL, converts to another data format, then saves the result to the filesystem.

## Quickstart

Getting help:
`python shapeshifter_cli.py -h`

Basic:
`python shapeshifter_cli.py ~/localdir/source.json`
The output filepath will be the same as source filepath, with .csv/.json swapped. If the source is a web url, it will be web_datasource.json or web_datasource.csv.

Specify the destination:
`python shapeshifter_cli.py ~/localdir/source.json -f ~/localdir/destination.csv`

Using comma delimiters:
`python shapeshifter_cli.py ~/localdir/source.csv -f ~/localdir/destination.json -d ','`

Using a web URL as a source:
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/localdir/destination.csv`

Also include headers:
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/localdir/destination.csv -h '{"Authorization": "Basic EXAMPLE_AUTH_VALUE"}'`

Keep the same data format (fetch & save as-is):
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/localdir/destination.csv --keep-datatype`

Remove some fields from the output:
`python shapeshifter_cli.py ~/localdir/source.json -e "spam,ham"`

Add some fields and remove some fields:
`python shapeshifter_cli.py ~/localdir/source.json -i "spam,ham" -e "eggs,bacon"`

Return only specific fields:
`python shapeshifter_cli.py ~/localdir/source.json -o "spam,ham"`

### How to set up the quick shell function shortcut

1. In shell-snippets/shapeshifter-shell.sh, change the value of `SHAPESHIFTER_PATH` to the root folder where this repo was copied.
2. Include the shapeshifter-shell.sh in your `.bash_profile`, `.zshrc` or other equivalent file, e.g. `source ~/path_to_this_repo/shell-snippets/shapeshifter-shell.sh`

## Documentation

This script works in four stages:

* Fetch the data source, convert it to Python data structures
* Apply field filtering or data modification actions
* Convert the data to the target data type
* Save to file

### Fetching from the data source

This script supports reading from a web URL and from a local file. To specify reading from a web URL, make sure your data source starts with `http://` or `https://`. If it starts with anything else, the script will interpret it as a local filepath. If the data source is a web URL which expects security headers, they can be defined in the config file (if you're usually fetching from the same endpoint) or passed in from a command line argument.

### Defining config settings

#### Using the config file

The script reads from `./config.json` to fetch settings for the `headers`, `delimiter` and `quotechar` variables. If these fields are not in the config file or if the config file fails to loads/could not be found, there are also default values as fallbacks.

#### Using command line arguments

The config file supports defining custom values for `headers`, `delimiter` and `quotechar`, however they can also be overwritten by corresponding command line arguments `--headers` `--delimiter` `--quotechar`.

### Modifying the output with include, exclude and only arguments

#### --include

Fields defined in the --include argument will always be included in the output.

This can be useful if your data source is e.g. a NoSQL database forwarding data to a API which returns JSON. Since the data source is NoSQL, the field you're looking for may not even be there, and if the REST API doesn't handle this, then you'd need to do it yourself. If you need your output in CSV, you'll want your output to have the same fields on all entries so --include will cover this case.

#### --exclude

Fields defined in the --exclude argument will be excluded from the output.

If your data source is unnecessarily verbose for your purpose, use the --exclude argument to strip specific fields out of the output. This can support scenarios when your data source has variable structure, but you also know there are specific fields you do not want in the output.

#### --only

Fields defined in the --only argument will be the only fields in the output.

Just like the exclude case, if your data source is unnecessarily verbose for your purpose you may want to remove some fields. There may be some more extreme cases like getting a raw dump of a 20 column table filled with stuff you have no clue about when you only need two fields. In this scenario you can use the --only argument to strip out everything else.
