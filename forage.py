import sys # this lets us receive passed arguments in the command line
import getopt # this lets us receive arguments and options in the command line
import json # this lets us parse JSON files
import csv # this lets us parse CSV files
import dateutil.parser # this helps us parse dates
import calendar # this helps us understand dates
import requests # this helps us make good HTTP requests
from contextlib import closing # this helps us make good HTTP requests

output = {}
data = {}
write = False
hydrometric = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 'w:p:h', ['write=', 'help'])
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

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

if (settings["global"]["hydrometric"] == "enabled"):
    output["hydrometric"] = {}
    data["hydrometric"]= {}
    hydrometric = True

for endpoint in settings["endpoints"]:
    if (settings["endpoints"][endpoint]["type"] == "hydrometric" and hydrometric == True):
        endpoint = settings["endpoints"][endpoint]
        output["hydrometric"][endpoint["id"]] = []
        url = endpoint["root"] + endpoint["province"] + "/" + endpoint["timescale"] + "/" + endpoint["province"] + "_" + endpoint["id"] + "_" + endpoint["timescale"] + "_hydrometric.csv"
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(r.iter_lines(), delimiter=',', quotechar='"')
            for row in reader:
                output["hydrometric"][endpoint["id"]].append(row)
        output["hydrometric"][endpoint["id"]] = output["hydrometric"][endpoint["id"]][1:]
if (hydrometric == True):
    for dataset in output["hydrometric"]:
        data["hydrometric"][dataset] = []
        for i in range(len(output["hydrometric"][dataset])):
            row = output["hydrometric"][dataset][i]
            if (row):
                data["hydrometric"][dataset].append([settings["endpoints"][row[0]]["timescale"], settings["endpoints"][row[0]]["name"], row[0], calendar.timegm(dateutil.parser.parse(row[1]).utctimetuple()), row[2], row[6]])

if (write == "csv" or write == "CSV"):
    if (hydrometric == True):
        with open('output-hydrometric.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Type", "Timescale", "Station Name", "Station ID", "Unix Timestamp", "Water Level (m)", "Discharge (m3/s)"])
            for dataset in data["hydrometric"]:
                for i in range(len(data["hydrometric"][dataset])):
                    row = data["hydrometric"][dataset][i]
                    if (row):
                        writer.writerow(["Hydrometric"] + row)

elif (write == "json" or write == "JSON"):
    if (hydrometric == True):
        with open('output-hydrometric.json', 'w') as outfile:
            json.dump(data, outfile)
# Coming soon: YAML support!
# elif (write == "yaml" or "YAML"):
#     if (hydrometric == True):
#         with open('output-hydrometric.yml', 'w') as outfile:
#             yaml.dump(data, outfile, default_flow_style=True)
