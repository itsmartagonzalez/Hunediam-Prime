#!/usr/bin/python3

import sys
import sqlite3
import logging
from collections import Counter
from getInfoFromMovieIDs import getInfoFromMovieIDs

logger = logging.getLogger(__name__)

# gets similar movies to the ones in args,
# define id_user = ... to only get movies that user hasn't seen yet
def getSimilarFromContentBased(*args, **kwargs):
  ratingAbove = 3.5
  logger.debug('entered into getSimilarFromContentBased')
  similarForMovies = [x for x in args]
  currentUser = None
  logger.debug("arguments: " + str(args) + " kwargs: " + str(kwargs))
  for k, v in kwargs.items():
    if k == 'id':
      currentUser = v

  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  logger.debug("connected to database")
  similarToMovies = []
  similarToMoviesRatedAbove = []
  if currentUser != None:
    logger.debug("Starting with user id")
    similarToMoviesRatedAbove = dbSql.execute('''
      SELECT contentBasedSimilar.id_similar_movie as movieID , count(contentBasedSimilar.id_similar_movie) as timesItAppears
        FROM contentBasedSimilar INNER JOIN rating INNER JOIN movie
          ON movie.id = rating.id_movie AND contentBasedSimilar.id_movie = movie.id
          AND rating.id_user = ? AND rating.rating >= ?
          AND movie.image NOT NULL
          AND contentBasedSimilar.id_similar_movie NOT IN (
            SELECT DISTINCT id_movie FROM rating WHERE id_user = ?
          ) GROUP BY movieID ORDER BY timesItAppears DESC LIMIT 50''', (currentUser, ratingAbove, currentUser,)).fetchall()
    logger.debug("Got values for user watch similar movies")
    for simMovieFor in args:
      simMovie = dbSql.execute('''
        SELECT DISTINCT contentBasedSimilar.id_similar_movie
          FROM contentBasedSimilar INNER JOIN movie INNER JOIN rating
            ON contentBasedSimilar.id_movie = movie.id AND movie.id = rating.id_movie
              AND contentBasedSimilar.id_movie = ?
              AND movie.image NOT NULL
                AND contentBasedSimilar.id_similar_movie NOT IN (
                  SELECT DISTINCT id_movie FROM rating WHERE id_user = ?
                ) LIMIT 50
        ''', (simMovieFor, currentUser,)).fetchall()
      similarToMovies.append(simMovie)
    logger.debug("Gotten values for similar movies passed as args")
  else:
    logger.debug("Only get similar movies like the ones in arguments: "+str(similarForMovies))
    for simMovieFor in similarForMovies:
      simMovie = dbSql.execute('''
        SELECT DISTINCT id_similar_movie FROM contentBasedSimilar WHERE id_movie = ? LIMIT 50''', (simMovieFor,)).fetchall()
      similarToMovies.append(simMovie)

  logger.debug("Finished with getting data")
  result = []
  for movieUser in similarToMoviesRatedAbove:
    for times in range(0, movieUser[1]):
      result.append(movieUser[0])
  logger.debug("Finished adding user based data")
  for movieRes in similarToMovies:
    for curMovieInRes in movieRes:
      result.append(curMovieInRes[0])
  result.sort(key=Counter(result).get, reverse=True)
  result = list(dict.fromkeys(result))

  logger.debug("result movies: "+str(result))

  movieInfo = getInfoFromMovieIDs(result, dbSql)

  # closing conection
  databaseConnection.close()
  return movieInfo

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getSimilarFromContentBased.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 2:
    try:
      logger.debug('In main of getSimilarFromContentBased.py, argv: %s', sys.argv)
      if sys.argv[-1][0] == 'i':
        logger.debug('Kwargs present')
        print(getSimilarFromContentBased(*sys.argv[1:len(sys.argv)-1], **dict(arg.split('=') for arg in sys.argv[len(sys.argv)-1:])))
      else:
        logger.debug('NO Kwargs')
        print(getSimilarFromContentBased(*sys.argv[1:]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
