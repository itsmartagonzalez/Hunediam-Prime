#!/usr/bin/python3

import sqlite3
import datetime

# Files

database = "../database/test.db"


# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();


curDate = datetime.datetime.now()
dbSql.execute("INSERT INTO svdTrainBlock(id, test_date, min_ratings, description) VALUES(?,?,?,?)", (1, curDate, 1, 'Testing insert'))

databaseConnection.commit()
databaseConnection.close()
