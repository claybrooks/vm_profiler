#!/bin/bash

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
sudo cp runAllTests.bash /etc/init.d/runAllTests.bash
sudo chmod +x /etc/init.d/runAllTests.bash
sudo update-rc.d runAllTests.bash defaults