#!/usr/bin/python3

import sys
import sqlite3
import logging

logger = logging.getLogger(__name__)
database = "database/test.db"

def newUserID():
  logger.debug('entered into newUserID')
  # connection to database
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  newUser = []
  dbSql.execute("INSERT INTO user(name) Values(NULL)") 
  newUser = dbSql.execute("SELECT MAX(id) FROM user").fetchall()
  logger.debug("new user = "+str(newUser))

  # commiting and closing conection
  databaseConnection.commit()
  databaseConnection.close()
  return newUser

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/newUserID.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 1:
    try:
      logger.debug('In main of newUserID.py, argv: %s', sys.argv)
      print(newUserID()[0][0])
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
