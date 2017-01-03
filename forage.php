<?php
  $hydrometric = false;
  $write = false;
  $data = [];

  // First, we're going to import the settings.json.
  $settings = json_decode(file_get_contents("settings.json"), true);
  if ($settings["global"]["hydrometric"]["parse"] == "enabled"){
    $hydrometric = true;
  }

  // Now, we're going to fetch the data.
  foreach ($settings["endpoints"] as $k => $v) { // Iterates through each endpoint
    $temp = false;
    if ($settings["endpoints"][$k]["type"] == "hydrometric" and $hydrometric = true){
      $data["hydrometric"][$k] = []; // Initializing an empty array
      $url = $v["root"] . $v["type"] . "/csv/" . $v["province"] . "/" . $v["timescale"] . "/" . $v["province"] . "_" . $v["id"] . "_" . $v["timescale"] . "_hydrometric.csv"; // Generating the URL from the settings
      $response = file_get_contents($url); // Getting the URL's content, in a string
      $parsed = str_getcsv($response, "\n"); // Parsing the string into an array, with each element containing a CSV row
      foreach ($parsed as $kr => $vr) {
        if ($temp == false){ // skips over header row
          $temp = true;
        }
        else{
          $vr_parsed = str_getcsv($vr); // Now, we parse the CSV row into an actual array
          array_push($data["hydrometric"][$k], [$v["name"], $v["id"], $v["timescale"], strtotime($vr_parsed[1]), $vr_parsed[2], $vr_parsed[6]]); // Formats the array to our liking
        }
      }
    }
  }

  // Now, we perform some write checks.

  if ($write == "csv" or $write == "CSV"){ // Writing to CSV
    if ($hydrometric == true){
      $writefile = fopen('output-hydrometric.csv', 'w');
      fputcsv($writefile, ["Type", "Station Name", "Station ID", "Timescale", "Unix Timestamp", "Water Level (m)", "Discharge (m3/s)"]);
      foreach ($data["hydrometric"] as $k => $v){
        foreach ($v as $o) {
          array_unshift($o, "Hydrometric");
          fputcsv($writefile, $o);
        }
      }
      fclose($writefile);
    }
  }

  elseif ($write == "json" or $write == "JSON"){ // Writing to JSON
    if ($hydrometric == true){
      file_put_contents('output-hydrometric.json', json_encode($data));
    }
  }
