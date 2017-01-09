# Forage
[![Build Status](https://travis-ci.org/NorvalLabs/forage.svg?branch=master)](https://travis-ci.org/NorvalLabs/forage)

A set of tools to pull and parse information from the [Canadian Government's Weather API](http://dd.weather.gc.ca/), for use with NorvalLabs.

Currently, you'll be able to pull hydrometric data, or things like river flow rates and water levels. You can do so with Python (2.7 and 3+), Ruby, and PHP. Once it pulls the raw data from the API endpoint, it sorts the data, and then outputs it to an easily read format (JSON, CSV, and YAML is supported). Forage scripts work on any system that supports any of our script languages, as long as you have internet! This output is more likely to be easily read by other combined systems, and allows you to locally store the data.

In the future, we're planning to add:
* Javascript Support (node-based)
* Outputted Averages (e.g. average hourly in a day)
* Full YAML Output
* Support scripts
* Support for other Weather Data (e.g. barometric data)

## Support Matrix

| Language | CSV | JSON | YAML | Write Parameter | Linting |  Help |
| --- | --- | --- | --- | --- | --- | --- |
| Python 2.7| To File  | To File  | No | Command Line | NPM-based | WIP |
| Python 3+ | To File  | To File  | No | Command Line | NPM-based | WIP |
| Ruby | To File  | To File  | To File  | Command Line | RubyGems-based | WIP |
| PHP | To File  | To File, Echo  | No | In-file, GET Request | None | None |

*Much more PHP support is coming soon.*

## Build Settings

`settings.json` acts as a settings file for all the build scripts, regardless of language. We include a sample `settings.json` in this project. Here's a look at it:

```json
{
  "global": {
    "hydrometric": {
      "parse" : "enabled"
    }
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

| Property | Description | Accepted Values |
| --- | --- | --- |
| `parse` | Enables processing of x data type. | `enabled` (default), `disabled` |

### Endpoints

Each endpoint has slightly different formats, but the general idea is the same. To add a new endpoint to get/parse, just add a new `endpoint` object.

| Property | Description |
|---|---|
| Key Name | This should be the same as `id`, and is normally the station ID |
| `type` | This should be the type of data collected, as present in the URL (e.g. `hydrometric`) |
| `id` | This should be the same as the key name, and is normally the station ID |
| `province` | The two-letter abbreviation of the province the station is located in |
| `timescale` | The supported timescales for your data type: `hydrometric` supports `hourly` and `daily` |
| `root` | The root site we pull from, for now it should always be `http://dd.weather.gc.ca/` |

## File Outputs

All files are outputted to `output-DATA-TYPE.FILE-TYPE`, unless specifically specified.

## Python

*Note: this script requires [Python 2.7 OR 3](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/). Please install these if you do not already have them!*

In order to use the python script, we first need to get our dependencies:

```
pip install -r pip-requirements.txt
```

Then, just run our script!

```
python forage.py
```

You can use the script parameters with `forage.py` (if you don't, it doesn't output anything). For example:

```
python forage.py -w json
```

If you're running python 3, you might have to use the `python3` and `pip3` commands on the `forage-py3.py` file. Other than that, everything should work!

## Ruby

*Note: this script requires [Ruby 2+](https://www.ruby-lang.org/en/), and optionally [Bundle](http://bundler.io/) for linting.*

In order to use the ruby script, simply run it from the command line.

```
ruby forage.rb
```

You can use the script parameters with `forage.rb` (if you don't, it doesn't output anything). For example:

```
ruby forage.rb -w csv
```

To use optional linting gems, first install them with bundle:

```
bundle
```

Then, use either the `csvlint`, `jsonlint`, or `yamllint` commands.

```
csvlint output-hydrometric.csv

jsonlint output.hydrometric.json

yamllint output.hydrometric.yaml
```

## PHP

*Note: this PHP file was tested on PHP 5.6.10. More information on supported versions will come soon.*

Our PHP project isn't command line; instead, the `forage.php` file is a viewable or importable PHP file that currently runs forage on view. Parameters are stored as variables in the file.

So, in essence, grab a [LAMP](https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-14-04) or [MAMP](https://www.mamp.info/en/) setup, and visit the `forage.php` file in your browser.

There are three ways to configure the `forage.php` file: `settings.json`, in-file, or through a `GET` request. The first two are relatively self-explanatory, and already documented in this README.

`GET` requests have two (optional) parameters (that default to `false`):
* `echo`, which determines what type of information is echoed to the page (very handy for AJAX requests)
* `write`, which determines what type of information is written to the file

## Team

This script was developed by Matthew Wang (@malsf21), who's part of the Norval Labs team.
