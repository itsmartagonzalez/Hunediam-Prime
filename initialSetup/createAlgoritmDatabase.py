#!/usr/bin/python3

# SQLlite3 : https://docs.python.org/3/library/sqlite3.html

import sqlite3
import re
import logging

logger = logging.getLogger(__name__)

def createAlgorithmDatabase(database):

    # connection to database
    databaseConnection = sqlite3.connect(database)
    dbSql = databaseConnection.cursor()

    # create tables:
    dbSql.execute('''CREATE TABLE svdTrainBlock(
        id INTEGER PRIMARY KEY,
        test_date DATE NOT NULL,
        description TEXT DEFAULT NULL)''')
    dbSql.execute('''CREATE TABLE svdStatistics(
        id INTEGER PRIMARY KEY,
        id_block INTEGER NOT NULL,
        n_epochs INTEGER NOT NULL,
        lr_all FLOAT NOT NULL,
        reg_all FLOAT NOT NULL,
        rmse FLOAT NOT NULL,
        mae FLOAT NOT NULL,
        right_on FLOAT DEFAULT NULL,
        still_good FLOAT DEFAULT NULL,
        meh FLOAT DEFAULT NULL,
        bad FLOAT DEFAULT NULL,
        FOREIGN KEY(id_block) REFERENCES svdTrainBlock(id))''')
    dbSql.execute('''CREATE TABLE userStatistics(
        id INTEGER PRIMARY KEY,
        id_user INTEGER NOT NULL,
        id_block INTEGER NOT NULL,
        amountOfRatings INTEGER DEFAULT NULL,
        FOREIGN KEY(id_block) REFERENCES svdTrainBlock(id),
        FOREIGN KEY(id_user) REFERENCES user(id))''')
    # commiting and closing conection
    databaseConnection.commit()
    databaseConnection.close()
    logger.info("Database for algorithm statistics was succesfully created")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.debug('In main of createAlgoritmDatabase.py')
    createAlgorithmDatabase("database/trainStatistics.db")
