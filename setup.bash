#!/bin/bash

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt install stress-ng
sudo apt install python3-matplotlib

sudo apt install linux-tools-common
sudo apt install linux-tools-generic
sudo apt install linux-tools-4.18.0-17-generic

# set privilege for the binary
sudo sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
