#!/usr/bin/python3

#internal
import Helper as h

#built in
import math
import matplotlib.pyplot as plt
import os
import pandas as pd

def extractTestResults(results, x, y):
    num_results = len(results.items())
    index   = list(range(0, num_results))
    x_data  = [0] * num_results
    y_data  = [0] * num_results

    iter = 0
    for _, data in results.items():
        x_data[iter] = data[x]
        y_data[iter] = data[y]
        iter += 1

    x_data, y_data = (list(t) for t in zip(*sorted(zip(x_data, y_data))))

    return index, x_data, y_data

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def genBargraph(outputDir, dataSet, listOfStats):
    
    # iterate through each test set
    for testSet, _type in dataSet.items():
        
        _dir = os.path.join(outputDir, testSet)

        # ensure our directory is good
        if os.path.isdir(_dir) == False:
            h.makeDirectory(_dir)
        
        # get the results from the type of run
        for typeName, results in _type.items():
                # iterate over the list of stats we want to extract
                for x,y in listOfStats:
            
                    outFile = os.path.join(_dir, f'{typeName}_{x}_{y}_bar.png')

                    plt.title(f'{testSet}: {y}')
                    plt.ylabel(y)
                    plt.xlabel(x)

                    index, x_data, y_data = extractTestResults(results, x, y)

                    low = min(y_data)
                    high = max(y_data)

                    plt.ylim([0, math.ceil(high+.5*(high - low))])
                    plt.xticks(index, x_data)
                    plt.bar(index, y_data, align='center', alpha=0.5)
                    plt.savefig(outFile)
                    plt.clf()

#***********************************************************************************************************************
#
#***********************************************************************************************************************
def genAggregateBargraph(outputDir, aggregateData, listOfStats):

    # get the keys, these are the different groups
    vms = list(aggregateData.keys())

    # assume they allhave the same exact tests run!
    testGroups = aggregateData[vms[0]].keys()

    # high level
    rawData = {}

    colors = ['#FF0000', '#00FF00', '#0000FF', '#FF00FF', '#00FFFF', '#FFFF00']

    # iterate over each test group
    for group in testGroups:
        # assume each test group has the same set of tests!
        testSets = list(aggregateData[vms[0]][group].keys())

        # now iterate over each test set
        for testSet in testSets:
            print (f'Graphing {group}:{testSet}')

            types = list(aggregateData[vms[0]][group][testSet].keys())

            for _type in types:

                # we have multiple relationships we want to show
                for x,y in listOfStats[group]:

                    dataToGraph = {}

                    # now, extract vm specific data
                    first = True
                    for vm in vms:
                        
                        index, x_data, y_data = extractTestResults(aggregateData[vm][group][testSet][_type], x, y)

                        dataToGraph[vm] = y_data
                        
                        if first:
                            dataToGraph[x] = x_data
                            first = False

                    _columns = [x] + vms
                    df = pd.DataFrame(dataToGraph, columns=_columns)

                    pos = index
                    width = .2

                    fig, ax = plt.subplots(figsize=(20,10))

                    index = 0
                    for vm in vms:
                        
                        _list = []

                        if index == 0:
                            _list = pos
                        else:
                            _list = [p + (width*index) for p in pos]

                        plt.bar(_list,
                            df[vm],
                            width,
                            alpha=.5,
                            color=colors[index],
                            label=df[vm][index]
                        )

                        index += 1

                    saveTo = os.path.join(outputDir, group, testSet)
                    h.makeDirectory(saveTo)
                    saveTo = os.path.join(saveTo, f'{_type}_{x}_{y}.png')
                    ax.set_ylabel(y)
                    ax.set_xlabel(x)
                    ax.set_title(f'{testSet}: {y}')
                    ax.set_xticks([p + 5* width for p in pos])
                    ax.set_xticklabels(df[x])
                    plt.legend(vms, loc='upper left')
                    plt.savefig(saveTo)
                    plt.clf()
                    plt.close()