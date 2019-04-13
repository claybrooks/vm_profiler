#!/usr/bin/python3

#internal
import Helper as h
import TestGroups as t

# built in
import subprocess as sp

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
def RunAndSaveResults(fileName, toRun, useIndex=0):
    output = runAndGetOutput(toRun)[useIndex]
    h.outputToFile(fileName, '\n'.join(output))

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getStressorsForClass(_class):
    return runAndGetOutput(f'stress-ng --class {_class}?')[0][0].split(':')[1].lstrip(' ').rstrip(' ').split(' ')

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def outputAllStressorToFile(file):
    output = "LIST OF STRESSORS\n\n"
    for _class in t.testClasses:
        stressors = '\n'.join([f'\t- {x}' for x in getStressorsForClass(_class)])

        output += f'{_class}:\n'
        output += stressors
        output += '\n\n'

    h.outputToFile(file, output)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getHogs():

    # send command, but tell stress-ng we just want output, not an actual run
    output = runAndGetOutput('stress-ng --cpu 0 --dry-run')[1]

    # we are interested in the hogs
    to_find = 'hogs: '

    # search through all output
    for line in output:
        # we found the line
        if to_find in line:
            # get the number between hogs: and ' '
            return int(h.getStringBetween(line, to_find, ' '))

    # we couldn't find hogs
    return -1