#!/bin/bash

setenv MY_USER=$USER
# useful
sudo apt install -y chromium-browser
sudo apt install -y vim
sudo apt install -y net-tools

# add executability
chmod +x src/*.py

# install stress-ng
sudo apt install -y stress-ng
sudo apt install -y python3-matplotlib
sudo apt install -y python3-pandas

sudo apt install -y linux-tools-common
sudo apt install -y linux-tools-generic
sudo apt install -y linux-tools-$(uname -r)

# install our service
sudo mv vm_profiler.service /etc/systemd/system
sudo systemctl enable vm_profiler
chmod u+x ~/Desktop/git/vm_profiler/runAllTests.bash
sudo systemctl enable vm_profiler