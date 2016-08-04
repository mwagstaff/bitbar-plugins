#!/bin/bash

tz_pt=$(TZ=":US/Pacific" date "+🇺🇸 %H:%M")
tz_in=$(TZ=":Asia/Kolkata" date "+🇮🇳 %H:%M")
tz_cn=$(TZ=":Asia/Shanghai" date "+🇨🇳 %H:%M")

echo -e "${tz_pt}   ${tz_in}   ${tz_cn}| color=gray"