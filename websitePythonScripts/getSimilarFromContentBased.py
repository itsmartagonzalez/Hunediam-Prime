#!/usr/bin/python3

import sys
import sqlite3
import logging

logger = logging.getLogger(__name__)
ratingAbove = 4

# gets similar movies to the ones in args,
# define id_user = ... to only get movies that user hasn't seen yet
def getSimilarFromContentBased(*args, **kwargs):
  logger.debug('entered into getSimilarFromContentBased: %s', userId)
  similarForMovies = [x for x in args]
  currentUser = None
  for k, v in kwargs.iteritems():
    if k == 'id':
      currentUser = v

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()

  similarToMoviesRatedAbove = None
  if currentUser != None:
    similarToMoviesRatedAbove = dbSql.execute('''SELECT movie.id FROM movie INNER JOIN ''')





  if userId[0].isdigit():
    user = dbSql.execute("SELECT DISTINCT count(id_user) FROM rating WHERE id_user = ?", (userId[0],)).fetchall()
    logger.debug('UserId ' + str(userId))
    # commiting and closing conection
  databaseConnection.close()
  return user

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getSimilarFromContentBased.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 2:
    try:
      logger.debug('In main of getSimilarFromContentBased.py, argv: %s', sys.argv)
      print(checkUserID(sys.argv[1:])[0][0])
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
