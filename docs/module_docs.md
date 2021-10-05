# Shapeshifter as a module

Use shapeshifter.py as an import in your project

## Quickstart

For advanced use, import the shapeshifter.py module into your own code.

Basic import & JSON->CSV example:

```python
from shapeshifter import Shapeshifter

instance = Shapeshifter()

data_source = "~/localdir/source.json"

result = instance.from_json(data_source).to_csv()
```

Basic CSV filtering plus field modification:

```python
result = instance.from_csv(data_source).include("spam", "ham").exclude("eggs").to_csv()
```

Basic JSON->CSV conversion plus field modification, also take snapshots of the data:

```python
instance.from_json(data_source)
result_after_include = instance.include("spam", "ham").to_csv()
result_after_exclude = instance.exclude("eggs").to_csv()
```

## Documentation

### Method chaining

Most methods in the Shapeshifter object returns the instance reference. This allows method calls to be chained until it hits an output call, which will return the output in the corresponding format.

The methods which can be chained:

* `from_json`
* `from_csv`
* `include`
* `exclude`
* `only`

The methods which do not chain:

* `to_json`
* `to_csv`
* `get_source`

### Fetching from the data source

Fetching data from the source happens in `__fetch`. which is implicitly called when `from_json` or `from_csv` gets called. These methods will attempt to dynamically interpret the data source: if the data source starts with `http://` or `https://` then it will assume it is a web URL, otherwise it will try reading from a local file.

### Data snapshots

When Shapeshifter successfully fetches data from the source, it is stored to a snapshot and subsequent calls that modify the data does not affect the snapshot. This allows you to compare your input and output if necessary. The the original snapshot can be accessed via the `get_source` method.

### Defining config settings

If there are no config values passed into the constructor then Shapeshifter will use default settings for `headers`, `delimiter` and `quotechar`. To overwrite these settings, define them when constructing a new instance.

### Modifying the output with include, exclude and only arguments

#### include

The `include` method expects string arguments which defines fields which will always be included in the output.

This can be useful if your data source is e.g. a NoSQL database forwarding data to a API which returns JSON. Since the data source is NoSQL, the field you're looking for may not even be there, and if the REST API doesn't handle this, then you'd need to do it yourself. If you need your output in CSV, you'll want your output to have the same fields on all entries so --include will cover this case.

#### exclude

The `exclude` method expects string arguments which defines fields which will always be excluded in the output.

If your data source is unnecessarily verbose for your purpose, use the --exclude argument to strip specific fields out of the output. This can support scenarios when your data source has variable structure, but you also know there are specific fields you do not want in the output.

#### only

The `only` method expects string arguments which defines the fields which will be the only fields in the output.

Just like the exclude case, if your data source is unnecessarily verbose for your purpose you may want to remove some fields. There may be some more extreme cases like getting a raw dump of a 20 column table filled with stuff you have no clue about when you only need two fields. In this scenario you can use the --only argument to strip out everything else.
