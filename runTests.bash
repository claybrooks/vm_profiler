#!/bin/bash

echo Running Profiler Disk
sudo phoronix-test-suite batch-run vm_profilerDisk

echo Running Profiler Graphics
sudo phoronix-test-suite batch-run vm_profilerGraphics

echo Running Profiler Memory
sudo phoronix-test-suite batch-run vm_profilerMemory

echo Running Profiler Processor
sudo phoronix-test-suite batch-run vm_profilerProcessor

echo Running Profiler System
sudo phoronix-test-suite batch-run vm_profilerSystem