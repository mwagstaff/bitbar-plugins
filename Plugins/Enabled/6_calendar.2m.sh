#!/bin/bash

date +%m/%d

echo "---"

/usr/local/bin/icalBuddy -ic 'Calendar' -n -ss "\n\n---" -eep "location,notes,url,attendees" -sd eventsToday+3