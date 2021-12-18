#!/usr/bin/python3.6

#Applied: https://medium.com/analytics-vidhya/content-based-recommender-systems-in-python-2b330e01eb80

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sqlite3
import re

database = "database/test.db"
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

#getting data for content bases recommendation (id, title, description)
#movies = dbSql.execute('''SELECT movie.id, movie.title, movie.overview FROM movie where movie.overview NOT NULL limit 50''').fetchall()
movies = dbSql.execute('''SELECT movie.id, movie.title, movie.overview FROM movie where movie.overview NOT NULL ORDER BY movie.id ASC''').fetchall()
movies = np.array(movies)
# print(movies[:,2])


def getSimilarity(similarity_matrix, movieID):
    #get similarity values with other movies
    #similarity_score is the list of index and similarity matrix
    similarity_score = list(enumerate(similarity_matrix[movieID]))
    #sort in descending order the similarity score of movie inputted with all the other movies
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    # Get the scores of the 15 most similar movies. Ignore the first movie.
    #similarity_score = similarity_score[1:15]
    #return movie names using the mapping series
    similarMovies = [i[0] for i in similarity_score]
    return similarMovies

def tfidfTesting(movieID, movies=movies):
    #creating ...
    tfidf = TfidfVectorizer(stop_words='english')
    #Construct the required TF-IDF matrix by applying the fit_transform method on the overview field of the movies
    overview_matrix = tfidf.fit_transform(movies[:,2].tolist())
    #Output the shape of tfidf_matrix
    # print(f"{overview_matrix.shape}")
    similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
    # print(similarity_matrix)
    return getSimilarity(similarity_matrix, movieID)


#Count vectorizer testing
def cvTesting(movieID, movies=movies):
    cv = CountVectorizer(stop_words='english');
    overview_matrix = cv.fit_transform(movies[:,2].tolist())
    cosine_sim = cosine_similarity(overview_matrix, overview_matrix)
    return getSimilarity(cosine_sim, movieID)


print(movies[:,1][0:20])
# passing movie id (index) into function to get similar movies
forId = 1
print()
similarMovies = tfidfTesting(forId)[1:10]
print("Similar movies for: " + movies[forId][1])
for id in similarMovies:
    print(movies[id][1])

print()
similarMovies = cvTesting(forId)[1:10]
print("Similar movies for: " + movies[forId][1])
for id in similarMovies:
    print(movies[id][1])
