#!/bin/bash

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt install stress-ng
sudo apt install python3-matplotlib

sudo apt install linux-tools-common
sudo apt install linux-tools-generic
sudo apt install linux-tools-$(uname -r)
