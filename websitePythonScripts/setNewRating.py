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
  if idUser[0].isdigit():
    logger.debug('Adding new rating for the movie with id: %s for user with id: %s ', idMovie[0], idUser[0])
    # Verficar Si ya hay un rating para esa pelicula para ese usuario
    isMovieRated = dbSql.execute('''SELECT DISTINCT rating.rating FROM rating
                                      on rating.id_movie = ?
                                      and rating.id_user = ?''', (idMovie[0], idUser[0],)).fetchall()
    if isMovieRated is not None:
    # actualizarlo con update
      dbSql.execute('''UPDATE rating SET rating.rating = ? WHERE rating.id_user = ?''', (newRating[0], idUser[0],)).fetchall()
    # else:
    # no hay rating -> actualizarlo con la cantidad de strellas con insert
      # dbSql.execute('''INSERT INTO rating(rating)
      #                 VALUES(?)''').fetchall() cómo especifico el usuario

  # closing conection
  # databaseConnection.commit()
  databaseConnection.close()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, filemode='w', filename='logs/setNewRating.log', format='%(name)s - %(levelname)s - %(message)s')
  if len(sys.argv) >= 3:
    try:
      logger.debug('In main of setNewRating.py, argv: %s', sys.argv)
      print(setNewRating(sys.argv[1:]))
    except Exception as e:
      logger.critical(e)
    sys.stdout.flush()
