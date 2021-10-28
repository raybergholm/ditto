# Roadmap for future development

## Bigger things

* ~~Currently this requires a file source for everything, which requires a lot of needless copying of data from remote APIs. Why not support fetch directly from the API too? (This will require defining auth headers and all that web traffic stuff)~~ added in v3.2
* ~~Currently this works entirely as a self-contained command line script, but most of the logic can be turned into a module which could be imported as a library in itself~~ added in v3.5
* ~~The include/exclude/only methods only care about which fields are included/dropped, but sometimes you need to filter based on the value of a field. Some basic support could help.~~ added in v4.1
* ~~When fetching from a web URL, sometimes the full dataset is large enough that it times out. There's paging available on the endpoint, but Shapeshifter only supports a single call right now.~~ added in v4.1

* This supports JSON and CSV right now. How about other data types?
* Because this was originally a barebones JSON->CSV/CSV->JSON parser, all JSON sources are implicitly expected to yield a list of objects like `[{{"id": 1},{"id": 2}}]` and that assumption remains to this day. This means that there's no handling for anything else like `{"listIsHere": [{{"id": 1},{"id": 2}}], "metadata": "blah"}`. It would be great to handle this case too, so that it's possible to fetch directly from this sort of data format. This will probably need some new argument or parameter to determine where/how to slice the subset out of the source

## Smaller things

* ~~`include()`, `exclude()` and `only()` all require a list as a parameter, but it's nicer to use varargs~~ added in v4.0

* --include currently causes some annoying key reordering due to the use of `destination = {**extra_fields, **source}`, could be smoother to append to the end instead
* How about being able to define a set field order or structure? Probably makes sense to use the data source as a template.
