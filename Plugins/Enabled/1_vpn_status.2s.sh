#!/bin/bash

# Try pinging Google (8.8.8.8) to check we have an Internet connection
if ping -c 1 -t 2 -q 8.8.8.8 > /dev/null 2>&1; then

  # If we have Internet, then check the VPN connection status
  vpnConnectionStatus=$(scutil --nc status "DC VPN (SSL)" | head -1)

  if [[ "${vpnConnectionStatus}" == "Disconnected" ]]; then
    echo "⌾ | color=red size=26"
    echo "---"
    echo "Not connected to VPN"
    echo "Connect to VPN | terminal=false bash=~/bin/Scripts/VPN_connect.sh"

  elif [[ "${vpnConnectionStatus}" == "Connecting" ]]; then
    echo "⌾ | color=gray size=26"
    echo "---"
    echo "Connecting to VPN"
    echo "Disconnect from VPN | terminal=false bash=~/bin/Scripts/VPN_disconnect.sh"

  elif [[ "${vpnConnectionStatus}" == "Disconnecting" ]]; then
    echo "⌾ | color=gray size=26"
    echo "---"
    echo "Disconnecting from VPN"
    echo "Connect to VPN | terminal=false bash=~/bin/Scripts/VPN_connect.sh"

  else
    vpnIpAddress=$(ifconfig | grep -A2 utun | grep " --> 17." | cut -d "-" -f1 | cut -d "t" -f2)

    echo "⌾ | color=lightgreen size=26"
    echo "---"
    echo "Connected to VPN:${vpnIpAddress}"
    echo "Disconnect from VPN | terminal=false bash=~/bin/Scripts/VPN_disconnect.sh"
  fi

# If we can't ping Google, assume we're offline
else

    echo "⌾ | color=orange size=26"
    echo "---"
    echo "You are offline!"

fi