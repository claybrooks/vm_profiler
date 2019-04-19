#!/bin/bash

outputFolder=~/Desktop/vm_results

sudo ./src/RunTests.py -o $outputFolder -a -c

./sendToGit.bash $outputFolder