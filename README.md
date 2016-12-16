# Forage
[![Build Status](https://travis-ci.org/NorvalLabs/forage.svg?branch=master)](https://travis-ci.org/NorvalLabs/forage)

A set of tools to pull information from the [Canadian Government's Weather API](http://dd.weather.gc.ca/), with support for the hydrometric data for now. Support for more data is coming soon!

## Settings

`settings.json` acts as a settings file for all the build scripts, regardless of language. Let's see how it works:

```json
{
  "global": {
    "hydrometric": "enabled"
  },
  "endpoints": {
    "02HB025": {
      "type" : "hydrometric",
      "name": "Credit River at Norval",
      "id": "02HB025",
      "province": "ON",
      "timescale": "daily",
      "root": "http://dd.weather.gc.ca/"
    },
    "02HB008": {
      "type" : "hydrometric",
      "name": "Credit River West Branch at Norval",
      "id": "02HB008",
      "province": "ON",
      "timescale": "hourly",
      "root": "http://dd.weather.gc.ca/"
    }
  }
}
```

### Global Settings

The `global` object defines some global settings. You should not have to add or remove any key/value pairs from `global`, just modifying the values.
* For every type of data you want to get and parse, switch the value for that type to `"enabled"`. If not, switch it to `"disabled"`. e.g. `"hydrometric": "enabled"`  gets and parses hydrometric data, while `"hydrometric": "disabled"` does not

### Endpoints

Each endpoint has slightly different formats, but the general idea is the same. To add a new endpoint to get/parse, just add a new `endpoint` object. It consists of:

* Key Name: this should be the same as `id`, and is normally the station ID
* `type`: this should be the type of data collected, as present in the URL (e.g. `hydrometric`)
* `id`: this should be the same as the key name, and is normally the station ID
* `province`: the Province the station is located in
* `timescale`: the supported timescales for your data type: `hydrometric` supports `hourly` and `daily`
* `root`: the root site we pull from, for now it should always be `http://dd.weather.gc.ca/`

## Python

*Note: this installation process requires [pip](https://pip.pypa.io/en/stable/). Please install it if you do not already have it!*

In order to use the python script, we first need to get our dependencies:

```
pip install -r pip-requirements.txt
```

Then, just run our script!

```
python forage.py
```

But, running the script just pulls the data, and doesn't output it. Luckily, the script takes parameters!

The script takes two parameters:
* `-w` or `--write`
  * Parameter of what file type to write
  * Default is none (no file will be written)
  * Accepts `csv` or `json`
  * The outputted file(s) is at `API-output.FILETYPE`
  * Example: `python forage.py -w csv`
* `-h` or `--help`
  * Displays help commands (coming soon)

And, it also uses `settings.json` to know what to get: look above on documentation on how to use it!
