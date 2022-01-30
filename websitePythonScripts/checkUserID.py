#!/usr/bin/python3

import sys
import sqlite3
import logging

logger = logging.getLogger(__name__)

def checkUserID(userId):
  logger.debug('entered into checkUserID: %s', userId)
  database = "database/test.db"
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  user = []
  if userId[0].isdigit():
    user = dbSql.execute("SELECT DISTINCT count(id) FROM user WHERE id = ?", (userId[0],)).fetchall()
    logger.debug('UserId ' + str(userId) + ' with count = ' + str(user))
  # commiting and closing conection
  databaseConnection.close()
  return user

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/checkuser.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 2:
    try:
      logger.debug('In main of checkUserID.py, argv: %s', sys.argv)
      print(checkUserID(sys.argv[1:])[0][0])
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
