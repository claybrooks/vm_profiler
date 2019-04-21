#!/bin/bash

command="cd ~/Desktop/git/vm_profiler; git pull; ./kickOffMultiVMTest.bash"
push="cd ~/Desktop/git/vm_profiler; git pull; ./sendToGit.bash ~/Desktop/vm_results"

# run the commands
ssh clay-kvm@192.168.122.151 -d -m $command
ssh clay-kvm@192.168.122.157 -d -m $command
ssh -t clay-kvm@192.168.122.230 -d -m $command