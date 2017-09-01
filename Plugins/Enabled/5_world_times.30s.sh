#!/bin/bash

function main() {

  tz_current=$(date +%Z)

  # If we're in the UK, display US time, otherwise, display UK time
  if [[ ${tz_current} == "GMT" ]] || [[ ${tz_current} == "BST" ]] ; then
    printf "$(TZ="US/Pacific" date "+🇺🇸 %H:%M")  "
  else
    printf "$(TZ="Europe/London" date "+🇬🇧 %H:%M")  "
  fi

  printf "$(TZ="Asia/Kolkata" date "+🇮🇳 %H:%M")  "
  printf "$(TZ="Asia/Shanghai" date "+🇨🇳 %H:%M")  "
  printf "$(TZ="Asia/Tokyo" date "+🇯🇵 %H:%M")  "

  printf " | color=gray \n"

  echo "---"

  echo -e "$(TZ="Australia/Sydney" date "+🇦🇺 %H:%M %a, %m/%d/%Y") - Australia (Sydney) | color=gray font=Monaco"
  echo -e "$(TZ="Europe/Paris" date "+🇫🇷 %H:%M %a, %m/%d/%Y") - Europe (France) | color=gray font=Monaco"
  echo -e "$(TZ="Europe/Moscow" date "+🇷🇺 %H:%M %a, %m/%d/%Y") - Europe (Moscow) | color=gray font=Monaco"
  echo -e "$(TZ="US/Eastern" date "+🇺🇸 %H:%M %a, %m/%d/%Y") - US Eastern Time (New York) | color=gray font=Monaco"
  echo -e "$(TZ="US/Mountain" date "+🇺🇸 %H:%M %a, %m/%d/%Y") - US Mountain Time (Edmonton) | color=gray font=Monaco"
  echo -e "$(TZ="US/Central" date "+🇺🇸 %H:%M %a, %m/%d/%Y") - US Central Time (Austin) | color=gray font=Monaco"
  echo -e "$(TZ="Etc/UTC" date "+🌍 %H:%M %a, %m/%d/%Y") - UTC | color=gray font=Monaco"

  echo "---"

  getTimeConversionTable "US/Pacific" "🇺🇸"
  echo "---"
  getTimeConversionTable "Asia/Shanghai" "🇨🇳"
  echo "---"
  getTimeConversionTable "Asia/Tokyo" "🇯🇵"

}

function getTimeConversionTable() {

  timezoneRemote="$1"
  flagRemote="$2"

  for (( hourIndex=0; hourIndex<24; hourIndex++ )) {
    if (( ${hourIndex}<10)) ; then
      hourIndexFriendly="0${hourIndex}"
    else
      hourIndexFriendly="${hourIndex}"
    fi

    timeRemote="${hourIndexFriendly}:00"
    timeLocal=$( /usr/local/bin/gdate --date="TZ=\"${timezoneRemote}\" ${timeRemote}" "+%H:%M %a" 2>/dev/null )

    echo -e "${flagRemote}  ${timeRemote} → 🇬🇧  ${timeLocal} | color=gray font=Monaco size=9"
  }

}

main $*

