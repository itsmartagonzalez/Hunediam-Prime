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

filenameOfModel = '../trainedModels/svd__trained_model.sav'

# Create database conection
database = "../database/test.db"
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

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
    print("Own statistics: ", str(result))


splittedDataset = sp.model_selection.split.KFold(n_splits=5, random_state=None, shuffle=True)
svdAlgorithm = sp.SVD(n_epochs=5)
for trainset, testset in splittedDataset.split(spRatingData):
    #Training the algorithm:
    svdAlgorithm.fit(trainset)
    #predictions:
    predictions = svdAlgorithm.test(testset)
    getOwnStatistics(predictions)

    sp.accuracy.rmse(predictions, verbose=True)
    sp.accuracy.mae(predictions, verbose=True)












# Cross Validating:
# svd = sp.SVD(verbose=True, n_epochs=10)

# # Estimating best values:
# print('starting grid search...')
# param_grid = {'n_epochs': [5, 10, 15], 'lr_all': [0.002, 0.005, 0.01, 0.02], 'reg_all': [0.2, 0.4, 0.6]}
# #paramGrid = {'n_epochs': [1], 'lr_all': [0.002], 'reg_all': [0.4, 0.6]}
# gridSaerch = GridSearchCV(sp.SVD, paramGrid, measures=['rmse', 'mae'], cv=5)
# gridSaerch.fit(spRatingData)
#
# resultsFromGridSearch = pd.DataFrame.from_dict(gridSaerch.cv_results)
#
# #print complete results:
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(resultsFromGridSearch)
#
# print(gridSaerch.best_score['rmse'])
# # combination of parameters that gave the best RMSE score
# print(gridSaerch.best_params['rmse'])
#
# bestSVD = gridSaerch.best_estimator['rmse']



exit(0)



# # Train with Full Dataset:
# fullTrainset = spRatingData.build_full_trainset()
# svd.fit(fullTrainset)
#
# # save model to file:
# with open(filenameOfModel, 'wb') as svdModel:
#     pickle.dump(svd, svdModel)
#
# svd = False
#
# # load saved model:
# with open(filenameOfModel, 'rb') as svdModel:
#     svd = pickle.load(svdModel)
#
# def generateEstimatedRatingData(user_id, model):
#     for curMovieID in ratings['id_movie']:
#         prediction = model.predict(uid=user_id, iid=curMovieID, verbose=False)
#         if prediction.est > 3.0:
#             print(prediction)
#
# generateEstimatedRatingData(22, svd)
#
# databaseConnection.close()
