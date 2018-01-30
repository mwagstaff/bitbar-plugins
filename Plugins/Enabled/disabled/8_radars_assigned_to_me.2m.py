#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pre-requisites:
#
# (1) You must have an application password Keychain entry set as follows:
#  - Name: apple_connect
#  - Account: <Your Apple Connect userrname>
#  - Password: <Your Apple Connect password>
#
# These login credentials will be used to authenticate your Radar access
#
# (2) You also need a script that retrieves the relevant Radar problems
# in JSON format, and takes the JSON query as its only parameter.
#
# Set the SCRIPT_PATH_FIND_PROBLEMS variable below to the path
# of this script.
#
# (3) Finally, ensure that you set your DSID below.

import json, os, os.path, re, sys
from subprocess import check_output, STDOUT, CalledProcessError

# Use UTF-8 encoding to enable emoji support
reload(sys)
sys.setdefaultencoding('utf8')


# This must be set to your DSID (person ID in Apple Directory)
DSID = 973574794


# These are the status icons displayed for each Radar in the dropdown
# Radars are considered "bad" if they have no milestone or priority set
RADAR_STATUS_INDICATOR_GOOD = "⚫"
RADAR_STATUS_INDICATOR_BAD = "🔴"

# This is the text color displayed by the menubar icon, depending on
# whether any "bad" radars exist or not
RADAR_SUMMARY_TEXT_COLOR_GOOD = "black"
RADAR_SUMMARY_TEXT_COLOR_BAD = "red"


KEYCHAIN_APPLE_CONNECT_LOGIN_CREDS = "apple_connect"
SCRIPT_PATH_FIND_PROBLEMS = "~/Projects/radar-api-tools/scripts/lib/findProblems.sh"
SCRIPT_MAX_TIMEOUT = 3
TEMP_DATA_OUTPUT_FILEPATH = "/tmp/findProblemsAssigned_Output.json"
TEMP_ERROR_FILEPATH = '/tmp/bitbar_radars_assigned_to_me.err'

JSON_FIND_PROBLEMS_QUERY = {
  "assignee" : DSID,
  "state" : [
    "New Problem",
    "Analyze",
    "Integrate",
    "Build",
    "Verify"
  ]
}


def main():

  if not os.path.isfile( TEMP_ERROR_FILEPATH ):

    # Get the login credentials from the keychain entry
    keychainOutput = getKeyChainOutput(KEYCHAIN_APPLE_CONNECT_LOGIN_CREDS)
    appleConnectUsername = getUsername(keychainOutput)
    appleConnectPassword = getPassword(keychainOutput)

    # Get the data, and print the summary
    getData(appleConnectUsername, appleConnectPassword, JSON_FIND_PROBLEMS_QUERY, SCRIPT_PATH_FIND_PROBLEMS, TEMP_DATA_OUTPUT_FILEPATH)
    printOutput()

  else:
    printErrorOutput()


def getKeyChainOutput(keychainEntry):
  cmd = [
    'security',
    'find-generic-password',
    '-l',
    keychainEntry,
    '-g'
  ]
  try:
    return check_output(cmd, stderr=STDOUT)
  except CalledProcessError:
    raise SystemExit("Error: Unable to retrieve \"apple_connect\" keychain entry")


def getUsername(keychainOutput):
  findUsername = re.compile('"acct"<blob>="([^"]+)"').search
  return findKey(findUsername, keychainOutput)


def getPassword(keychainOutput):
  findPassword = re.compile('password: "([^"]+)"').search
  return findKey(findPassword, keychainOutput)


def findKey(fn, out):
  match = fn(out)
  return match and match.group(1)


def getData(appleConnectUsername, appleConnectPassword, json_query, script_path, output_path):
  cmdGetData = "export AppleConnect_Username='{}' && export AppleConnect_Password='{}' && {} \"{}\" 2>/dev/null > {} & sleep {} ; kill $!".format(
      appleConnectUsername,
      appleConnectPassword,
      script_path,
      str(json_query),
      output_path,
      SCRIPT_MAX_TIMEOUT
    )

  os.system(cmdGetData)

