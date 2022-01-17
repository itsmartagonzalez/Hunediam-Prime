#!/usr/bin/python3.6

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

filenameOfModel = '../trainedModels/svd_test_trained_data.sav'

database = "../database/test.db"
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

ratings = dbSql.execute('''SELECT id_user, id_movie, rating FROM rating''').fetchall()
ratings = pd.DataFrame(ratings, columns = ['id_user', 'id_movie', 'rating'])
#print(ratings)
spReader = sp.Reader(rating_scale=(1,5))
spData = sp.Dataset.load_from_df(ratings, spReader)

# Cross Validating:
svd = sp.SVD(verbose=True, n_epochs=10)
#sp.model_selection.cross_validate(svd, spData, measures=[u'rmse', u'mae'], cv=3, verbose=True)

# Full Dataset:
fullTrainset = spData.build_full_trainset()
svd.fit(fullTrainset)

# save model to file:
with open(filenameOfModel, 'wb') as svdModel:
    pickle.dump(svd, svdModel)

svd = False

# load saved model:
with open(filenameOfModel, 'rb') as svdModel:
    svd = pickle.load(svdModel)

def generateEstimatedRatingData(user_id, model):
    for curMovieID in ratings['id_movie']:
        prediction = model.predict(uid=user_id, iid=curMovieID, verbose=False)
        if prediction.est > 3.0:
            print(prediction)

generateEstimatedRatingData(22, svd)

databaseConnection.close()
