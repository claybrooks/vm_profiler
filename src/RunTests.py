#!/usr/bin/python3

# internal
import GraphGen as graph
import Helper as h
import TestGroups as t
import StressNg as ng

# built in
import argparse
from collections import Counter
import os
import sys
import zipfile

_cpu = 'cpu'
_mem = 'memory'
_sch = 'scheduler'

testClasses = [
    _cpu, 
    _mem,
    _sch,
]

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def simpleCommandBuilder(p, t, _class, stressor, separateInstances):
    if separateInstances:
        return f'stress-ng --{stressor} 1 --{stressor}-ops {stressorBogoLimit[_class][stressor]} --metrics-brief --perf --times'
    else:
        return f'stress-ng --{stressor} {p} -t {t}s --metrics-brief --perf --times'

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def cpuCommandBuilder(p, t, _class, stressor, separateInstances):
    if separateInstances:
        return f'stress-ng --cpu 1 --cpu-method {stressor} --cpu-ops {stressorBogoLimit[_class][stressor]} --metrics-brief --perf --times'
    else:
        return f'stress-ng --cpu {p} --cpu-method {stressor} -t {t}s --metrics-brief --perf --times'

classBuilders = {
    _cpu: cpuCommandBuilder, 
    _mem: simpleCommandBuilder,
    _sch: simpleCommandBuilder,
}

stressorSets = {
    _cpu: [
        'hanoi', 
        'atomic',
        #'dither', 
        #'euler', 
        #'pi', 
        #'fibonacci'
    ],
    _mem: [
        #'bsearch',
        #'hsearch',
        #'tsearch',
        'memcpy',
    ],
    _sch: [
        'pthread'
    ]
}

stressorBogoLimit = {
    _cpu: {
        'hanoi': 250
    },
    _mem: {
        'memcpy': 1000,
    },
    _sch: {
        'pthread': 1750,
    }
}

classGraphGen = {
    _cpu: graph.genBargraph,
    _mem: graph.genBargraph,
    _sch: graph.genBargraph,
}

commonSets = [
    ('Parallelism', 'Throughput'),
    ('Parallelism', 'time'),
    
    ('Parallelism', 'CPU Clock'),
    ('Parallelism', 'Task Clock'),
    ('Parallelism', 'Page Faults Total'),
    ('Parallelism', 'Page Faults Minor'),
    ('Parallelism', 'Page Faults Major'),
    ('Parallelism', 'Context Switches'),
    ('Parallelism', 'CPU Migrations'),
    ('Parallelism', 'Alignment Faults'),
    ('Parallelism', 'Emulation Faults'),
    ('Parallelism', 'Page Faults User'),
    ('Parallelism', 'Page Faults Kernel'),
    ('Parallelism', 'System Call Enter'),
    ('Parallelism', 'System Call Exit'),
    ('Parallelism', 'TLB Flushes'),
    ('Parallelism', 'Kmalloc'),
    ('Parallelism', 'Kmalloc Node'),
    ('Parallelism', 'Kfree'),
    ('Parallelism', 'Kmem Cache Alloc'),
    ('Parallelism', 'Kmem Cache Alloc Node'), 
    ('Parallelism', 'Kmem Cache Free'),
    ('Parallelism', 'MM Page Alloc'),
    ('Parallelism', 'MM Page Free'),
    ('Parallelism', 'RCU Utilization'),
    ('Parallelism', 'Sched Migrate Task'),
    ('Parallelism', 'Sched Move NUMA'),
    ('Parallelism', 'Sched Wakeup'),
    ('Parallelism', 'Sched Proc Exec'),
    ('Parallelism', 'Sched Proc Exit'),
    ('Parallelism', 'Sched Proc Fork'),
    ('Parallelism', 'Sched Proc Free'),
    ('Parallelism', 'Sched Proc Hang'),
    ('Parallelism', 'Sched Proc Wait'),
    ('Parallelism', 'Sched Switch'),
    ('Parallelism', 'Signal Generate'),
    ('Parallelism', 'Signal Deliver'),
    ('Parallelism', 'IRQ Entry'),
    ('Parallelism', 'IRQ Exit'),
    ('Parallelism', 'Soft IRQ Entry'),
    ('Parallelism', 'Soft IRQ Exit'),
    ('Parallelism', 'Writeback Dirty Inode'), 
    ('Parallelism', 'Writeback Dirty Page'),
    ('Parallelism', 'Migrate MM Pages'),
    ('Parallelism', 'SKB Consume'),
    ('Parallelism', 'SKB Kfree'),
    ('Parallelism', 'IOMMU IO Page Fault'),
    ('Parallelism', 'IOMMU Map'), 
    ('Parallelism', 'IOMMU Unmap'),
]

