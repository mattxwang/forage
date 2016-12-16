# Forage
A set of tools to pull information from the many APIs we plan to use. For now, we just have a little python script that pulls information from the [Canadian Government's Hydrometric API](http://dd.weather.gc.ca/hydrometric/).

## Python

In order to use the python script, we first need to get our dependencies:

```
pip install -r pip-requirements.txt
```

Then, just run our script!

```
python forage.py
```

The script takes two parameters:
* `-w` or `--write`
  * Parameter of what file type to write
  * Default is none (no file will be written)
  * Accepts `csv` or `json`
  * The outputted file(s) is at `API-output.FILETYPE`
  * Example: `python forage.py -w csv`
* `-h` or `--help`
  * Displays help commands (coming soon)
