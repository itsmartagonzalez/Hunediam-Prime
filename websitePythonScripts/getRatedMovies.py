#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)

# movies = array of movie ID
def getRatedMovies(idUser):
  logger.debug('entered into getRatedMovies: %s', idUser)

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  movieInfo = {"movies":[]}
  if idUser[0].isdigit():
    logger.debug('Selecting rated movies for user with id: %s', idUser[0])
    moviesRated = dbSql.execute('''SELECT DISTINCT movie.id, movie.title, movie.overview, movie.image
                                    FROM movie INNER JOIN rating
                                    on movie.id = rating.id_movie
                                    AND rating.id_user = ?
                                    AND movie.overview NOT NULL
                                    AND movie.image NOT NULL LIMIT 30''', (idUser[0],)).fetchall()
  # closing conection
  databaseConnection.close()
  for movie in moviesRated:
    logger.debug(movie)
    currentMovie = {
      "id": str(movie[0]),
      "title": str(movie[1].encode('ascii', 'ignore')),
      #"overview": str(movie[2].encode('ascii', 'ignore')).replace('"', ''),
      "image": str(movie[3])
    }
    # currentMovie = {
    #   "id": str(re.sub(r'[^\x00-\x7f]', " ", movie[0])),
    #   "title": str(re.sub(r'[^\x00-\x7f]', " ", movie[1])),
    #   "overview": str(re.sub(r'[^\x00-\x7f]', " ", movie[2])),
    #   "image": str(re.sub(r'[^\x00-\x7f]', " ", movie[3]))
    # }
    # currentMovie = {
    #   "id": movie[0],
    #   "title": movie[1],
    #   "overview": movie[2],
    #   "image": movie[3]
    # }
    movieInfo["movies"].append(currentMovie)
  logger.debug('moviesRated for userID = ' + str(idUser) + ' : ' + str(movieInfo))
  movieInfo = str(movieInfo)
  return movieInfo

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getRatedMovies.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 1:
    try:
      logger.debug('In main of getRatedMovies.py, argv: %s', sys.argv)
      print(getRatedMovies(sys.argv[1:]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
