#!/usr/bin/python3

import sqlite3

# Files

database = "../database/test.db"


# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();

dbSql.execute('''CREATE TABLE svdTrainBlock(
    id INTEGER PRIMARY KEY,
    test_date DATE NOT NULL,
    min_ratings INTEGER NOT NULL,
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
    FOREIGN KEY(id_block) REFERENCES svdTrainBlock(id),
    FOREIGN KEY(id_user) REFERENCES user(id))''')

databaseConnection.commit()
databaseConnection.close()
