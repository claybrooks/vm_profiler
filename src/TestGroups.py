#!/usr/bin/python3

#internal
import StressNg as ng

# Manpage for stress-ng
# http://manpages.ubuntu.com/manpages/bionic/man1/stress-ng.1.html

# to find out what stressors are avialable for a class
# stress-ng --class {name}? ({name} is one of the groups listed above)

# list of possible classes for stress-ng
testClasses = [
    'cpu',
    'cpu-cache',
    'device',
    'io',
    'interrupt',
    'filesystem',
    'memory',
    'network',
    'os',
    'pipe',
    'scheduler',
    'security',
    'vm'
]