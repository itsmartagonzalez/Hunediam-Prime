#!/usr/bin/python3.6

# SQLlite3 : https://docs.python.org/3/library/sqlite3.html

import sqlite3
import re

# Files

database = "database/test.db"
movieFile = "data/movies.csv"
ratingFile = "data/ratings.csv"

# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();

# create tables:

dbSql.execute('''CREATE TABLE movie(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    overview TEXT DEFAULT NULL,
    image TEXT DEFAULT NULL)''')
dbSql.execute("CREATE TABLE genre(id INTEGER PRIMARY KEY, genre TEXT UNIQUE NOT NULL)")
dbSql.execute('''CREATE TABLE movieGenres(
    id INTEGER PRIMARY KEY,
    id_movie INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    FOREIGN KEY(id_movie) REFERENCES movie(id),
    FOREIGN KEY(id_genre) REFERENCES genre(id))''')

dbSql.execute("CREATE TABLE user(id INTEGER PRIMARY KEY, name TEXT DEFAULT NULL)")

dbSql.execute('''CREATE TABLE rating(
    id INTEGER PRIMARY KEY,
    id_user INTEGER NOT NULL,
    id_movie INTEGER NOT NULL,
    rating FLOAT DEFAULT NULL,
    time INTEGER DEFAULT NULL,
    FOREIGN KEY(id_user) REFERENCES user(id),
    FOREIGN KEY(id_movie) REFERENCES movie(id))''')

dbSql.execute("CREATE TABLE cast(id INTEGER PRIMARY KEY, name TEXT DEFAULT NULL)")
dbSql.execute('''CREATE TABLE movieCast(
    id INTEGER PRIMARY KEY,
    id_movie INTEGER NOT NULL,
    id_cast INTEGER NOT NULL,
    FOREIGN KEY(id_movie) REFERENCES movie(id),
    FOREIGN KEY(id_cast) REFERENCES cast(id))''')

# Insert Data:
# Insert Movie data:

print("Inserting movie data")

with open(movieFile, newline='') as movies:
    #Only ASCII will be inserted correctly so we remove other characters
    movieData = re.sub(r'[^\x00-\x7f]',r' ', movies.read())
    movieData = movieData.splitlines()
    genres = set();
    cleanMovieData = []

    # insert movies:
    for i in range(1, len(movieData)):
        curLine = movieData[i].split(',')
        if len(curLine) > 3:
            curLine = [curLine[0], ','.join(curLine[1:len(curLine)-1]).strip('"'), curLine[len(curLine)-1]]
        cleanMovieData.append([curLine[0], curLine[1], curLine[2].split('|')])
        genres.update([genre for genre in curLine[2].split('|')])

    # insert genres:
    for genre in genres:
        dbSql.execute("INSERT INTO genre(genre) VALUES(?)", (genre,))

    for movie in cleanMovieData:
        # insert movies and create relationship between movies and genres
        dbSql.execute("INSERT INTO movie(id, title) VALUES(?,?)", (int(movie[0]), movie[1],))
        for genre in movie[2]:
            genreId = dbSql.execute("SELECT id FROM genre WHERE genre=?", (genre,)).fetchall()
            if len(genreId) > 0:
                dbSql.execute("INSERT INTO movieGenres(id_movie, id_genre) VALUES(?,?)", (int(movie[0]), int(genreId[0][0]),))

# Insert rating data:

print("Inserting rating data")

with open(ratingFile, newline='') as ratings:
    ratingData = re.sub(r'[^\x00-\x7f]',r' ', ratings.read())
    ratingData = ratingData.splitlines()
    ratingData.pop(0)

    for rating in ratingData:
        rating = rating.split(',')
        #check if user exists
        userId = dbSql.execute("SELECT id FROM user WHERE id=?", (int(rating[0]),)).fetchall()
        if len(userId) == 0:
            dbSql.execute("INSERT INTO user(id) VALUES(?)", (int(rating[0]),))
        dbSql.execute("INSERT INTO rating(id_user, id_movie, rating, time) VALUES(?,?,?,?)", (int(rating[0]), int(rating[1]), float(rating[2]), int(rating[3]),))


# commiting and closing conection
databaseConnection.commit()
databaseConnection.close()
