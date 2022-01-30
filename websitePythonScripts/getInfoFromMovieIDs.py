#!/usr/bin/python3

import sys
import sqlite3
import logging
from collections import Counter

logger = logging.getLogger(__name__)

# gets similar movies to the ones in args,
# define id_user = ... to only get movies that user hasn't seen yet
def getInfoFromMovieIDs(movieIds, dbSql):
  logger.debug('entered into getInfoFromMovieIDs')

  resultWithData = []
  for movieID in movieIds:
    movieInfoSel = dbSql.execute('''SELECT DISTINCT * FROM movie WHERE id = ? LIMIT 50''', (movieID,)).fetchall()
    logger.debug("RESULT MOVIE DATA: "+str(movieInfoSel))
    if movieInfoSel[0][3]:
      resultWithData.append(movieInfoSel[0])
  
  logger.info("Found: " + str(len(resultWithData))+" MOVIES")
  movieInfo = '{"movies" : ['
  for movie in resultWithData:
    logger.debug(movie)
    currentMovie = '{'
    currentMovie += '"id" : '+ str(movie[0]) + ','
    currentMovie += '"title" : "' + str(movie[1]).replace('"', '')  + '",'
    currentMovie += '"overview" : "' + str(movie[2]).replace('"', '').replace("\\'", "'")  + '",'
    currentMovie += '"image" : "' + str(movie[3]) + '"},'
    movieInfo += currentMovie

  movieInfo = movieInfo[:-1]
  movieInfo += ']}'

  return movieInfo

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getInfoFromMovieID.log', format='%(name)s - %(levelname)s - %(message)s')
  logger.warning("THIS FILE CAN ONLY BE RUN FROM OTHER FILES")
