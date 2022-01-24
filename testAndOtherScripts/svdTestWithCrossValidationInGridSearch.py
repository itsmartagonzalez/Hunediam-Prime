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
from surprise.model_selection import GridSearchCV
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

# Cross Validating:
svd = sp.SVD(verbose=True, n_epochs=10)

# Estimating best values:
print('starting grid search...')
paramGrid = {'n_epochs': [5, 10, 15], 'lr_all': [0.002, 0.005, 0.01, 0.02], 'reg_all': [0.2, 0.4, 0.6]}
#paramGrid = {'n_epochs': [1], 'lr_all': [0.002], 'reg_all': [0.4, 0.6]}
gridSaerch = GridSearchCV(sp.SVD, paramGrid, measures=['rmse', 'mae'], cv=5)
gridSaerch.fit(spRatingData)

resultsFromGridSearch = pd.DataFrame.from_dict(gridSaerch.cv_results)

#print complete results:
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(resultsFromGridSearch)

print('Results:')
print(gridSaerch.best_score['rmse'])
# combination of parameters that gave the best RMSE score
print(gridSaerch.best_params['rmse'])

bestSVD = gridSaerch.best_estimator['rmse']



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
