#!/usr/bin/python3

# https://realpython.com/build-recommendation-engine-collaborative-filtering/

# sudo pip3 install scikit-surprise
# if failing with python setup.py...
# sudo apt-get install python3-setuptools
# if failing due to Python.h not found:
# sudo apt-get install python3-dev

import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import surprise as sp
import pickle
import logging

import threading
import concurrent.futures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

filenameOfModel = '../trainedModels/svd__trained_model.sav'

# Create database conection
database = '../database/test.db'
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

#CHECK IF  USER WITH MORE THAN X RATINGS GET CHOSEN FOR TRANING GETS BETTER REUSLTS
#get rating data
ratings = dbSql.execute('''SELECT id_user, id_movie, rating FROM rating''').fetchall()
ratings = pd.DataFrame(ratings, columns = ['id_user', 'id_movie', 'rating'])

#Start surprise library
spReader = sp.Reader(rating_scale=(1,5))
spRatingData = sp.Dataset.load_from_df(ratings, spReader)

def getOwnStatistics(predictions):
    #difference to considered as:
    rightOnDif = 0.5
    stillGoodDif = 1
    mehDif = 1.5

    result = {}
    result['rightOn'] = 0
    result['stillGood'] = 0
    result['meh'] = 0
    result['bad'] = 0
    for curPred in predictions:
        curPredDif = abs(curPred.r_ui - curPred.est)
        if curPredDif <= rightOnDif:
            result['rightOn'] += 1
        elif curPredDif <= stillGoodDif:
            result['stillGood'] += 1
        elif curPredDif <= mehDif:
            result['meh'] += 1
        else:
            result['bad'] += 1
    return result

def getInitialDistribution():
    # In implemented version get best from database latest entry
    #nEpochsStep = 5
    nEpochs = [5, 10, 15]

    #lRAllStep = 0.005
    lRAll = [0.001, 0.005, 0.01]

    #regAllStep = 0.2
    regAll = [0.2, 0.4, 0.6]

    toTest = []

    for curNEpochs in nEpochs:
        for curLRAll in lRAll:
            for curRegAll in regAll:
                combination = {}
                combination['n_epochs'] = curNEpochs
                combination['lr_all'] = curLRAll
                combination['reg_all'] = curRegAll
                toTest.append(combination)
    return toTest

def runSVDWith(values):
    dataSplitSize = 5
    logger.debug("Thread started for values: " + str(values))
    svdAlgorithm = sp.SVD(n_epochs=values['n_epochs'],lr_all=values['lr_all'],reg_all=values['reg_all'])
    splittedDataset = sp.model_selection.split.KFold(n_splits=dataSplitSize, random_state=5, shuffle=True)
    allResults = []
    for trainset, testset in splittedDataset.split(spRatingData):
        #Training the algorithm:
        svdAlgorithm.fit(trainset)
        #predictions:
        predictions = svdAlgorithm.test(testset)
        result = getOwnStatistics(predictions)
        result['rmse'] = sp.accuracy.rmse(predictions, verbose=False)
        result['mae'] = sp.accuracy.mae(predictions, verbose=False)
        allResults.append(result)
        logger.debug('RESULT FOR: n_epochs = '+str(values['n_epochs'])+' lr_all= '+
            str(values['lr_all'])+' reg_all= '+str(values['reg_all'])+' --> '+str(result))
    #Calculate median value to return
    finalResult = {'rmse': 0, 'mae': 0, 'rightOn': 0, 'stillGood': 0, 'meh': 0, 'bad': 0, 'inUse': values}
    for key in allResults[0]:
        for values in allResults:
            finalResult[key] += values[key]/dataSplitSize
    return finalResult

maxThreads = 1

testValues = getInitialDistribution()
testChunks = [testValues[x:x+maxThreads] for x in range(0, len(testValues), maxThreads)]

allResults = []

for chunk in testChunks:
    result = []
    if len(chunk) > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
            for curResult in executor.map(runSVDWith, chunk):
                result.append(curResult)
    else:
        result.append(runSVDWith(chunk[0]))

    logger.debug("Result for chunk obtained:"+str(result))
    allResults.extend(result)

logger.info("All Results: "+str(allResults))

exit(0)

#
# for curNEpochs in nEpochs:
#     for curLRAll in lRAll:
#         for curRegAll in regAll:
#             svdAlgorithm = sp.SVD(n_epochs=curNEpochs,lr_all=curLRAll,reg_all=curRegAll)
#             for trainset, testset in splittedDataset.split(spRatingData):
#                 #Training the algorithm:
#                 svdAlgorithm.fit(trainset)
#                 #predictions:
#                 predictions = svdAlgorithm.test(testset)
#                 print('RESULT FOR: n_epochs=',curNEpochs,'lr_all=',curLRAll,'reg_all=',curRegAll)
#                 result = getOwnStatistics(predictions)
#                 result['rmse'] = sp.accuracy.rmse(predictions, verbose=False)
#                 result['mae'] = sp.accuracy.mae(predictions, verbose=False)
#                 print(result)
#
#                 if result['rmse'] < bestFound['rmse']:
#                     bestFound['rmse'] = result['rmse']
#                     bestFound['mae'] = result['mae']
#                     bestFound['n_epochs'] = curNEpochs
#                     bestFound['lr_all'] = curLRAll
#                     bestFound['reg_all'] = curRegAll
#                     bestFound['result'] = result
#
# print(end='\n\n')
# print("BEST FOUND:")
# print(bestFound)



databaseConnection.close()

# param_grid = {'n_epochs': [5, 10, 15], 'lr_all': [0.002, 0.005, 0.01, 0.02], 'reg_all': [0.2, 0.4, 0.6]}
