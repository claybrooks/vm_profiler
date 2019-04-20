#!/bin/bash

outputFolder=~/Desktop/vm_results

sudo ./src/RunTests.py -o $outputFolder -a --vm --vmresults results -c

mkdir -p results
prior=$PWD
resultsFolder=~/Desktop/git/vm_profiler/results/

cd ~/Desktop/vm_results/aggregateData
zip -r -FS ~/Desktop/git/vm_profiler/aggregateData.zip *
cd $prior

git add aggregateData.zip
git commit -m "Adding aggregate results"
git push