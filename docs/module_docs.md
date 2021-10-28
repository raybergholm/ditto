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

Convert JSON->CSV and filter based on a field value

```python
result = instance.from_json(data_source).filter("meaningoflife", "==", 42).to_csv()
```

## Documentation

### Method chaining

Most methods in the Shapeshifter object return the instance reference. This allows method calls to be chained until it hits an output call, which will return the output in the corresponding format.

The methods which can be chained:

* `from_json`
* `from_csv`
* `include`
* `exclude`
* `only`
* `filter`

The methods which do not chain:

* `to_json`
* `to_csv`
* `get_source`

### Fetching from the data source

Fetching data from the source happens in `__fetch`. which is implicitly called when `from_json` or `from_csv` gets called. These methods will attempt to dynamically interpret the data source: if the data source starts with `http://` or `https://` then it will assume it is a web URL, otherwise it will try reading from a local file.

#### Fetching from a web URL with paging

When reading from a web URL, some endpoints might have have a lot of data, maybe even too much for it to transmit in a single request. If it has paging implemented then use the paging feature to specify the name of the query param that corresponds to the page number, plus the min & max range.

Paging can be turned on by supplying values to the paging parameter in the constructor. This expects a dictionary in the example format:

```python
{
  "iterator": "page",
  "min": 0,
  "max": 100
}
```

The shapeshifter instance will not try to calculate anything for you so it's up to you to supply valid min and max ranges.

### Data snapshots

When Shapeshifter successfully fetches data from the source, it is stored to a snapshot and subsequent calls that modify the data does not affect the snapshot. This allows you to compare your input and output if necessary. The original snapshot can be accessed via the `get_source` method.

### Defining config settings

If there are no config values passed into the constructor then Shapeshifter will use default settings for `headers`, `delimiter` and `quotechar`. To overwrite these settings, define them when constructing a new instance.

### Modifying the output with include, exclude and only arguments

#### include fields

The `include` method expects string arguments which defines fields which will always be included in the output.

This can be useful if your data source is e.g. a NoSQL database forwarding data to a API which returns JSON. Since the data source is NoSQL, the field you're looking for may not even be there, and if the REST API doesn't handle this, then you'd need to do it yourself. If you need your output in CSV, you'll want your output to have the same fields on all entries so --include will cover this case.

#### exclude fields

The `exclude` method expects string arguments which defines fields which will always be excluded in the output.

If your data source is unnecessarily verbose for your purpose, use the --exclude argument to strip specific fields out of the output. This can support scenarios when your data source has variable structure, but you also know there are specific fields you do not want in the output.

#### only fields

The `only` method expects string arguments which defines the fields which will be the only fields in the output.

Just like the exclude case, if your data source is unnecessarily verbose for your purpose you may want to remove some fields. There may be some more extreme cases like getting a raw dump of a 20 column table filled with stuff you have no clue about when you only need two fields. In this scenario you can use the --only argument to strip out everything else.

### Filtering the output based on field values

The `filter` method accepts field, operator and value parameters. Note that if the field does not exist in an entry, that entry will be filtered out too.

This method lets you perform some basic data filtering by making calls like:
`filter("meaningoflife", "==", 42)`
`filter("powerlevel", ">", 9000)`
`filter("firstname", "<=", "Monty")`

## Methods

### `__init__`

Method signature:

`__init__(config={}, delimiter=DEFAULT_CSV_DELIMITER, quotechar=DEFAULT_CSV_QUOTECHAR, headers=DEFAULT_HEADERS, paging=None)` => `self`

Examples:

```python

```

### `from_json`

Method signature:

`from_json(source)` => `self`

Examples:

```python

```

### `from_csv`

Method signature:

`from_csv(source)` => `self`

Examples:

```python

```

### `to_json`

Method signature:

`to_json()` => `String`

Examples:

```python

```

### `to_csv`

Method signature:

`to_csv()` => `String`

Examples:

```python

```

### `get_source`

Method signature:

`get_source()` => `List`

Examples:

```python

```

### `include`

Method signature:

`include(*varargs)` => `self`

Examples:

```python

```

### `exclude`

Method signature:

`exclude(*varargs)` => `self`

Examples:

```python

```

### `only`

Method signature:

`only(*varargs)` => `self`

Examples:

```python

```

### `filter`

Method signature:

`filter(field, operator, value)` => `self`

Examples:

```python

```
