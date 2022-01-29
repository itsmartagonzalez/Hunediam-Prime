#!/usr/bin/python3.6

#Applied: https://medium.com/analytics-vidhya/content-based-recommender-systems-in-python-2b330e01eb80

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import matplotlib.pyplot as plt
from collections import Counter
import logging

import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


database = "../database/test.db"
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor()


limitHowManyMovies = 20


def getMovieData(dbSql):
    movies = dbSql.execute('''SELECT movie.id, movie.title, movie.overview FROM movie ORDER BY movie.id ASC''').fetchall()

    movies = np.array(movies)

    logger.debug("Finished movies select")

    # Adding genre to movies
    for movie in movies:
        genres = dbSql.execute('''SELECT DISTINCT genre.genre FROM genre INNER JOIN movieGenres INNER JOIN movie
                                    on movie.id = movieGenres.id_movie
                                    and movieGenres.id_genre = genre.id
                                    and movie.id == ?''', (int(movie[0]),)).fetchall()
        genres = np.array(genres)
        strConvertedGenres = " "
        for genre in genres:
            strConvertedGenres += "-".join(genre[0].split()) + " "
        if movie[2] is not None:
            movie[2] += strConvertedGenres
        else:
            movie[2] = strConvertedGenres

    logger.debug("Finished movies adding genres")

    # Adding cast to movie
    for movie in movies:
        actors = dbSql.execute('''SELECT DISTINCT actor.name FROM actor INNER JOIN movieActor INNER JOIN movie
                                    on movie.id = movieActor.id_movie
                                    and movieActor.id_actor = actor.id
                                    and movie.id == ?''', (int(movie[0]),)).fetchall()
        actors = np.array(actors)
        strConvertedActor = ". "
        for actor in actors:
            strConvertedActor += "-".join(actor[0].split()) + " "
        if movie[2] is not None:
            movie[2] += strConvertedActor
        else:
            movie[2] = strConvertedActor
    return movies

    logger.debug("Finished movies adding actors")


