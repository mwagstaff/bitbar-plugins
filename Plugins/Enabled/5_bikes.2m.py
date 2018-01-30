#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import threading
import urllib2

from pprint import pprint

APP_ID = 'd9bb486e'
APP_KEY = '63ab1eedebbebb832fd43130521e173c'

bikeData = []

# Define the array of bikePoint data to retrieve
bikePoints = [ 542, 552, 449, 229, 276, 354, 587, 811, 570, 532, 480 ]


def main():

  # Get the bike data asynchronously

  threads = [ threading.Thread ( target=populateBikeData, args=( bikePoint,) ) for bikePoint in bikePoints ]
  for thread in threads:
      thread.start()
  for thread in threads:
      thread.join()


  # Once we have the data, print out the summaries

  printSummary('🚲', 542, '')  # Salmon Lane, Limehouse
  print "---"
  printSummary('🏠', 542)  # Salmon Lane, Limehouse
  printSummary('🏠', 480)  # Flamborough Street, Limehouse
  print "---"
  printSummary('🏠', 552)  # Watney Street, Shadwell
  printSummary('🏠', 449)  # Shadwell Station, Shadwell
  print "---"
  printSummary('🏢', 229)  # Whitehall Place, Strand
  printSummary('🏢', 354)  # Northumberland Avenue, Strand
  print "---"
  printSummary('🏦', 587)  # Monument Street, Monument
  printSummary('🏦', 276)  # Lower Thames Street, Monument
  print "---"
  printSummary('🛳', 811)  # Westferry Circus, Canary Wharf
  printSummary('🛳', 570)  # Upper Bank Street, Canary Wharf
  printSummary('🛳', 532)  # Jubilee Plaza, Canary Wharf


def populateBikeData(bikePoint):

  retriesRemaining = 2

  while retriesRemaining > 0:

    retriesRemaining -= 1

    try:
      page = urllib2.urlopen( 'https://api.tfl.gov.uk/BikePoint/BikePoints_{}?app_id={}&app_key={}'.format( bikePoint, APP_ID, APP_KEY ), timeout = 5 )
      data = json.load(page)
      props = data['additionalProperties']

      bikePointData = {
        "bikePoint" : bikePoint,
        "name" : data['commonName'],
        "bikes" : getBikes(props),
        "emptyDocks" : getEmptyDocks(props)
      }

      bikeData.append( bikePointData )

    except:
      pass


def printSummary(icon, bikePoint, name = None):

  for bikePointData in bikeData:

    if bikePointData['bikePoint'] == bikePoint:

      if icon is None:
        icon = ''

      if name is None:
        name = bikePointData['name']

      bikes = int( bikePointData['bikes'] )
      emptyDocks = int( bikePointData['emptyDocks'] )

      formatting = getFormatting( bikes, emptyDocks )

      print '{} {}/{} {} {}'.format( icon, str( bikes ), str ( emptyDocks ), name, formatting )

      return

  print "🚳 Uh oh, data for bikepoint {} not found".format( bikePoint )


def getFormatting(bikes, emptyDocks):

  if bikes < 3:
    return '| color=red'

  elif bikes < 5:
    return '| color=orange'

  elif emptyDocks < 3:
    return '| color=red'

  elif emptyDocks < 5:
    return '| color=orange'

  else:
    return '| color=green'


def getBikes(props):

  for prop in props :

    if prop['key'] == 'NbBikes' :
      return prop['value']


def getEmptyDocks(props):

  for prop in props :

    if prop['key'] == 'NbEmptyDocks' :
      return prop['value']


if __name__ == '__main__':
  main()