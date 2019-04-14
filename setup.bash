#!/bin/bash

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt-get install stress-ng
sudo apt-get install python3-matplotlib

# set privilege for the binary
sudo setcap cap_sys_admin+ep /usr/bin/stress-ng