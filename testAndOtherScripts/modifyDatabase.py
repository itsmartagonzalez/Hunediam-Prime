#!/usr/bin/python3

import sqlite3

# Files

database = "../database/test.db"


# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();

dbSql.execute('''CREATE TABLE contentBasedSimilar(
    id INTEGER PRIMARY KEY,
    id_movie INTEGER NOT NULL,
    id_similar_movie INTEGER NOT NULL,
    FOREIGN KEY(id_movie) REFERENCES movie(id),
    FOREIGN KEY(id_similar_movie) REFERENCES movie(id))''')

databaseConnection.commit()
databaseConnection.close()
