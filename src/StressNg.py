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
def runCommand(command):
    return sp.Popen(command.split(), stdout=sp.PIPE, stderr=sp.PIPE)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getOutput(p):
    out, err = p.communicate()
    return [out.decode('utf-8').split('\n'), err.decode('utf-8').split('\n')]

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def runAndGetOutput(command):
    p = runCommand(command)
    return getOutput(p)
       
#***********************************************************************************************************************
#
#***********************************************************************************************************************
def getOutputs(listOfPs, index=1):
    data = []

    for p in listOfPs:
        data.append(getOutput(p)[index])

    return data

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def saveResults(fileName, data):
    h.outputToFile(fileName, '\n'.join(data))

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def RunAndSaveResults(fileName, toRun, useIndex=0):
    output = runAndGetOutput(toRun)[useIndex]
    saveResults(fileName, output)

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
    hogs                = 'hogs: '
    time                = 'completed in '
    stressor            = 'stressor'
    emulationFaults = 'Emulation Faults'

    # some helper bools to flag what section we are in
    onStressor = False
    stressorDone = False
    bogoLineStarts = 2
    onDetailed = False

    # holder for output
    data = {}
    
    try:
        # open the file
        with open(fullPathToFile, 'r') as f:
            # iterate over each line
            for line in f:
                # ignore this
                if 'defaulting to a' in line:
                    continue
                # wait for proper stressor line
                if onStressor == True:
                    bogoLineStarts -= 1

                    # we are on the right line
                    if bogoLineStarts == 0:
                        # split up the data
                        list_of_data = line.split(']')[1]
                        list_of_data = re.sub(' +', ' ', list_of_data).lstrip(' ').rstrip(' ').split(' ')

                        # fill in data
                        index = 1
                        data['Bogo']            = float(list_of_data[index])
                        index += 1
                        data['Real Time (s)']   = float(list_of_data[index])
                        index += 1
                        data['User Time (s)']   = float(list_of_data[index])
                        index += 1
                        data['Sys Time (s)']    = float(list_of_data[index])
                        index += 1
                        data['Throughput']      = float(list_of_data[index])
                        index += 1
                        #data['bogo_ops_s_total'] = list_of_data[5].rstrip('\n')

                        onStressor  = False
                        stressorDone = True

                    # nothing interesting yet
                    else:
                        continue
                elif onDetailed == True:
                    # This is the end of the section
                    if '/sec' not in line:
                        onDetailed = False 
                        continue     

                    line = line.split(']')[1]
                    line = re.sub(' +', ' ', line).lstrip(' ').rstrip(' ').replace(',','').split(' ')

                    num = line[0]
                    rateStart = 1
                    for i in range(1, len(line)):
                        if line[i][0].isdigit():
                            rateStart = i
                            break
                    
                    name = ' '.join(line[1:rateStart])
                    rate = line[rateStart]

                    data[name] = float(num)
                    data[name+" Rate"] = float(rate)
                else:  
                    # count hogs
                    if hogs in line:
                        data['Parallelism'] = float(h.getStringBetween(line, hogs, ' '))
                    # count time
                    elif time in line:
                        data['time'] = float(h.getStringBetween(line, time, 's'))
                    elif stressor in line:
                        onStressor = True
                    elif onStressor == False and stressorDone == True:
                        onDetailed = True
                        stressorDone = False
    except Exception as e:
        pass
    return data

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