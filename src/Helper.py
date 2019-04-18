#!/usr/bin/python3

import pathlib
import os
import shutil
import zipfile

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def outputToFile(full_path_to_file, data):
    # make sure all folders are created for the file
    makeDirectory(os.path.dirname(full_path_to_file))

    f = open(full_path_to_file, 'w+')
    f.write(data)
    f.close()

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
def makeDirectory(directory):
    if os.path.isdir(directory) == False:
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def cleanFolder(fullPathToDir):
    if os.path.isdir(fullPathToDir) == False:
        return

    for file in os.listdir(fullPathToDir):
        filePath = os.path.join(fullPathToDir, file)

        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print(e)