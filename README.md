# Shapeshifter: a tiny standalone Python JSON/CSV data converter

Are you sitting between developers using JSON APIs and business analysts using Excels and CSVs? Does your job require a lot of tedious data conversion from/to JSON and CSV? Do you have to deal with JSON APIs that regurgitate half of the database on every endpoint, regardless of what you actually need?

If the answer was yes, look no further than here. This library lets you convert JSON -> CSV or CSV -> JSON in one terminal command, or it can be embedded into another Python script as a dependency.

## Quickstart Guide - running Shapeshifter from the command line

Use shapeshifter_cli.py for a simple, no-nonsense command line script that fetches data from a local file or a web URL, converts to another data format, then saves the result to the filesystem.

Getting help:
`python shapeshifter_cli.py -h`

Basic:
`python shapeshifter_cli.py ~/username/source.json`
The output filepath will be the same as source filepath, with .csv/.json swapped. If the source is a web url, it will be web_datasource.json or web_datasource.csv.

Specify the destination:
`python shapeshifter_cli.py ~/username/source.json -f ~/username/destination.csv`

Using comma delimiters:
`python shapeshifter_cli.py ~/username/source.csv -f ~/username/destination.json -d ','`

Using a web URL as a source:
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/username/destination.csv`

Also include headers:
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/username/destination.csv -h '{"Authorization": "Basic EXAMPLE_AUTH_VALUE"}'`

Keep the same data format (fetch & save as-is):
`python shapeshifter_cli.py https://www.example.com/rest/etc -f ~/username/destination.csv --keep-datatype`

Remove some fields from the output:
`python shapeshifter_cli.py ~/username/source.json -e "spam,ham"`

Add some fields and remove some fields:
`python shapeshifter_cli.py ~/username/source.json -i "spam,ham" -e "eggs,bacon"`

Return only specific fields:
`python shapeshifter_cli.py ~/username/source.json -o "spam,ham"`

### How to set up the quick shell function shortcut

1. In shell-snippets/shapeshifter-shell.sh, change the value of `SHAPESHIFTER_PATH` to the root folder where this repo was copied.
2. Include the shapeshifter-shell.sh in your `.bash_profile`, `.zshrc` or other equivalent file, e.g. `source ~/path-to-this-repo/shell-snippets/shapeshifter-shell.sh`

### Using Shapeshifter as a module inside another Python script

For advanced use, import the shapeshifter.py module into your own code.

Importing the module:
`import shapeshifter.Shapeshifter`
`from shapeshifter import Shapeshifter`

Instantiating an instance:
`instance = Shapeshifter(config=CONFIG)`

Every method apart from the get methods returns the object itself so calls can be chained.

Convert JSON -> CSV:
`result = instance.from_json(DATA_SOURCE).to_csv()`

Convert CSV -> JSON:
`result = instance.from_csv(DATA_SOURCE).to_json()`

Fetch JSON, add some fields and remove some fields, then back to JSON:
`result = instance.from_json(DATA_SOURCE).include(["spam","ham"]).exclude(["eggs"]).to_json()`

Do some JSON filtering and get snapshots of the data at each stage:

```python
instance.from_json(DATA_SOURCE)
result1 = instance.include(["spam","ham"]).to_json()
result2 = instance.exclude(["eggs"]).to_json()
```

## Documentation

This converter works in four stages:

* Fetch the data source, convert it to Python data structures
* Apply field filtering or data modification actions
* Convert the data to the target data type
* Save to file

### Configuration settings: the config file

The command line script reads from `./config.json` to fetch settings for the `headers`, `delimiter` and `quotechar` variables. If these fields are not in the config file or if the config file fails to loads/could not be found, there are also default values as fallbacks. These fields can be overwritten by passing in command line corresponding arguments.

### Fetching from the data source

This script supports reading from a web URL and from a local file. To specific reading from a web URL, make sure your data source starts with `http://` or `https://`. If it starts with anything else, the script will interpret it as a local filepath. If the data source is a web URL which expects security headers, they can be defined in the config file (if you're usually fetching from the same endpoint) or passed in from a command line argument.

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

## Roadmap

[Roadmap here](./Roadmap.md)
