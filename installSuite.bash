#!/bin/bash

echo Copying Packages
sudo mkdir -p ~/.phoronix-test-suite/test-suites/local
sudo cp -r packages/vm_* ~/.phoronix-test-suite/test-suites/local

echo Installing Dependancies
phoronix-test-suite install vm_profilerDisk
phoronix-test-suite install vm_profilerGraphics
phoronix-test-suite install vm_profilerMemory
phoronix-test-suite install vm_profilerProcessor
phoronix-test-suite install vm_profilerSystem