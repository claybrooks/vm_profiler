#!/bin/bash

outputFolder=~/Desktop/vm_results

sudo ./src/RunTests.py -o $outputFolder -a --vm --vmresults results -c

mkdir -p results
prior=$PWD
resultsFolder=~/Desktop/git/vm_profiler/results/

zip -r -FS aggregateData.zip ~/Desktop/vm_results/aggregateData/*

git add aggregateData.zip
git commit -m "Adding aggregate results"
git push