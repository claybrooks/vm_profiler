#!/bin/bash

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt install -y stress-ng
sudo apt install -y python3-matplotlib

sudo apt install -y linux-tools-common
sudo apt install -y linux-tools-generic
sudo apt install -y linux-tools-$(uname -r)
