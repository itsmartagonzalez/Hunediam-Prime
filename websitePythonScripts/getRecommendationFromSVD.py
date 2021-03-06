#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np
import pickle
import pandas as pd
from getInfoFromMovieIDs import getInfoFromMovieIDs

logger = logging.getLogger(__name__)


def generateEstimatedRatingData(user_id, model, ratings):
  for curMovieID in ratings['id_movie']:
    prediction = model.predict(str(user_id), str(curMovieID), verbose=False)
    #logger.debug(str(prediction))
    yield prediction

def getRecommendationFromSVD(userId, **kwargs):
  listOfMovieIDs = False
  logger.debug("arguments: " + str(userId) + " kwargs: " + str(kwargs))
  for k, v in kwargs.items():
    if k == 'listOfMovieIDs':
      listOfMovieIDs = v
  logger.debug('entered into getRecommendationFromSVD')
  numberOfMovies = 50

  filenameOfModel = 'trainedModels/svd_trained_model.sav'
  database = "database/test.db"

  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()

  notWatchedMovies = dbSql.execute('''
    SELECT DISTINCT id FROM movie WHERE id NOT IN (
      SELECT id_movie from rating where id_user = ?
    )
  ''', (userId,)).fetchall()
  notWatchedMovies = pd.DataFrame(notWatchedMovies, columns = ['id_movie'])
  logger.debug("Gotten not watched movies")
  logger.debug(notWatchedMovies['id_movie'].tolist())

  recommendations = ""
  with open(filenameOfModel, 'rb') as svdModel:
    svd = pickle.load(svdModel)
    result = []
    for movieRating in generateEstimatedRatingData(userId, svd, notWatchedMovies):
      result.append(movieRating)
    resultAsPD = pd.DataFrame(result, columns = ['user', 'item', 'r_ui', 'est', 'impossible'])
    resultAsPD = resultAsPD.sort_values(by='est', ascending=False)
    bestMovies = resultAsPD['item'].tolist()[:numberOfMovies]

    recommendations = getInfoFromMovieIDs(bestMovies, dbSql)
    recommendations = recommendations[:-1]
    isUserInSVD = dbSql.execute('''
    SELECT count(userStatistics.id) FROM userStatistics INNER JOIN svdTrainBlock
      ON userStatistics.id = svdTrainBlock.id
      AND userStatistics.id = ?
      ORDER BY svdTrainBlock.test_date DESC LIMIT 1
    ''', (userId,)).fetchall()[0][0]
    recommendations += ', "Approved" : ' + str(isUserInSVD) + '}'
    logger.debug(resultAsPD.to_numpy())
  
  databaseConnection.close()
  if listOfMovieIDs:
    return bestMovies
  else:
    return recommendations

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getRecommendationFromSVD.log', format='%(name)s - %(levelname)s - %(message)s')
  logger.debug("IN MAIN OF getRecommendationFromSVD outside IF")
  if len(sys.argv) == 2:
    try:
      logger.debug('In main of getRecommendationFromSVD.py, argv: %s', sys.argv)
      print(getRecommendationFromSVD(sys.argv[1]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()