#!/bin/bash

# update ourselves
git pull

# set ourselves up if necessary
./setup.bash

paraFile=/proc/sys/kernel/perf_event_paranoid

# store users current paranoid level
paranoidLevel="$(sudo cat ${paraFile})"

# set paranoid level for performance counter
sudo sh -c "echo 1 >${paraFile}"

outputFolder=~/Desktop/vm_results
sudo ./src/RunTests.py -o $outputFolder -c -r --pmult 2 -t 1 -a

#sudo chown -R $USER $outputFolder

sudo sh -c "echo ${paranoidLevel} >${paraFile}"

./sendToGit.bash $outputFolder
