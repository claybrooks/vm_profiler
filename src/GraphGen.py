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
    
    # iterate through each test set
    for testSet, results in dataSet.items():
        
        _dir = os.path.join(outputDir, testSet)

        # ensure our directory is good
        if os.path.isdir(_dir) == False:
            h.makeDirectory(_dir)

        for x,y in listOfStats:
            outFile = os.path.join(_dir, f'{x}_{y}_bar.png')

            plt.title(f'{testSet}: {y}')
            plt.ylabel(y)
            plt.xlabel(x)

            num_results = len(results.items())
            index   = list(range(0, num_results))
            x_data  = [0] * num_results
            y_data  = [0] * num_results

            # temporarily display bogo ops per group of CPU
            iter = 0
            for _, data in results.items():
                x_data[iter] = int(float(data[x].replace(',','')))
                y_data[iter] = int(float(data[y].replace(',','')))
                iter += 1

            x_data, y_data = (list(t) for t in zip(*sorted(zip(x_data, y_data))))

            low = min(y_data)
            high = max(y_data)

            plt.ylim([0, math.ceil(high+.5*(high - low))])
            plt.xticks(index, x_data)
            plt.bar(index, y_data, align='center', alpha=0.5)
            plt.savefig(outFile)
            plt.clf()