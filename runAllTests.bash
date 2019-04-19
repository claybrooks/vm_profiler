#!/bin/bash

# update ourselves
git pull

paraFile=/proc/sys/kernel/perf_event_paranoid

# store users current paranoid level
paranoidLevel="$(sudo cat ${paraFile})"

# set paranoid level for performance counter
sudo sh -c "echo 1 >${paraFile}"

curDir=$(dirname "$0")
outputFolder=~/Desktop/vm_results
sudo ./$curDir/src/RunTests.py -o $outputFolder -c -r --pmult 2 -t 3 -a

sudo chown -R $USER $outputFolder

sudo sh -c "echo ${paranoidLevel} >${paraFile}"

./$curDir/sendToGit.bash $outputFolder
