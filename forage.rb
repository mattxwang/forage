require 'optparse' # we use this to parse arguments/parameters
require 'time' # we need this to deal with dates and times
require 'csv' # we need this to read/write CSV files
require 'json' # we need this to read/write JSON files
require 'yaml' # we need this to read/write YAML files
require "net/http" # we need this to make http requests
require "uri" # we need this to make http requests

# Setup Variables

data = Hash.new()
write = false
hydrometric = false

# Parsing Command Line Arguments

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: forage.rb [options]"

  opts.on("-w", "--write TYPE", "Add output type, e.g. json or csv") do |w|
    write = w
  end

  opts.on("-h", "--help", "Get help!") do
    puts "Help coming soon!"
    exit
  end
end.parse!

# Parsing Settings

puts " Opening settings from settings.json ..."

settingsf = File.read('settings.json')
settings = JSON.parse(settingsf)

# Enabling hydrometrics

if (settings["global"]["hydrometric"]["parse"] == "enabled")
  data["hydrometric"] = Hash.new()
  hydrometric = true
end

puts " Settings configured!"

# Fetches Data

puts " Fetching data..."

settings["endpoints"].each do |key, value|
  temp = false
  data["hydrometric"][value["id"]] = []
  if value["type"] == "hydrometric" && hydrometric == true
    url = value["root"] + value["type"] + "/csv/" + value["province"] + "/" + value["timescale"] + "/" + value["province"] + "_" + value["id"] + "_" + value["timescale"] + "_hydrometric.csv"
    uri = URI.parse(url)
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)
    CSV.parse(response.body) do |row|
      if row
        if temp == false
          temp = true
        else
          data["hydrometric"][key].push([value["name"], value["id"], value["timescale"], Time.parse(row[1]).to_i, row[2], row[6]])
        end
      end
    end
  end
end

puts " Data fetched!"

# If CSV is enabled, writes to CSV

if write == "csv" || write == "CSV"
  puts " Writing data to CSV..."
  if hydrometric == true
    CSV.open("output-hydrometric.csv", "wb") do |csv|
      csv << ["Type", "Station Name", "Station ID", "Timescale", "Unix Timestamp", "Water Level (m)", "Discharge (m3/s)"]
      data["hydrometric"].each do |key, value|
        value.each do |k|
          csv << k.unshift("Hydrometric")
        end
      end
    end
  end
  puts " Write to CSV complete!"
end

# If JSON is enabled, writes to JSON

if write == "json" || write == "JSON"
  puts " Writing data to JSON..."
  if hydrometric == true
    File.open("output-hydrometric.json","w") do |f|
      f.write(data.to_json)
    end
  end
  puts " Write to JSON complete!"
end

# If YAML is enabled, writes to YAML

if write == "yaml" || write == "yml" || write == "YAML" || write == "YML"
  puts " Writing data to YAML..."
  if hydrometric == true
    File.open("output-hydrometric.yaml","w") do |f|
      f.write(data.to_yaml)
    end
  end
  puts " Write to YAML complete!"
end


puts " Script complete!"
puts " Shutting down..."
