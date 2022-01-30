#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)

def getAmountOfRatedMovies(idUser):
  logger.debug('entered into getAmountOfRatedMovies: %s', idUser)

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  if idUser[0].isdigit():
    logger.debug('Selecting count of rated movies for user with id: %s', idUser[0])
    moviesCount = dbSql.execute('''SELECT count(DISTINCT movie.id)
                                    FROM movie INNER JOIN rating
                                    on movie.id = rating.id_movie
                                    AND rating.id_user = ?
                                    AND movie.overview NOT NULL
                                    AND movie.image NOT NULL''', (idUser[0],)).fetchall()

  # closing conection
  databaseConnection.close()

  logger.debug('Count ofmoviesRated for userID = ' + str(idUser) + ' : ' + str(moviesCount))
  #movieInfo = str(movieInfo)
  return moviesCount

if __name__ == '__main__':
  logging.basicConfig(level=logging.WARNING, filemode='w', filename='logs/getAmountOfRatedMovies.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 1:
    try:
      logger.debug('In main of getAmountOfRatedMovies.py, argv: %s', sys.argv)
      print(getAmountOfRatedMovies(sys.argv[1:]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
