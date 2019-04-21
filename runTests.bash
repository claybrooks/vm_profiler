#!/bin/bash

echo Running Profiler Disk
phoronix-test-suite batch-run vm_profilerDisk

#echo Running Profiler Graphics
#phoronix-test-suite batch-run vm_profilerGraphics

echo Running Profiler Memory
phoronix-test-suite batch-run vm_profilerMemory

echo Running Profiler Processor
phoronix-test-suite batch-run vm_profilerProcessor

echo Running Profiler System
phoronix-test-suite batch-run vm_profilerSystem