def printOutput():

  # Try and load the radars JSON
  with open( TEMP_DATA_OUTPUT_FILEPATH ) as radars_data_raw:
    try:
      radars = json.load( radars_data_raw )

    except:
      radars = None

  # If we haven't got a list, we've got a problem with the data
  # Write the error to a temporary file so that if it's a credentials issue,
  # we don't keep on retrying and cause the account to become disabled
  if not isinstance( radars, (frozenset, list, set, tuple) ):

    f = open( TEMP_ERROR_FILEPATH, 'w' )
    f.write( str ( radars_data_raw ) )
    f.close()

    printErrorOutput()

  for radar in radars:
    if radar["milestone"] is None:
      radar["milestone"] = { "name" : "No milestone" }

  # Sort by ID
  # radars = sorted( radars, key=lambda k: ( k["milestone"]["name"], k["id"] ), reverse = False )
  radars = sorted( radars, key=lambda k: k["id"], reverse = True )

  radarSummaryTextColor = RADAR_SUMMARY_TEXT_COLOR_GOOD
  radarDropDownTextShortTerm = ""
  radarDropDownTextLongTerm = ""

  radarCountShortTerm = 0
  radarCountLongTerm = 0

  # Iterate through the radars, and print out the summary line for each
  for radar in radars:

    radarId = str( radar["id"] )
    radarTitle = str( radar["title"] )


    radarIssues = getRadarIssues(radar)

    if len(radarIssues) > 0:
      radarStatusIndicator = RADAR_STATUS_INDICATOR_BAD
      radarSummaryTextColor = RADAR_SUMMARY_TEXT_COLOR_BAD
    else:
      radarStatusIndicator = RADAR_STATUS_INDICATOR_GOOD

    radarTextMilestoneInfo = radar["milestone"]["name"]
    radarTextIssues = getRadarTextIssues(radarIssues)

    # Set the dropdown entries, one containing the basic info, and an "alternate"
    # line with more info that's only displayed if the user holds down the "alt" key
    radarTextBasicInfo = radarStatusIndicator + " " + radarId + " - " + radarTextMilestoneInfo + ": " + radarTitle + radarTextIssues
    radarDropDownText = radarTextBasicInfo + getRadarTextUrl(radarId) + "\n"
    radarDropDownText += getRadarTextAlternate(radar, radarTextBasicInfo) + getRadarTextUrl(radarId) + "\n"

    # Work out if it's a long or short term radar
    if isRadarLongTerm(radar):
      radarCountLongTerm += 1
      radarDropDownTextLongTerm += radarDropDownText
    else:
      radarCountShortTerm += 1
      radarDropDownTextShortTerm += radarDropDownText



  # Print the number of short term and long term radars in the menu bar
  print "🎯 {} | color={}".format( str( len(radars) ), radarSummaryTextColor )
  print "---"

  # Print dropdown top line summary
  print "🔄 {} short term radar(s), {} long term (\"Future\" or \"A galaxy far far away\"). Hold alt to see more detail, or click to refresh. | refresh=true".format( str(radarCountShortTerm), str(radarCountLongTerm) )

  # Print short term radars first in dropdown
  print "---"
  if radarCountShortTerm > 0:
    print radarDropDownTextShortTerm
  else:
    print "No short term radars (where the milestone contains anything other than \"Future\" or \"A galaxy far far away\")"

  # Then print the long term radars
  print "---"
  if radarCountLongTerm > 0:
    print radarDropDownTextLongTerm
  else:
    print "No long term radars (where the milestone contains \"Future\" or \"A galaxy far far away\")"


def isRadarLongTerm(radar):

  if "Future" in radar["milestone"]["name"] or radar["milestone"]["name"] == "A galaxy far far away":
    return True


def getRadarTextUrl(radarId):
  return " | href=rdar://problem/" + radarId


def getRadarIssues(radar):

  radarIssues = []

  if radar["milestone"]["name"] == "No milestone":
    radarIssues.append("milestone not set")

  if radar["priority"] == 5:
    radarIssues.append("priority not set")

  return radarIssues


def getRadarTextIssues(radarIssues):

  radarTextIssues = ""
  for issue in radarIssues:
    radarTextIssues += " (" if len(radarTextIssues) == 0 else ", "
    radarTextIssues += issue
  radarTextIssues += ")" if len(radarTextIssues) > 0 else ""

  return radarTextIssues


def getRadarTextAlternate(radar, radarTextBasicInfo):

  radarTextAlternate = radar["component"]["name"] + " - " + radar["component"]["version"] + " - " + radar["classification"] + " - " + radar["lastModifiedAt"]

  return radarTextBasicInfo + " - " + radarTextAlternate + " | alternate=true"


def printErrorOutput():

  print RADAR_STATUS_INDICATOR_BAD
  print "---"
  print "Unable to read Radar data from " + TEMP_DATA_OUTPUT_FILEPATH
  print "---"
  with open(TEMP_DATA_OUTPUT_FILEPATH, 'r') as fin:
      print fin.read()
  print "---"
  print "Remove the error lock file (have you checked your apple_connect Keychain entry?) | bash=\"rm " + TEMP_ERROR_FILEPATH + " && exit \" "
  sys.exit(1)

main()