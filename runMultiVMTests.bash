#!/bin/bash

# update ourselves
git pull

paraFile=/proc/sys/kernel/perf_event_paranoid

# store users current paranoid level
paranoidLevel="$(sudo cat ${paraFile})"

# set paranoid level for performance counter
sudo sh -c "echo 1 >${paraFile}"

outputFolder=~/Desktop/git/vm_profiler/results/$2
sudo ./src/RunTests.py -o $outputFolder -c -r -p 1 -t 1 -a --multiVM $1

#sudo chown -R $USER $outputFolder

sudo sh -c "echo ${paranoidLevel} >${paraFile}"