import pandas as pd
from pymongo import MongoClient
import numpy as np

def iicf(username):

    client = MongoClient()

    # point the client at mongo URI
    client = MongoClient('mongodb://db_username:db_password_12345@moviers-shard-00-00-3hnlg.mongodb.net:27017,moviers-shard-00-01-3hnlg.mongodb.net:27017,moviers-shard-00-02-3hnlg.mongodb.net:27017/moviers?ssl=true&replicaSet=moviers-shard-0&authSource=admin&retryWrites=true')
    
    # select database
    db = client['moviers']
    global person
    # select the collection within the database
    ratings_mongodb = db.user_ratings_100836_test
    # convert entire collection to Pandas dataframe
    ratings = pd.DataFrame(list(ratings_mongodb.find()))

    ratings_only = ratings.drop(['_id', 'userId'], axis = 1)

    ratings_only = ratings_only.apply(pd.to_numeric)


    ratings_only = ratings_only.replace(np.nan, 0)

    ratings_only_t = ratings_only.T


    person_username = username

    a = list(ratings.T.loc["userId"])
    list_of_all_movies = list(ratings_only)

    for i in range(len(a)):
        if a[i] == person_username:
            person = i

    user_rated_movies = []

    for movie in ratings_only_t.T:
        yield 'a'
        if ratings_only.iloc[person][movie] != 0.0 and str(movie) in list_of_all_movies:
            user_rated_movies.append(str(movie))


    ratings_only_user = ratings_only[user_rated_movies]

    ratings_only_drop = (ratings_only.T.drop(user_rated_movies)).T

    corr_all_scores = []
    for seen_movie in user_rated_movies:
        yield 'a'
        corr_movie_i = ratings_only_drop.corrwith(ratings_only_user.loc[:, seen_movie])
        corr_all_scores.append(corr_movie_i)

    # get ratings list
    ratings_list = []
    for seen_movie in user_rated_movies:
        yield 'a'
        ratings_list.append(ratings_only.iloc[person][seen_movie])

    corr_all_scores_df = pd.DataFrame(corr_all_scores)

    corr_all_scores_df[corr_all_scores_df < 0] = 0


    denominator_for_all_movies = corr_all_scores_df.sum(axis=0)


    multiply_rating_by_similarity_scores = corr_all_scores_df.mul(ratings_list, axis = 0)


    sum_for_all_movies = multiply_rating_by_similarity_scores.sum(axis = 0)


    final_ratings = sum_for_all_movies.div(denominator_for_all_movies, axis = 0)

    iicf = list(final_ratings.nlargest(10).index)

    return iicf




