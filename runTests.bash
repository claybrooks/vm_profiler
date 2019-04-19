#!/bin/bash

# list tests
#phoronix-test-suite list-recommended-tests
#phoronix-test-suite list-available-tests
#phoronix-test-suite list-available-suites


# cpu suite DONT RUN AS SUDO
phoronix-test-suite batch-benchmark cpu

# Can run individual tests ~~need to hash pick some out~~
# phoronix-test-suite batch-benchmark pybench \
# ramspeed \ 
