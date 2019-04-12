#!/usr/bin/python3

import argparse
import os
import pathlib
import subprocess as sp
import shutil

# CPU Group Micro Tests
CPUTests = ['hanoi']

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def outputToFile(full_path_to_file, data):
    # make sure all folders are created for the file
    pathlib.Path(os.path.dirname(full_path_to_file)).mkdir(parents=True, exist_ok=True)

    f = open(full_path_to_file, 'w+')
    f.write(data)
    f.close()

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def RunAndSaveResults(fileName, toRun, useIndex=0):
    output = runAndGetOutput(toRun)[useIndex]
    outputToFile(fileName, '\n'.join(output))

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def RunCPU(args):
    print ("Starting CPU Group")
    
    p = args.numParallel
    t = args.timeAllotted

    testGroupDir = args.outputDir + '/CPU'

    for test in CPUTests:
        print (f'Running {test} test set')
        testSetDir = testGroupDir + f'/{test}'

        for i in range(1,p+1):
            command = f'stress-ng --cpu {i} --cpu-method {test} -t {t}s --metrics-brief'
            fileName = testSetDir + f'/{i}_{t}.results'
            RunAndSaveResults(fileName, command, 1)

# high level test group functions
TestGroupFuncs = [RunCPU]

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def RunTests(args):
    # clear the output first
    if os.path.isdir(args.outputDir):
        if args.clean == True:
            cleanFolder(args.outputDir)
    else:
        os.mkdir(args.outputDir)

    for func in TestGroupFuncs:
        func(args)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getHogs():

    output = runAndGetOutput('stress-ng --cpu 0 --dry-run')[1]

    to_find = 'hogs: '

    for line in output:
        if to_find in line:
            return int(getStringBetween(line, to_find, ' '))

    return -1

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def cleanFolder(fullPathToDir):
    for file in os.listdir(fullPathToDir):
        filePath = os.path.join(fullPathToDir, file)

        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print(e)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getStringBetween(string, sub1, sub2):
    start = string.find(sub1) + len(sub1)
    end = string.find(sub2, start)
    return string[start:end]

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runAndGetOutput(command):
    p = sp.Popen(command.split(), stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = p.communicate()

    return [out.decode('utf-8').split('\n'), err.decode('utf-8').split('\n')]

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def validateArgs(args):
    if args.numParallel == 0:
        args.numParallel = getHogs()

    if os.path.isdir(args.outputDir) == False:
        os.mkdir(args.outputDir)

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
                        required=True,
                        help='Location of all output date for this script run')

    parser.add_argument('-c',
                        dest='clean',
                        action='store_true',
                        help='Clean output directory before generating new data')

    args = parser.parse_args()

    validateArgs(args)

    RunTests(args)