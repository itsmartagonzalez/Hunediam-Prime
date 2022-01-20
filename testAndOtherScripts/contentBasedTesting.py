#!/usr/bin/python3.6

#Applied: https://medium.com/analytics-vidhya/content-based-recommender-systems-in-python-2b330e01eb80

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import matplotlib.pyplot as plt


database = "database/test.db"
databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

#getting data for content bases recommendation (id, title, description)
#movies = dbSql.execute('''SELECT movie.id, movie.title, movie.overview FROM movie where movie.overview NOT NULL limit 50''').fetchall()
movies = dbSql.execute('''SELECT movie.id, movie.title, movie.overview FROM movie where movie.overview NOT NULL ORDER BY movie.id ASC''').fetchall()
movies = np.array(movies)



def getSimilarity(wordVector, movieID):
    overview_matrix = wordVector.fit_transform(movies[:,2].tolist())

    #Not sure whihc one is better
    similarity_matrix = cosine_similarity(overview_matrix, overview_matrix)
    #similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
    #print(overview_matrix)
    # plt.imshow(similarity_matrix);
    # plt.colorbar()
    # plt.show()

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
    tfidf = TfidfVectorizer(stop_words='english')
    return getSimilarity(tfidf, movieID)


#Count vectorizer testing
def cvTesting(movieID, movies=movies):
    cv = CountVectorizer(stop_words='english');
    return getSimilarity(cv, movieID)


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

databaseConnection.close()
