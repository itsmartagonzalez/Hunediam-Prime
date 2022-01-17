#!/usr/bin/python3

import sys
import sqlite3
import logging

logger = logging.getLogger(__name__)

# movies = array of movie ID
def getMovieData(movies):
  logger.debug('enetered into getMovieData: %s', movies)

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  movieInfo = {}
  for movieID in movies:
    if movieID.isdigit():
      logger.debug('Select movie with id: %s', movieID)
      select = dbSql.execute("SELECT * FROM movie WHERE id = ?", movieID).fetchall()
      if len(select) > 0:
        movieInfo[movieID] = select[0]
  return movieInfo

if __name__ == '__main__':
  if len(sys.argv) >= 2:
    logging.basicConfig(level=logging.ERROR)
    logger.debug('In main of getMovieData.py, argv: %s', sys.argv)
    print(getMovieData(sys.argv[1:]))
    sys.stdout.flush()
