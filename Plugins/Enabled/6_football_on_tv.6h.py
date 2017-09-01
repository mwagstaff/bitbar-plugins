#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import *
import time
import urllib2

# Add the path to site packages so that BeautifulSoup and Dateutil are picked up
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from bs4 import BeautifulSoup

from dateutil.relativedelta import *
from dateutil.parser import parse

uri = 'http://www.live-footballontv.com/'

retryAttempts = 1

while retryAttempts > 0:

  try:

    page = urllib2.urlopen( uri )

    soup = BeautifulSoup(page, 'html.parser')

    # Get the listings div content
    container_listings = soup.find('div', attrs={'id': 'listings'})

    # Get all the rows in the listings div
    all_rows = container_listings.find_all('div', attrs={'class': 'row-fluid'})

    today = False
    todaysFixtures = 0
    todaysFixturesOfInterest = 0
    fixturesContent = ""

    # Iterate through each row
    #  - If it's a matchdate, print the match date
    #  - Otherwise, print the fixture details
    for row in all_rows:

      matchdate = row.find('div', attrs={'class': 'matchdate'})
      matchfixture = row.find('div', attrs={'class': 'matchfixture'})
      competition = row.find('div', attrs={'class': 'competition'})
      kickofftime = row.find('div', attrs={'class': 'kickofftime'})
      channels = row.find('div', attrs={'class': 'channels'})

      if matchdate:
        fixturesContent += "---\n"
        matchdateText = matchdate.text.strip()

        # Use dateutils to parse the match date string into a proper date
        # Then check to see if it's today's date
        dtMatchdate = parse(matchdateText)
        fixturesContent += matchdateText
        dtToday = date.today()
        delta_from_today = relativedelta(dtToday, dtMatchdate)

        # If it's today's date, then highlight the content in black
        if delta_from_today.days == 0 and delta_from_today.months == 0:
          today = True
          fixturesContent += " | color=black"

        else:
          today = False

        fixturesContent += "\n"

      # If it's a match fixture, then print the fixture details
      if matchfixture and competition and kickofftime and channels:
        fixturesContent += "  "
        fixturesContent += kickofftime.text.strip() + " "
        fixturesContent += channels.text.strip() + " - "
        fixturesContent += matchfixture.text.strip()
        fixturesContent += " (" + competition.text.strip() + ")"
        fixturesContent += " | trim=false "

        # Highlight today's Premier League and Champions League fixtures in black
        if today:
          todaysFixtures += 1

          if competition.text.strip() == 'Premier League' or ( 'England' in matchfixture.text.strip() and 'U21' not in matchfixture.text.strip() ):
            fixturesContent += " color=black"
            todaysFixturesOfInterest += 1

        fixturesContent += "\n"

    # Print the top menubar icon with the count of today's fixtures
    print '⚽️ ({} - {})'.format( str(todaysFixtures), str(todaysFixturesOfInterest) )

    # Then print all the other match dates and fixtures found above
    print fixturesContent.encode('ascii', 'ignore')

    break

  except:
    time.sleep(3)
    retryAttempts -= 1

if retryAttempts == 0:
  print "⚽️ (⚠️ Unable to get fixture data)"
  print "---"
  print "Well, that sucks. Try again. | refresh=true"