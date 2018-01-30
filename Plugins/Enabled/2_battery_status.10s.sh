#!/bin/bash

batteryInfo=$( pmset -g batt | egrep "([0-9]+\%).*" -o | awk -F "present" '{print $1}' )

# chargeRemaining=$( echo "${batteryInfo}" | grep -i capacity | tr '\n' ' | ' | awk '{printf("%.0f", $10/$5 * 100)}' )

if [[ $(echo "${batteryInfo}" | grep "charged") ]] ; then
  chargeRemaining=100
else
  chargeRemaining=$( echo "${batteryInfo}" | cut -d '%' -f1 )
fi

# currentCapacity=$( echo "${batteryInfo}" | grep "CurrentCapacity" | cut -d '=' -f2 | xargs)
# maxCapacity=$( echo "${batteryInfo}" | grep "MaxCapacity" | cut -d '=' -f2 | xargs)
# chargeRemaining=$(( currentCapacity * 100 / maxCapacity ))

# isExternalConnected=$( echo "${batteryInfo}" | grep -v "discharging" )

if (( chargeRemaining < 25 )) ; then
  color="orange"
  size="14"
elif (( chargeRemaining < 15 )) ; then
  color="red"
  size="18"
else
  color="gray"
  size="12"
fi

if [[ $( echo "${batteryInfo}" | grep "not charging" ) ]] ; then
  chargeIcon="🔴"
elif [[ $( echo "${batteryInfo}" | grep -v "discharging" ) ]] ; then
  chargeIcon="⚡"
else
  chargeIcon="🚫"
fi

if (( chargeRemaining < 25 )) ; then
  batterySummaryInfo=$( echo "${batteryInfo}" | cut -d ';' -f3 )
fi

echo "${chargeRemaining}% ${batterySummaryInfo} ${chargeIcon} | color=${color} size=${size}"

echo "---"

echo "${batteryInfo}"