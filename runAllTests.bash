#!/bin/bash

outputFolder=!/Desktop/vm_results
sudo ./src/RunTests.py -o $outputFolder -c -r --pmult 2 -t 3 -a

sudo chown -R $USER $outputFolder
