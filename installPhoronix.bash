#!/bin/bash

sudo apt install -y gdebi-core
sudo apt install -y aptitude
sudo gdebi packages/phoronix-test-suite_8.6.1_all.deb
#sudo apt install libssl-dev libssl1.0.0=1.0.1e-2+deb7u14
sudo apt install -y libsdl1.2-dev libsdl-image1.2-dev
sudo apt install -y autoconf
sudo apt install -y libssl1.0-dev 

sudo cp packages/phoronix-test-suite.xml /etc/

sudo apt update
sudo apt upgrade