classGraphDataSets = {
    _cpu: commonSets,
    _mem: commonSets,
    _sch: commonSets,
}

testResults = 'testResults'
analyzedResults = 'analyzedData'
aggregateResults = 'aggregateData'
testResultsDir = ''
analyzedDataDir = ''
analyzedAggregateData = ''

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runTestClass(args, name, commandBuilder, stressorSet, separateInstances):
    global testResultsDir

    print (f'Starting {name} Group')

    p = args.numParallel
    t = args.timeAllotted

    testGroupDir = os.path.join(testResultsDir, f'{name}')
    
    for stressor in stressorSet:
        print (f'\tStarting {stressor}')
        testSetDir = os.path.join(testGroupDir, f'{stressor}')

        for i in range(1,p+1):
            command = commandBuilder(i, t, name, stressor, separateInstances)
            print(f'\t\tP={i}')
            # running as a single stress-ng instance
            if not separateInstances:
                fileName = os.path.join(testSetDir, f'{i}_{t}.results')
                ng.RunAndSaveResults(fileName, command, 1)
            # running as multiple
            else:
                processes = []

                # spawn the appropriate number of processes
                for _ in range(0, i):
                    processes.append(ng.runCommand(command))

                allOuputs = ng.getOutputs(processes)
                
                iter = 0
                for output in allOuputs:
                    fileName = os.path.join(testSetDir, 'separateInstances', f'{i}', f'{iter}.results')
                    ng.saveResults(fileName, output)
                    iter += 1

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

    print(f'Single Instance Stress-ng')
    for name in testClasses:
        runTestClass(args, name, classBuilders[name], stressorSets[name], False)

    print (f'Multi Instance Stress-ng')
    for name in testClasses:
        runTestClass(args, name, classBuilders[name], stressorSets[name], True)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runAggregateAnalysis(args):

    print (f'Analayzing folder {args.vmResultsDirectory} as aggregate VM results folder')

    # clearing previous results
    h.cleanFolder(analyzedAggregateData)
    
    tempExtractionDir = os.path.join(analyzedAggregateData, 'temp')
    h.makeDirectory(tempExtractionDir)

    for filename in os.listdir(args.vmResultsDirectory):
        # join immediately
        fullPathToFile = os.path.join(args.vmResultsDirectory, filename)

        extension = os.path.splitext(filename)[1]
        filename = os.path.splitext(filename)[0]

        # we are only lookin at zips
        if extension != '.zip':
            continue

        print (f'Found results for {fullPathToFile}')
        
        # extract everything
        zipfile.ZipFile(fullPathToFile, 'r').extractall(os.path.join(tempExtractionDir, filename))

    # now that we've extracted everything, process the folder like normal
    agData = {}

    # iterate over each one
    for _dir in next(os.walk(tempExtractionDir))[1]:
        print (f'Start Analyzing {_dir}')
        agData[_dir] = analyzeData(args, os.path.join(tempExtractionDir, _dir, testResults))

    graph.genAggregateBargraph(analyzedAggregateData, agData, classGraphDataSets)

    print ("cleaning temp")
    h.cleanFolder(tempExtractionDir)
    os.rmdir(tempExtractionDir)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runVMAnalysis(args):
    parsedData = analyzeData(args, testResultsDir)

    # got our parsed data, now we need to do a bit of work on the separate instance thing
    generateGraphs(args, parsedData)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def analyzeData(args, directoryToAnalyze):
    parsedData = {}

    # each directory here is a test class, ignore files
    for topLevel, folders, _ in os.walk(directoryToAnalyze):

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

                    print(f'Analyzing {testClass}:{testSet}')
                    classData[testSet] = {}
                    testSetData = classData[testSet]
                    
                    testSetData['singleInstance'] = {}
                    singleInstance = testSetData['singleInstance']

                    # walk through each folder
                    for _dir, _subdirs, results in os.walk(os.path.join(topLevel, testClass, testSet)):
                        # go through each result
                        for result in results:
                            singleInstance[result] = ng.parseOutput(os.path.join(topLevel, testClass, testSet, result))

                        break

                    # walk through the separate instance test
                    testSetData['multiInstance'] = {}
                    multiInstance = testSetData['multiInstance']

                    for _dir, _subdirs, results in os.walk(os.path.join(topLevel, testClass, testSet, 'separateInstances')):
                        for _subdir in _subdirs:

                            results = []
                            for result in os.listdir(os.path.join(topLevel, testClass, testSet, 'separateInstances', _subdir)):
                                results.append(ng.parseOutput(os.path.join(topLevel, testClass, testSet, 'separateInstances', _subdir, result)))

                            # now average all of the results
                            sums = Counter()
                            counters = Counter()
                            for itemset in results:
                                sums.update(itemset)
                                counters.update(itemset.keys())

                            result = {x:float(sums[x])/counters[x] for x in sums.keys()}

                            # parallelism number report by ng is not 'correct', we know that it is actually
                            # more.  The real parallelism number is the subdir that these results are located
                            # in
                            result["Parallelism"] = int(_subdir)

                            multiInstance[_subdir] = result

                        break
                # break after iterating through all testSets
                break
        # break after iterating through all testClasses
        break
    return parsedData
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
    global analyzedAggregateData

    # track if our arguments are valid
    valid = True

    # check parallelsism
    if args.numParallel == 0:
        args.numParallel = int(ng.getHogs() * args.parallelMultipler)
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

    if args.vmAnalysis and os.path.isdir(args.vmResultsDirectory) == False:
        print(f'Invalid aggregate VM Results Path: {args.vmResultsDirectory}')
        valid = False

    # we've determined we are valid, do stuff
    if valid:
        # create our output directory if it doesn't exist
        if os.path.isdir(args.outputDir) == False:
            h.makeDirectory(args.outputDir)

        testResultsDir = os.path.join(args.outputDir, testResults)

        if args.multiVM:
            testResultsDir = os.path.join(testResultsDir, 'multiVM', f'{args.multiVM}')

        h.makeDirectory(testResultsDir)

        analyzedDataDir = os.path.join(args.outputDir, analyzedResults)
        h.makeDirectory(analyzedDataDir)

        analyzedAggregateData = os.path.join(args.outputDir, aggregateResults)
        h.makeDirectory(analyzedAggregateData)
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
                        type=float,
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
                        type=float,
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

    parser.add_argument('--vm',
                        dest='vmAnalysis',
                        action='store_true',
                        help='If this flag is provided, data will be analyzed for aggregate vm results.  -a also has to be provided, as well as -o to the \
                            aggregate results folder')

    parser.add_argument('--vmresults',
                        dest='vmResultsDirectory',
                        action='store',
                        type=str,
                        help='Location of all vm aggregate results to read from')

    parser.add_argument('--multiVM',
                        dest='multiVM',
                        action='store',
                        help='If this flag is provided, test will assume it\'s running in a multi vm environment')

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
        if args.vmAnalysis:
            runAggregateAnalysis(args)
        else:
            runVMAnalysis(args)

    sys.exit(0)