#!/usr/bin/python3

import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import surprise as sp
import pickle
import logging
import os
import ast
import datetime

import threading
import concurrent.futures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

saveObtainedRaitingDataTo = 'splittedDataForMultThreading.sav'

saveTrainedModelTo = '../trainedModels/svd_trained_model.sav'

# Create database conection
database = '../database/test.db'
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor()

minimumRatings = 15

#CHECK IF  USER WITH MORE THAN X RATINGS GET CHOSEN FOR TRANING GETS BETTER RESULTS
#get rating data
# ratings = dbSql.execute('''SELECT id_user, id_movie, rating FROM rating''').fetchall()
ratings = dbSql.execute('''WITH tmpRatings AS (SELECT id_user, rating FROM rating
                            GROUP BY id_user
                            HAVING count(rating) >= ?)
                            SELECT rating.id_user, rating.id_movie, rating.rating FROM rating INNER JOIN tmpRatings
                            on rating.id_user = tmpRatings.id_user
                            ''', (minimumRatings,)).fetchall()

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
    nEpochs = [5, 10, 15, 20, 25, 30, 35, 40]
    #nEpochs = [5, 10]

    #lRAllStep = 0.005
    lRAll = [0.001, 0.005, 0.01, 0.02, 0.03, 0.04]
    #lRAll = [0.001, 0.005]

    #regAllStep = 0.2
    regAll = [0.1, 0.2, 0.4]
    #regAll = [0.2, 0.4]

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

def insertResultIntoDatabases(results, dbSql, userData ,minRatings = 1):
    logger.debug("INSERT INTO DATABASE")
    lastIdSVDBlock = dbSql.execute('''SELECT max(id) FROM svdTrainBlock''').fetchall()[0][0]
    logger.info("Last one was:"+str(lastIdSVDBlock))
    nextSVDId = lastIdSVDBlock+1

    curDate = datetime.datetime.now()
    dbSql.execute('''INSERT INTO svdTrainBlock(id, test_date, min_ratings, description)
        VALUES(?,?,?,?)''', (nextSVDId, curDate, minRatings, 'Automatic Update'))

    for res in allResults:
        dbSql.execute('''INSERT INTO svdStatistics(
            id_block, n_epochs, lr_all, reg_all, rmse, mae, right_on, still_good, meh, bad)
            VALUES(?,?,?,?,?,?,?,?,?,?)''', (nextSVDId, res['inUse']['n_epochs'], res['inUse']['lr_all'],
                res['inUse']['reg_all'], res['rmse'], res['mae'], res['rightOn'], res['stillGood'], res['meh'], res['bad']))

    for userId in set(userData['id_user']):
        dbSql.execute('''INSERT INTO userStatistics(id_user, id_block)
        VALUES(?,?)''', (userId, nextSVDId))

maxThreads = 12
testValues = getInitialDistribution()
testChunks = [testValues[x:x+maxThreads] for x in range(0, len(testValues), maxThreads)]

allResults = []

for chunk in testChunks:
    result = []
    if len(chunk) > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
            for curResult in executor.map(runExternalProgram, chunk):
                result.append(ast.literal_eval(curResult))
    else:
        result.append(ast.literal_eval(runExternalProgram(chunk[0])))

    logger.debug("Result for chunk obtained:"+str(result))
    #convert string to dictionary
    allResults.extend(result)

logger.info("All Results: "+str(allResults))

os.remove(saveObtainedRaitingDataTo)

bestResult = allResults[0]
for result in allResults:
    if result['rmse'] < bestResult['rmse']:
        bestResult = result

logger.info('Best Result:')
logger.info(str(bestResult))

insertResultIntoDatabases(allResults, dbSql, ratings, minimumRatings)

# create prediction model from full dataset
logger.info("Training algorithm with full dataset")
fullTrainset = spRatingData.build_full_trainset()
svdAlgorithm = sp.SVD(n_epochs=bestResult['inUse']['n_epochs'],
    lr_all=bestResult['inUse']['lr_all'],reg_all=bestResult['inUse']['reg_all'])
svdAlgorithm.fit(fullTrainset)

# save model to file:
logger.info("Saving trained algorithm to: "+ str(saveTrainedModelTo))
with open(saveTrainedModelTo, 'wb') as svdModel:
    pickle.dump(svdAlgorithm, svdModel)

databaseConnection.commit()
databaseConnection.close()
