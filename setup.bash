#!/bin/bash

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt-get install stress-ng

# set privilege for the binary
sudo setcap cap_sys_admin+ep /usr/bin/stress-ng