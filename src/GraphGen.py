#!/usr/bin/python3

#internal
import Helper as h

#built in
import math
import matplotlib.pyplot as plt
import os
import pandas as pd

def extractTestResults(results, x, y):
    badKeys = False

    num_results = len(results.items())
    index   = list(range(0, num_results))
    x_data  = [0] * num_results
    y_data  = [0] * num_results

    iter = 0
    for _, data in results.items():
        if x not in data or y not in data:
            badKeys = True
            break

        x_data[iter] = (int)(data[x])
        y_data[iter] = data[y]
        iter += 1

    if badKeys:
        return None, None, None

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

                    header = 'Multi-Instance' if typeName == 'multiInstance' else 'Single-Instance'
                    plt.title(f'{header} {testSet}')
                    plt.ylabel(y)
                    plt.xlabel(x)

                    index, x_data, y_data = extractTestResults(results, x, y)

                    if index == None and x_data == None and y_data == None:
                        continue

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

    #colors = ['firebrick', 'orangered', 'darkorange', 'gold']
    colors = ['tab:blue', 'tab:red', 'tab:orange', 'tab:green' ]

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

                    broken = False

                    # now, extract vm specific data
                    first = True
                    
                    for vm in vms:
                        
                        index, x_data, y_data = extractTestResults(aggregateData[vm][group][testSet][_type], x, y)

                        if index == None and x_data == None and y_data == None:
                            broken = True
                            continue

                        dataToGraph[vm] = y_data
                        
                        if first:
                            dataToGraph[x] = x_data
                            first = False

                    if broken:
                        continue

                    _columns = [x] + vms
                    df = pd.DataFrame(dataToGraph, columns=_columns)

                    pos = index
                    width = .15

                    fig, ax = plt.subplots(figsize=(15, 10))

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
                            color=colors[index],
                            label=df[vm][index]
                        )

                        index += 1

                    legend = [x.split('-')[1] for x in vms]
                    saveTo = os.path.join(outputDir, group, testSet)
                    h.makeDirectory(saveTo)
                    saveTo = os.path.join(saveTo, f'{_type}_{x}_{y}.png')
                    ax.set_ylabel(y)
                    ax.set_xlabel(x)
                    header = 'Multi-Instance' if _type == 'multiInstance' else 'Single-Instance'
                    ax.set_title(f'{header} {testSet}')
                    ax.set_xticks([p + 2 * width for p in pos])
                    ax.set_xticklabels(df[x])
                    plt.legend(legend, loc='upper left')
                    plt.savefig(saveTo)
                    plt.clf()
                    plt.close()