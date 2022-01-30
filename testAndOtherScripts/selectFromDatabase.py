#!/usr/bin/python3.6

# SQLlite3 : https://docs.python.org/3/library/sqlite3.html

import sqlite3
import re
import pandas as pd

# Files

database = "../database/test.db"

# connection to database

databaseConnection = sqlite3.connect(database)

dbSql = databaseConnection.cursor();

# SELECT titles from movies

# movieTitle = dbSql.execute('''SELECT movie.title FROM movie''').fetchall()
# print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")

# SELECT titles of movies from genre ...

genre = "Comedy"
#
#movieTitle = dbSql.execute('''
#    SELECT * FROM movie INNER JOIN movieGenres INNER JOIN genre
#        on movie.id = movieGenres.id_movie
#        and movieGenres.id_genre = genre.id
#        and genre.genre = ?
#''', (genre,)).fetchall()
#print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")


# movieTitle = dbSql.execute('''SELECT count(*) FROM movie where overview IS NULL''').fetchall()
# print(movieTitle)

minimumRatings = 20 # minimum count of ratings per user in our data base

ratings = dbSql.execute('''WITH tmpRatings AS (SELECT id_user, rating FROM rating
                            GROUP BY id_user
                            HAVING count(rating) >= ?)
                            SELECT rating.id_user, rating.id_movie, rating.rating FROM rating INNER JOIN tmpRatings
                            on rating.id_user = tmpRatings.id_user
                            ''', (minimumRatings,)).fetchall()

# print(ratings[:10])
# print(len(ratings))
ratings = pd.DataFrame(ratings, columns = ['id_user', 'id_movie', 'rating'])

# ratings = dbSql.execute('''SELECT MIN(mycount) FROM (SELECT id_user, count(rating) mycount FROM rating GROUP BY id_user)''').fetchall()

# SVD Statistics

svdStatistics = dbSql.execute('''SELECT * FROM svdStatistics''').fetchall()
# print(svdStatistics)

# SVD ID BLOCK
idBlock = 2
svdStatistics = dbSql.execute('''SELECT * FROM svdStatistics WHERE id_block = ? ''', (idBlock,)).fetchall()

# print(svdStatistics)


# Get users 

forMovie = 1
ratingAbove = 5
# select movies with similar rating from the same users
# wellRatedMovies = dbSql.execute('''WITH tmpSelectedUsers AS (SELECT id_user
#                                                                 FROM rating
#                                                                 WHERE id_movie = ? and rating.rating >= ?)
#                                     SELECT count(rating.id_movie)
#                                     FROM rating INNER JOIN tmpSelectedUsers
#                                     on rating.id_user = tmpSelectedUsers.id_user
#                                     where rating.rating >= ?''', (forMovie, ratingAbove, ratingAbove,)).fetchall()

# print(wellRatedMovies)

# sameFromUsers = dbSql.execute('''SELECT count(rating.id_movie) FROM rating 
#                               where rating.rating >= ? and rating.id_user IN (SELECT rating.id_user FROM rating
#                                 where rating.rating >= ? and rating.id_movie = ?)''', (ratingAbove, ratingAbove, forMovie,)).fetchall()
# print(sameFromUsers)

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

# movieTitle = dbSql.execute('''SELECT * FROM movie WHERE id=1''').fetchall()
# print(movieTitle)
# print("Found " + str(len(movieTitle)) + " Results")


bestRatedMovies = dbSql.execute('''
    SELECT DISTINCT movie.id, movie.title, movie.overview, movie.image, avg(rating.rating) as avgR 
      FROM movie INNER JOIN rating
        on movie.id = rating.id_movie
        and movie.overview NOT NULL
        and movie.image NOT NULL
        GROUP BY movie.id ORDER BY avgR DESC LIMIT 50''').fetchall()

print(bestRatedMovies)

# closing conection
databaseConnection.close()