def getSimilarity(wordVector, movieIDs, movies):
    overview_matrix = wordVector.fit_transform(movies[:,2].tolist())
    similarity_matrix = cosine_similarity(overview_matrix, overview_matrix)
    #similarity_matrix = linear_kernel(overview_matrix,overview_matrix)

    for pos in movieIDs:
        similarity_score = list(enumerate(similarity_matrix[pos]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similarMovies = [i[0] for i in similarity_score]
        yield similarMovies

def tfidfTesting():
    return TfidfVectorizer(stop_words='english')

#Count vectorizer testing
def cvTesting():
    return CountVectorizer(stop_words='english')

def updateDatabaseToContainNewResults(forMovie, similarMovies, dbSql):
    numberInDatabse = dbSql.execute('''SELECT DISTINCT count(id_similar_movie) FROM contentBasedSimilar
        WHERE id_movie = ?''', (forMovie,)).fetchall()[0][0]

    numberOfUpdates = min(numberInDatabse, limitHowManyMovies)
    numberOfNewInserts = limitHowManyMovies-numberInDatabse
    numberOfDeletions = 0
    if numberOfNewInserts < 0:
        numberOfDeletions = abs(numberOfNewInserts)
        numberOfNewInserts = 0

    similarMovieToInsert = 0

    # Update existing entries
    toUpdate = dbSql.execute('''SELECT DISTINCT contentBasedSimilar.id FROM contentBasedSimilar
        WHERE id_movie = ? ORDER BY contentBasedSimilar.id ASC''', (forMovie,)).fetchall()
    toUpdate = np.array(toUpdate)
    for idToUpdate in toUpdate:
        dbSql.execute('''UPDATE contentBasedSimilar SET id_movie = ?, id_similar_movie = ?
            WHERE id = ?''', (forMovie, similarMovies[similarMovieToInsert], idToUpdate[0],))
        similarMovieToInsert += 1
        # update user
    # Insert new ones to to have limitHowManyMovies in database
    for i in range(0, numberOfNewInserts):
        dbSql.execute('''INSERT INTO contentBasedSimilar(id_movie, id_similar_movie)
            VALUES(?,?)''', (forMovie, similarMovies[similarMovieToInsert],))
            similarMovieToInsert += 1
        # number of new inserts

    # delete excess entries
    toDelete = dbSql.execute('''SELECT DISTINCT contentBasedSimilar.id FROM contentBasedSimilar
        WHERE id_movie = ? ORDER BY contentBasedSimilar.id DESC limit ?''', (forMovie, numberOfDeletions,)).fetchall()
    toDelete = np.array(toDelete)
    for idToDelete in toDelete:
        dbSql.execute('''DELETE FROM contentBasedSimilar WHERE id = ?''', (idToDelete[0],))


def checkResultForSingleMovie(forMovie, similarMovies, dbSql):
    logger.debug("checkResultForSingleMovie:"+str(forMovie)+' similar:'+str(similarMovies))

    # averageRating = dbSql.execute('''SELECT avg(rating.rating) FROM rating
    #                           where rating.id_user IN (
    #                               SELECT rating.id_user FROM rating where rating.id_movie = ?)''',
    #                                 (forMovie,)).fetchall()

    # moviesWatched = dbSql.execute('''SELECT rating.id_movie, rating.rating FROM rating
    #                                 where rating.id_user IN (
    #                                     SELECT rating.id_user FROM rating
    #                                     where rating.rating >= ? and rating.id_movie = ?)''', (averageRating[0][0], forMovie,)).fetchall()


    moviesWatched = dbSql.execute('''SELECT rating.id_movie, rating.rating FROM rating
                                    WHERE rating.id_user IN (
                                        SELECT rating.id_user FROM rating
                                        WHERE rating.id_movie = ? and rating.rating >= (
                                            SELECT avg(rating.rating) FROM rating where rating.id_movie = ?)
                                        )''', (forMovie, forMovie,)).fetchall()


    # logger.debug(str(moviesLiked))
    estimationStatistics = Counter({'good': 0, 'bad':0})
    moviesWatched = np.array(moviesWatched) #moviesLiked
    logger.debug(str(moviesWatched)) #moviesLiked
    if len(moviesWatched) > 0:
        for curMovie in similarMovies:
            if curMovie in moviesWatched[:,0]:  #moviesLiked
                index = np.where(moviesWatched[:,0] == curMovie)[0]
                if np.any([ x >= ratingAbove for x in moviesWatched[index, 1]]):
                    estimationStatistics['good'] += 1
                else:
                    estimationStatistics['bad'] += 1
            logger.debug("Estimation statistics for singleMovie: " + str(estimationStatistics))
    return estimationStatistics

def getStatisticsForAllMovies(movies, dbSql, estimatorFunction):
    estimationStatistics = Counter({'good': 0, 'bad':0})
    posInArr = 0;
    for similarMovies in getSimilarity(estimatorFunction(), range(0, len(movies)), movies):
        limitedSimilarMovies = similarMovies[1:limitHowManyMovies+1]
        similarMoviesDBIds = [movies[x][0] for x in limitedSimilarMovies]
        statisticForSingleMovie = checkResultForSingleMovie(movies[posInArr][0], similarMoviesDBIds, dbSql)
        estimationStatistics += statisticForSingleMovie
        logger.info("Movie id:"+str(movies[posInArr][0])+' raw: '+str(statisticForSingleMovie)+
            ' --> '+str(calculatePercentage(statisticForSingleMovie) * 100.) + "%")
        posInArr += 1
    return estimationStatistics

def calculatePercentage(estimationStatistics):
    percentage = 0
    if estimationStatistics['good'] > 0 or estimationStatistics['bad'] > 0:
        percentage = estimationStatistics['good'] / (estimationStatistics['good'] + estimationStatistics['bad'])
    return percentage

movies = getMovieData(dbSql)
# print(movies[0:2])

# tfidfTesting: 65.24580926891112%
TfidfVectorizerStats = getStatisticsForAllMovies(movies, dbSql, tfidfTesting)
CountVectorizerStats = getStatisticsForAllMovies(movies, dbSql, cvTesting)

logger.info("Porcentaje de acierto usando tfidfTesting: " + str(calculatePercentage(TfidfVectorizerStats) * 100.) + "%")
logger.info("Porcentaje de acierto usando cvTesting: " + str(calculatePercentage(CountVectorizerStats) * 100.) + "%")

databaseConnection.close()
