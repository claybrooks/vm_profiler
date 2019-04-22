#!/bin/bash

export MY_USER=$USER
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

sudo apt install -y openssh-server

git config credential.helper store
git config --global user.name "Clay Brooks"
git config --global user.email "clay_brooks@outlook.com"

if [ $1 == "vb" ]; then
    sudo ifconfig enp0s8 192.168.56.$2 netmask 255.255.255.0 up