#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)

def getBestRatedMovies():
  logger.debug('entered into getBestRatedMovies')

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  logger.debug('Selecting best rated movies')    
  bestRatedMovies = dbSql.execute('''
      SELECT DISTINCT movie.id, movie.title, movie.overview, movie.image, avg(rating.rating) as avgR, count(rating.rating) as countR
        FROM movie INNER JOIN rating
          on movie.id = rating.id_movie
          and movie.overview NOT NULL
          and movie.image NOT NULL
          and rating.rating > 4
          GROUP BY movie.id ORDER BY countR DESC, avgR DESC LIMIT 200''').fetchall()

  # closing conection
  databaseConnection.close()
  bestRatedMoviesInfo = '{"movies" : ['
  for movie in bestRatedMovies:
    logger.debug(movie)
    currentMovie = '{'
    currentMovie += '"id" : '+ str(movie[0]) + ','
    currentMovie += '"title" : "' + str(movie[1]).replace('"', '')  + '",'
    currentMovie += '"overview" : "' + str(movie[2]).replace('"', '').replace("\\'", "'")  + '",'
    currentMovie += '"image" : "' + str(movie[3]) + '",'
    currentMovie += '"avg rating" : ' + str(movie[4]) + '},'
    bestRatedMoviesInfo += currentMovie
  bestRatedMoviesInfo = bestRatedMoviesInfo[:-1]
  bestRatedMoviesInfo += ']}'
  logger.warning(bestRatedMoviesInfo)
  logger.debug('bestMoviesRated :'  + str(bestRatedMoviesInfo))

  return bestRatedMoviesInfo

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getBestRatedMovies.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 1:
    try:
      logger.debug('In main of getBestRatedMovies.py, argv: %s', sys.argv)
      print(getBestRatedMovies())
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
