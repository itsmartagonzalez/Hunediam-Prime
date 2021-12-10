#!/usr/bin/python3.6

# SQLlite3 : https://docs.python.org/3/library/sqlite3.html

import sqlite3
import re

# Files

database = "database/test.db"

# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();

# SELECT titles from movies

# movieTitle = dbSql.execute('''SELECT movie.title FROM movie''').fetchall()
# print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")

# SELECT titles of movies from genre ...

# genre = "Comedy"
#
# movieTitle = dbSql.execute('''
#     SELECT movie.title FROM movie INNER JOIN movieGenres INNER JOIN genre
#         on movie.id = movieGenres.id_movie
#         and movieGenres.id_genre = genre.id
#         and genre.genre = ?
# ''', (genre,)).fetchall()
# print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")

# SELECT id and titles of movies from genre ... that have at least a rating of ...

# genre = "Crime"
# rating = 5.0
#
# movieTitle = dbSql.execute('''
#     SELECT movie.id, movie.title FROM movie INNER JOIN movieGenres INNER JOIN genre INNER JOIN rating
#         on movie.id = movieGenres.id_movie
#         and movieGenres.id_genre = genre.id
#         and movie.id = rating.id_movie
#         and genre.genre = ?
#         and rating.rating >= ?
# ''', (genre, rating,)).fetchall()
# print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")

# SELECT * from movies

movieTitle = dbSql.execute('''SELECT * FROM movie WHERE id=1''').fetchall()
print(movieTitle)
print("Found " + str(len(movieTitle)) + " Results")

# closing conection
databaseConnection.close()
