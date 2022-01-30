#!/usr/bin/python3

import sys
import sqlite3
import logging
from collections import Counter
from random import shuffle
from getSimilarFromContentBased import getSimilarFromContentBased
from getRecommendationFromSVD import getRecommendationFromSVD
from getInfoFromMovieIDs import getInfoFromMovieIDs

logger = logging.getLogger(__name__)

def getCombinedRecommendation(userId):
  logger.debug("in function getCombinedRecommendation: " + str(userId))
  contentBased = getSimilarFromContentBased(id=userId, listOfMovieIDs=True)
  logger.debug("Content based: "+str(contentBased))
  svdBased = []
  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  isUserInSVD = dbSql.execute('''
    SELECT count(userStatistics.id) FROM userStatistics INNER JOIN svdTrainBlock
      ON userStatistics.id = svdTrainBlock.id
      AND userStatistics.id = ?
      ORDER BY svdTrainBlock.test_date DESC LIMIT 1
    ''', (userId,)).fetchall()[0][0]
  if isUserInSVD != 0:
    svdBased = getRecommendationFromSVD(userId, listOfMovieIDs=True)
  logger.debug("SVD data: "+str(svdBased))

  # [] []
  result = contentBased.copy()
  result.extend(svdBased)
  result.sort(key=Counter(result).get, reverse=True)
  cnt = Counter(result)
  result = [k for k, v in cnt.items() if v > 1]
  for curMovie in result:
    if curMovie in contentBased: contentBased.remove(curMovie)
    if curMovie in svdBased: svdBased.remove(curMovie)

  contentBased.extend(svdBased)
  shuffle(contentBased)
  result.extend(contentBased)
  result = getInfoFromMovieIDs(result, dbSql)
  databaseConnection.close()
  return result

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/getCombinedRecommendation.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) == 2:
    logger.debug('In main of getCombinedRecommendation.py, argv: %s', sys.argv)
    print(getCombinedRecommendation(sys.argv[1]))
    sys.stdout.flush()
