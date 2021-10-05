# Changelog

## v4.0

* Renamed project to Shapeshifter.
* The include/exclude/only methods now expect variable arguments rather than a single list argument

## v3.2

* Moved the data fetching step to `from_json` and `from_csv`. This means that you don't call `fetch` directly, it's been renamed to `__fetch` and will be called behind the scenes.
* Moved the data output step to `to_json` and `to_csv`. This means that you don't need to call `get_output`, it's been removed
* Bugfix: explicitly defined headers were being read as a string instead of being parsed as json first

## v3.1

* Refactored the main library logic into a standalone module that can be imported into other scripts
* The old command line script is now `ditto_cli.py`. `ditto.py` is now the module

## v3.0.4

* Added a `--keep-datatype` argument so that the script doesn't always convert JSON->CSV or CSV->JSON every time. This means that the script now supports cases like "fetch JSON from a URL, filter some fields, then save the output as JSON"

## v3.0.3

* Added support for reading a local config file. You can now skip having to explicitly declare `headers`, `delimiter` and `quotechar` for every execution where any of these differ from the defaults (this is mostly a QoL improvement for fetching from a URL since you'll need to define authorization headers)

## v3.0.2

* Added MVP implementation of fetching from a URL. This MVP version only supports JSON->CSV. HTTP traffic requires the [Requests library](https://requests.readthedocs.io/en/master/).

## v3.0.1

* Decoupled implicit file reading from all conversion methods, e.g. `from_json_file` becomes `to_json`. This is to support a better structure for future functionality to fetch from a URL
* Refactor csv logic to use the built-in Python csv library in both directions. This should finally fix buggy CSV->JSON behaviour in weird fringe cases

## v3.0

* Added `include`, `exclude` and `only` arguments. These replace the old `fields` argument
* Decoupled conversion from/to data formats so that the entire process does not occur in one function, e.g. `json_to_csv` becomes `from_json_file` and `to_csv`

## v2.0

* Renamed project to Ditto
* Refactored codebase to be more streamlined: fewer dependencies, moved all local dependencies to utils folder
* Added example shell snippets for command line execution without needing to be in the root folder
* Misc bugfixes

## v1.2

* Bugfix: missing return statement in json->csv conversion
* Bugfix: wrong param name

## v1.1

* Refactored conversion logic into its own file

## v1.0

* Initial release
