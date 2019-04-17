#!/usr/bin/python3

# internal
import GraphGen as graph
import Helper as h
import TestGroups as t
import StressNg as ng

# built in
import argparse
import os
import sys

_cpu = 'cpu'
#***********************************************************************************************************************
#
#***********************************************************************************************************************
def cpuCommandBuilder(p, t, stressor):
    return f'stress-ng --cpu {p} --cpu-method {stressor} -t {t}s --metrics-brief --perf --times'

_mem = 'memory'
_sch = 'scheduler'
#***********************************************************************************************************************
#
#***********************************************************************************************************************
def simpleCommandBuilder(p, t, stressor):
    return f'stress-ng --{stressor} {p} -t {t}s --metrics-brief --perf --times'

testClasses = [
    _cpu, 
    _mem,
    _sch
]

classBuilders = {
    _cpu: cpuCommandBuilder, 
    _mem: simpleCommandBuilder,
    _sch: simpleCommandBuilder
}

stressorSets = {
    _cpu: [
        'hanoi', 
        'dither', 
        'euler', 
        'factorial', 
        'fibonacci'
    ],
    _mem: [
        'bsearch',
        'hsearch',
        'tsearch',
        'memcpy',
    ],
    _sch: [
        'msg',
        'pthread'
    ]
}

classGraphGen = {
    _cpu: graph.genBargraph,
    _mem: graph.genBargraph,
    _sch: graph.genBargraph
}

classGraphDataSets = {
    _cpu: [
        ('Parallelism',     'Throughput'),
        ('Parallelism',     'Page Faults User'),
    ],
    _mem: [
        ('Parallelism',     'Throughput'),
        ('Parallelism',     'Page Faults User'),
    ],
    _sch: [
        ('Parallelism',     'Throughput'),
        ('Parallelism',     'Page Faults User'),
    ],
}

testResultsDir = ''
analyzedDataDir = ''

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runTestClass(args, name, commandBuilder, stressorSet):
    global testResultsDir

    print (f'Starting {name} Group')

    p = args.numParallel
    t = args.timeAllotted

    testGroupDir = testResultsDir + f'/{name}'

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
def clearTestFolders(args, fullPathToFolder):
    # clear the output first
    if os.path.isdir(fullPathToFolder):
        # we want to clean our output folder
        if args.clean == True:
            # only clean classes we are running
            for _class in testClasses:
                h.cleanFolder(os.path.join(fullPathToFolder, _class))
#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runTests(args):
    
    clearTestFolders(args, testResultsDir)

    print(f'Running with parallelism of {args.numParallel}')

    for name in testClasses:
        runTestClass(args, name, classBuilders[name], stressorSets[name])

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def analyzeData(args):

    print("Analyzing Data")

    parsedData = {}

    # each directory here is a test class, ignore files
    for topLevel, folders, _ in os.walk(testResultsDir):

        # iterate through each test class
        for testClass in folders:

            # we don't care about this folder
            if testClass not in testClasses:
                continue

            parsedData[testClass] = {}
            classData = parsedData[testClass]

            # walk through each folder
            for _dir, testSets, _file in os.walk(os.path.join(topLevel, testClass)):

                # iterate through each test set
                for testSet in testSets:
                    classData[testSet] = {}
                    testSetData = classData[testSet]

                    # walk through each folder
                    for _, _, results in os.walk(os.path.join(topLevel, testClass, testSet)):
                        # go through each result
                        for result in results:
                            testSetData[result] = ng.parseOutput(os.path.join(topLevel, testClass, testSet, result))

                # break after iterating through all testSets
                break
        # break after iterating through all testClasses
        break

    generateGraphs(args, parsedData)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def generateGraphs(args, parsedData):
    
    print("Generating Graphs")

    clearTestFolders(args, analyzedDataDir)

    # iterate over each class
    for _class in testClasses:
        # graph each data set
        classGraphGen[_class](os.path.join(analyzedDataDir, _class), parsedData[_class], classGraphDataSets[_class])

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def validateArgs(args):
    # flag as the global version of this var
    global testClasses
    global testResultsDir
    global analyzedDataDir

    # track if our arguments are valid
    valid = True

    # check parallelsism
    if args.numParallel == 0:
        args.numParallel = ng.getHogs() * args.parallelMultipler
        if args.numParallel == -1:
            print ("Couldn't get Hogs")
            valid = False

    # user has specified classes to test, verify they exist
    if len(args.classesToTest) > 0:
        allValid = True
        for _class in args.classesToTest:
            if _class not in testClasses:
                allValid = False
                print(f'{_class} is not a valid test class')

        # store to higher level flag
        valid = allValid

        # overwrite global for this test run
        if allValid:
            testClasses = args.classesToTest

        else:
            print (f'List of valid classes: {", ".join(testClasses)}')


    # we've determined we are valid, do stuff
    if valid:
        # create our output directory if it doesn't exist
        if os.path.isdir(args.outputDir) == False:
            h.makeDirectory(args.outputDir)

        testResultsDir = os.path.join(args.outputDir, 'testResults')
        h.makeDirectory(testResultsDir)

        analyzedDataDir = os.path.join(args.outputDir, 'analyzedData')
        h.makeDirectory(analyzedDataDir)
    else:
        print("quitting")

    return valid

#***********************************************************************************************************************
#
#***********************************************************************************************************************
if __name__ == "__main__":
    print ("Stress-ng Test Runner")

    parser = argparse.ArgumentParser(description='Stress-Ng Wrapper for Virtual Machines Project')

    parser.add_argument('--class',
                        dest='classesToTest',
                        action='append',
                        type=str,
                        default=[],
                        help="Specify which classes of tests to run.  If nothing is supplied, all classes will be run. \
                             More than one can be provided")

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

    parser.add_argument('--pmult',
                        dest='parallelMultipler',
                        action="store",
                        type=int,
                        default=1,
                        help='Multiplier for parallelism number.  Only used if -p is not provided.')
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

    if validateArgs(args) == False:
        sys.exit(0)

    if args.listStressors:
        ng.outputAllStressorToFile(args.outputDir + '/Stressors.out')
        sys.exit(0)

    if args.runTests:
        runTests(args)

    if args.analyze:
        analyzeData(args)

    sys.exit(0)