#!/bin/sh
# start.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Desktop/yohan/proto/5
sleep 5
python server.py &
sleep 5
node advertising.js &
python volume.py &
python button.py
cd /