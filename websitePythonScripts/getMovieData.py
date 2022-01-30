#!/usr/bin/python3

import sys
import sqlite3
import logging

logger = logging.getLogger(__name__)

def getMovieData(movieTitle):
  logger.debug('enetered into getMovieData for movie: %s', movieTitle)

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  movie = dbSql.execute("SELECT * FROM movie WHERE title = ?", (movieTitle,)).fetchall()[0]

  movieInfo = '{"id" : '+ str(movie[0]) + ','
  movieInfo += '"title" : "' + str(movie[1].encode('ascii', 'ignore')).replace('"', '')  + '",'
  movieInfo += '"overview" : "' + str(movie[2].encode('ascii', 'ignore')).replace('"', '')  + '",'
  movieInfo += '"image" : "' + str(movie[3]) + '"}'
  logger.debug('Selected movie: %s', str(movieInfo))
  # commiting and closing conection
  databaseConnection.close()
  return movieInfo

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getMovieData.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) == 2:
    logger.debug('In main of getMovieData.py, argv: %s', sys.argv)
    print(getMovieData(sys.argv[1]))
    sys.stdout.flush()
