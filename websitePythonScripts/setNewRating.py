#!/usr/bin/python3

import sys
import sqlite3
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)

def setNewRating(idUser, idMovie, newRating):
  logger.debug('entered into setNewRating: %s', idUser)

  # connection to database
  database = "database/test.db"
  databaseConnection = sqlite3.connect(database)
  dbSql = databaseConnection.cursor()
  if idUser.isdigit():
    logger.debug("inside isDigit")
    isMovieRated = dbSql.execute('''SELECT DISTINCT count(rating.rating) FROM rating
                                      where rating.id_movie = ?
                                      and rating.id_user = ?''', (idMovie, idUser,)).fetchall()
    if isMovieRated[0][0] != 0:
      logger.debug('Changing rating to %s for the movie with id: %s for user with id: %s ', newRating, idMovie, idUser)
      dbSql.execute('''UPDATE rating SET rating = ? 
                       where rating.id_user = ?
                       and rating.id_movie = ?''', (newRating, idUser, idMovie)).fetchall()
    else:
      logger.debug('Adding new rating %s for the movie with id: %s for user with id: %s ', newRating, idMovie, idUser)
      dbSql.execute('''INSERT INTO rating(id_user, id_movie, rating) 
                   VALUES(?,?,?) ''',(idUser, idMovie, newRating,)).fetchall()
      logger.debug("INSERTED: "+str(dbSql.execute('''SELECT * FROM rating WHERE id_user = ? AND id_movie = ?''',(idUser, idMovie,)).fetchall()))        

  # closing conection
  # databaseConnection.commit()
  databaseConnection.close()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/setNewRating.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) == 4:
    try:
      logger.debug('In main of setNewRating.py, argv: %s', sys.argv)
      print(setNewRating(*sys.argv[1:]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
