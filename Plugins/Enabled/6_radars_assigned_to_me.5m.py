#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pre-requisites:
#
# You need a script that sets the following environment variables
#  (1) AppleConnect_Username
#  (2) AppleConnect_Password
#
# It is recommended that this script extracts the credentials in
# a secure manner, e.g. from Keychain
#
# Set the SCRIPT_PATH_SET_LOGIN_CREDS variable below to the path
# of this script.

# You also need a script that retrieves the relevant Radar problems
# in JSON format, and takes the JSON query as its only parameter.
#
# Set the SCRIPT_PATH_FIND_PROBLEMS variable below to the path
# of this script.
#
# Finally, ensure that you set your DSID below.

import json, os, sys

# Use UTF-8 encoding to enable emoji support
reload(sys)
sys.setdefaultencoding('utf8')


DSID = 973574794

SCRIPT_PATH_SET_LOGIN_CREDS = "~/bin/Scripts/setLoginCredentials.sh"
SCRIPT_PATH_FIND_PROBLEMS = "~/Projects/radar-api-tools/scripts/lib/findProblems.sh"
TEMP_DATA_OUTPUT_FILEPATH = "/tmp/findProblemsAssigned_Output.json"


def main():

  json_query = {
    "assignee" : DSID,
    "state" : [
      "New Problem",
      "Analyze",
      "Integrate",
      "Build",
      "Verify"
    ]
  }

  os.system ( 'bash -c \"source '  + SCRIPT_PATH_SET_LOGIN_CREDS + ' && ' + SCRIPT_PATH_FIND_PROBLEMS + ' \\\"' + str(json_query) + '\\\" 2>/dev/null > ' + TEMP_DATA_OUTPUT_FILEPATH + "\"" )
  printSummary()


def printSummary():

  # Load the radars JSON
  with open( TEMP_DATA_OUTPUT_FILEPATH ) as radars_data_raw:
    radars = json.load( radars_data_raw )

  # Sort by ID
  radars = sorted( radars, key=lambda k: k["id"], reverse=True )

  # Print the number of radars in the menu bar
  print "🎯 " + str( len(radars) )
  print "---"

  # Iterate through the radars, and print out the summary line for each
  for radar in radars:
    
    radarId = str( radar["id"] )
    radarTitle = str( radar["title"] )

    if radar["milestone"] and radar["milestone"]["name"]:
      milestoneName = radar["milestone"]["name"]
      if milestoneName == "Future":
        radarInfoPrefix = "⬇️"
      else:
        radarInfoPrefix = "⚫"
      radarInfoSuffix = "(" + radar["milestone"]["name"] + ")"

    else:
      radarInfoPrefix = "⚠️"
      radarInfoSuffix = "(no milestone)"

    print radarInfoPrefix + " " + radarId + ": " + radarTitle + " " + radarInfoSuffix + " | href=rdar://problem/" + radarId

main()