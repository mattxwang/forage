# importing libraries

import sys # this lets us receive passed arguments in the command line
import getopt # this lets us receive arguments and options in the command line
import json # this lets us parse JSON files
import csv # this lets us parse CSV files
import dateutil.parser # this helps us parse dates
import calendar # this helps us understand dates
import requests # this helps us make good HTTP requests
from contextlib import closing # this helps us make good HTTP requests

# Setting a few variables

output = {}
data = {}
write = False
hydrometric = False

# Here, we get the arguments and parameters passed to our script, and do things accordingly!

try:
    opts, args = getopt.getopt(sys.argv[1:], 'w:h', ['write=', 'help'])
except getopt.GetoptError:
    print "Uh oh, something went wrong. Try again, and read the docs! Use forage.py -h if you need help."
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print "Help docs coming soon!"
        sys.exit(2)
    elif opt in ('-w', '--write'):
        write = arg
    else:
        print "Uh oh, something went wrong. Try again, and read the docs! Use forage.py -h if you need help."
        sys.exit(2)

# Coming soon!
# if (write == "yaml" or "YAML"):
#     import yaml

print " Opening settings from settings.json ..."

# We open settings.json and load it to settings

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

# This enables hydrometrics

if (settings["global"]["hydrometric"]["parse"] == "enabled"):
    output["hydrometric"] = {}
    data["hydrometric"]= {}
    hydrometric = True

print " Settings configured!"

print " Fetching data..."

# This iterates through all endpoints and fetches the data.

for endpoint in settings["endpoints"]:
    if (settings["endpoints"][endpoint]["type"] == "hydrometric" and hydrometric == True):
        endpoint = settings["endpoints"][endpoint]
        data["hydrometric"][endpoint["id"]] = []
        url = endpoint["root"] + endpoint["type"] + "/csv/" + endpoint["province"] + "/" + endpoint["timescale"] + "/" + endpoint["province"] + "_" + endpoint["id"] + "_" + endpoint["timescale"] + "_hydrometric.csv"
        with closing(requests.get(url, stream=True)) as r:
            lines = r.iter_lines()
            reader = csv.reader(lines, delimiter=',', quotechar='"')
            temp = False
            for row in reader:
                if (temp == False):
                    temp = True
                elif (row):
                    data["hydrometric"][endpoint["id"]].append([settings["endpoints"][endpoint["id"]]["name"], endpoint["id"], settings["endpoints"][endpoint["id"]]["timescale"], calendar.timegm(dateutil.parser.parse(row[1]).utctimetuple()), row[2], row[6]])

print " Data fetched!"

# If the write type is CSV, this function outputs to a CSV file called output-hydrometric.csv

if (write == "csv" or write == "CSV"):
    print " Writing data to CSV..."
    if (hydrometric == True):
        with open('output-hydrometric.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Type", "Station Name", "Station ID", "Timescale", "Unix Timestamp", "Water Level (m)", "Discharge (m3/s)"])
            for dataset in data["hydrometric"]:
                for i in range(len(data["hydrometric"][dataset])):
                    row = data["hydrometric"][dataset][i]
                    if (row):
                        writer.writerow(["Hydrometric"] + row)
    print " Write to CSV complete!"

# If the write type is JSON, this function outputs to a JSON file called output-hydrometric.json

elif (write == "json" or write == "JSON"):
    print " Writing data to JSON..."
    if (hydrometric == True):
        with open('output-hydrometric.json', 'w') as outfile:
            json.dump(data, outfile)
    print " Write to JSON complete!"
# Coming soon: YAML support!
# elif (write == "yaml" or "YAML"):
#     if (hydrometric == True):
#         with open('output-hydrometric.yml', 'w') as outfile:
#             yaml.dump(data, outfile, default_flow_style=True)
print " Script complete!"
print " Shutting down..."
