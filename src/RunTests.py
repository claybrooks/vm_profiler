#!/usr/bin/python3

# internal
import Helper as h
import TestGroups as t
import StressNg as ng

# built in
import argparse
import os
import sys

_cpu = 'cpu'
_mem = 'memory'

stressorSets = {
    _cpu: [
        'hanoi', 
        'dither', 
        'euler', 
        'factorial', 
        'fibonacci'
    ],
    _mem: [
        'bsearch'
    ]
}

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def cpuCommandBuilder(p, t, stressor):
    return f'stress-ng --cpu {p} --cpu-method {stressor} -t {t}s --metrics-brief --perf --times'

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def memoryCommandBuilder(p, t, stressor):
    return f'stress-ng --cpu {p} --cpu-method {stressor} -t {t}s --metrics-brief --perf --times --dry-run'

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runTestClass(args, name, commandBuilder, stressorSet):
    print (f'Starting {name} Group')

    p = args.numParallel
    t = args.timeAllotted

    testGroupDir = args.outputDir + f'/{name}'

    for stressor in stressorSet:
        print (f'\tStarting {stressor}')
        testSetDir = testGroupDir + f'/{stressor}'

        for i in range(1,p+1):
            command = commandBuilder(i, t, stressor)
            fileName = testSetDir + f'/{i}_{t}.results'
            ng.RunAndSaveResults(fileName, command, 1)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runTests(args):

    # clear the output first
    if os.path.isdir(args.outputDir):
        if args.clean == True:
            h.cleanFolder(args.outputDir)
    else:
        os.mkdir(args.outputDir)

    # high level test group functions
    testClasses = {
        _cpu: cpuCommandBuilder, 
        _mem: memoryCommandBuilder,
    }

    for name, command in testClasses.items():
        runTestClass(args, name, command, stressorSets[name])

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def analyzeData(args):

    # each directory here is a test class, ignore files
    for outputDir, testClasses, _ in os.walk(args.outputDir):
        # iterate through each test class
        for testClass in testClasses:
            # walk through each folder
            for _, testSets, _ in os.walk(os.path.join(outputDir, testClass)):
                # iterate through each test set
                for testSet in testSets:
                    # walk through each folder
                    for _, _, results in os.walk(os.path.join(outputDir, testClass, testSet)):
                        # go through each result
                        for result in results:
                            # parse the data
                            parsedData = ng.parseOutput(os.path.join(outputDir, testClass, testSet, result))


#***********************************************************************************************************************
#
#***********************************************************************************************************************
def validateArgs(args):
    valid = True

    if args.numParallel == 0:
        args.numParallel = ng.getHogs()
        if args.numParallel == -1:
            print ("Couldn't get Hogs")
            valid = False

    if os.path.isdir(args.outputDir) == False:
        h.makeDirectory(args.outputDir)

    if valid == False:
        print("quitting")

#***********************************************************************************************************************
#
#***********************************************************************************************************************
if __name__ == "__main__":
    print ("Stress-ng Test Runner")

    parser = argparse.ArgumentParser(description='Stress-Ng Wrapper for Virtual Machines Project')

    parser.add_argument('-t',
                        dest='timeAllotted',
                        action='store',
                        type=int,
                        default=1,
                        help='Number of seconds allotted for each test.  Default is 1')

    parser.add_argument('-p',
                        dest='numParallel',
                        action="store",
                        type=int,
                        default=0,
                        help='Max parallelism of tests.  Default is 0, which means max parallelism as determined by \
                            stress-ng.  Successive tests will be run from 1 to MAX')

    parser.add_argument('-o',
                        dest='outputDir',
                        action='store',
                        type=str,
                        help='Location of all output date for this script run')

    parser.add_argument('-l',
                        dest='listStressors',
                        action='store_true',
                        help='If this flag is provided, all stressors will be output to -o/Stressors.out  No tests will\
                            be run when this flag is provided.')

    parser.add_argument('-a',
                        dest='analyze',
                        action='store_true',
                        help='If this flag is provided, data will be analyzed')

    parser.add_argument('-r',
                        dest='runTests',
                        action='store_true',
                        help='If this flag is provided, tests will be run')

    parser.add_argument('-c',
                        dest='clean',
                        action='store_true',
                        help='Clean output directory before generating new data')

    args = parser.parse_args()

    validateArgs(args)

    if args.listStressors:
        ng.outputAllStressorToFile(args.outputDir + '/Stressors.out')
        sys.exit(0)

    if args.runTests:
        runTests(args)

    if args.analyze:
        analyzeData(args)
