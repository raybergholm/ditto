# Roadmap for future development

## Bigger things

* ~~Currently this requires a file source for everything, which requires a lot of needless copying of data from remote APIs. Why not support fetch directly from the API too? (This will require defining auth headers and all that web traffic stuff)~~ added in v3.2
* ~~Currently this works entirely as a self-contained command line script, but most of the logic can be turned into a module which could be imported as a library in itself~~ added in v3.5
* This supports JSON and CSV right now. How about other data types?

## Smaller things

* --include currently causes some annoying key reordering due to the use of `destination = {**extra_fields, **source}`, could be smoother to append to the end instead
* How about being able to define a set field order or structure? Probably makes sense to use the data source as a template.
