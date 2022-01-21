#!/usr/bin/python3


import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import surprise as sp
import pickle
import logging
import sys

logger = logging.getLogger(__name__)

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

def runSVDWith(values, spRatingData):
    dataSplitSize = 5
    logger.debug('Thread started for values: ' + str(values))
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

def loadDataAndRun(currentRatingData, values):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)

    spRatingData = None
    # load saved model:
    with open(currentRatingData, 'rb') as svdModel:
        spRatingData = pickle.load(svdModel)
    if spRatingData == None:
        logger.critical('ERROR: unable to open file '+currentRatingData)
        exit(0)
    print(runSVDWith(values, spRatingData))

def checkVariablesAndRun():
    if len(sys.argv) != 5:
        logger.critical('ERROR: wrong number of arguments')
        exit(0)
    values = {'n_epochs': int(sys.argv[2]), 'lr_all': float(sys.argv[3]), 'reg_all': float(sys.argv[4])}
    loadDataAndRun(sys.argv[1], values)

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    checkVariablesAndRun()
