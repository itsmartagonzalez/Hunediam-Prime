#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np

logger = logging.getLogger(__name__)

def getAllMovies():
  logger.debug('entered into getAllMovies')
  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  movies = dbSql.execute("SELECT DISTINCT title FROM movie").fetchall()
  movies = np.array(movies)

  movieTitles = '{ "Titles" : ['
  for movie in movies:
    movieTitles += '"'+str(movie[0].encode('ascii', 'ignore').replace('"', ''))+'",'
  movieTitles = movieTitles[:-1]
  movieTitles += "]}"
  logger.debug('Movies ' + str(len(movieTitles)))


  # movieTitles = []
  # for movie in movies:
  #   movieTitles.append(str(movie[0].encode('ascii', 'ignore')))
  # logger.debug('Movies ' + str(movieTitles))
  # commiting and closing conection
  databaseConnection.close()
  return movieTitles

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/allMovies.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 1:
    try:
      logger.debug('In main of getAllMovies.py, argv: %s', sys.argv)
      print(getAllMovies())
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
