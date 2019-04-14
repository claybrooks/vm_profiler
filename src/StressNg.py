#!/usr/bin/python3

#internal
import Helper as h
import TestGroups as t

# built in
import subprocess as sp
import re

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
def parseOutput(fullPathToFile):
    # some helper strings for searching
    hogs        = 'hogs: '
    time        = 'completed in '
    stressor    = 'stressor'
    cpu         = 'cpu'
    cpu_colon   = 'cpu: '

    # some helper bools to flag what section we are in
    onStressor = False

    # holder for output
    data = {}
    
    # open the file
    with open(fullPathToFile, 'r') as f:
        # iterate over each line
        for line in f:
            # wait for proper stressor line
            if onStressor == True:
                # we are on the right line
                if cpu in line:
                    # split up the data
                    list_of_data = line.split(cpu)[1]
                    list_of_data = re.sub(' +', ' ', list_of_data).lstrip(' ').rstrip(' ').split(' ')

                    # fill in data
                    data['bogo'] = list_of_data[0]
                    data['real_time'] = list_of_data[1]
                    data['usr_time'] = list_of_data[2]
                    data['sys_time'] = list_of_data[3]
                    data['bogo_ops_s'] = list_of_data[4]
                    data['bogo_ops_s_total'] = list_of_data[5]

                    onStressor = False

                # nothing interesting yet
                else:
                    continue
                    
            # count hogs
            if hogs in line:
                data['hogs'] = h.getStringBetween(line, hogs, ' ')
            # count time
            elif time in line:
                data['time'] = h.getStringBetween(line, time, 's')
            elif stressor in line:
                onStressor = True
                


        # start looking for data
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