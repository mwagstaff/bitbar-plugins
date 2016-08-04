#!/bin/bash

tz_uk=$(TZ=":Europe/London" date "+%m/%d %H:%M:%S")

echo -e "${tz_uk}"