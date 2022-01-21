#!/usr/bin/python3

import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import surprise as sp
import pickle
import logging
import os

import threading
import concurrent.futures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

saveObtainedRaitingDataTo = 'splittedData.sav'

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

# save data to file:
with open(saveObtainedRaitingDataTo, 'wb') as spTmp:
    pickle.dump(spRatingData, spTmp)

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

def runExternalProgram(values):
    #model stored in saveObtainedRaitingDataTo
    argumentsForProgram = ' '+saveObtainedRaitingDataTo+' '+str(values['n_epochs'])+' '+str(values['lr_all'])+' '+str(values['reg_all'])
    stream = os.popen('python3 runSVDWithValues.py' + argumentsForProgram)
    output = stream.read()
    return output

maxThreads = 4
testValues = getInitialDistribution()
testChunks = [testValues[x:x+maxThreads] for x in range(0, len(testValues), maxThreads)]

allResults = []

for chunk in testChunks:
    result = []
    if len(chunk) > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
            for curResult in executor.map(runExternalProgram, chunk):
                result.append(curResult)
    else:
        result.append(runExternalProgram(chunk[0]))

    logger.debug("Result for chunk obtained:"+str(result))
    allResults.extend(result)
    break

logger.info("All Results: "+str(allResults))


databaseConnection.close()
