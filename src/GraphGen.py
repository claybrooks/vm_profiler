#!/usr/bin/python3

#internal
import Helper as h

#built in
import math
import matplotlib.pyplot as plt
import os
#***********************************************************************************************************************
#
#***********************************************************************************************************************
def genBargraph(outputDir, dataSet, listOfStats):
    
    # ensure our directory is good
    if os.path.isdir(outputDir) == False:
        h.makeDirectory(outputDir)

    # iterate through each test set
    for testSet, results in dataSet.items():

        for x,y in listOfStats:
            outFile = os.path.join(outputDir, testSet) + f'_{x}_{y}_bar.png'

            plt.title(f'{testSet}: {y}')
            plt.ylabel(y)
            plt.xlabel(x)
            plotData = {}

            # temporarily display bogo ops per group of CPU
            for _, data in results.items():
                plotData[data[x]] = data[y]

            index = list(range(0, len(plotData)))
            x_data = list(range(1, len(plotData) + 1))
            y_data = [0] *len(x_data)

            for x in x_data:
                y_data[x-1] = float(plotData[str(x)])

            # normalize to 1
            high = max(y_data)
            y_data = [x/high for x in y_data]

            low = min(y_data)
            high = max(y_data)

            plt.ylim([math.ceil(low-.5*(high - low)), math.ceil(high+.5*(high - low))])
            plt.xticks(index, x_data)
            plt.bar(index, y_data, align='center', alpha=0.5)
            plt.savefig(outFile)
            plt.clf()