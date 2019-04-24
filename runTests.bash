#!/bin/bash

echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo Run \$phoronix-test-suite batch-setup first!
echo with Y y n n n Y
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

echo Running Profiler Disk
phoronix-test-suite batch-run vm_profilerDisk

echo Running Profiler Memory
phoronix-test-suite batch-run vm_profilerMemory

echo Running Profiler Processor
phoronix-test-suite batch-run vm_profilerProcessor

echo Running Profiler System
phoronix-test-suite batch-run vm_profilerSystem