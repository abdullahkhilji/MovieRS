import pandas as pd
from pymongo import MongoClient
import numpy as np
import warnings
from sklearn.decomposition import TruncatedSVD

def mf(username):

    client = MongoClient()

    person_username = username

    # point the client at mongo URI
    client = MongoClient('mongodb://db_username:db_password_12345@moviers-shard-00-00-3hnlg.mongodb.net:27017,moviers-shard-00-01-3hnlg.mongodb.net:27017,moviers-shard-00-02-3hnlg.mongodb.net:27017/test?ssl=true&replicaSet=moviers-shard-0&authSource=admin&retryWrites=true/moviers')
    # select database
    db = client['movie_data']
    # select the collection within the database
    ratings_mongodb = db.user_ratings_100836_test
    # convert entire collection to Pandas dataframe
    ratings = pd.DataFrame(list(ratings_mongodb.find()))

    ratings_only = ratings.drop(['_id', 'userId'], axis = 1)


    a = list(ratings.T.loc["userId"])

    for i in range(len(a)):
        if a[i] == person_username:
            person = i


    ratings_only = ratings_only.apply(pd.to_numeric)


    ratings_only = ratings_only.replace(np.nan, 0)

    ratings_only_t = ratings_only.T


    list_of_all_movies = list(ratings_only)

    user_rated_movies = []
    for movie in ratings_only_t.T:
        if ratings_only.iloc[person][movie] != 0.0 and str(movie) in list_of_all_movies:
            user_rated_movies.append(str(movie))

    X = ratings_only.values.T

    SVD = TruncatedSVD(n_components=12, random_state=17)
    matrix = SVD.fit_transform(X)
    matrix.shape

    warnings.filterwarnings("ignore",category =RuntimeWarning)
    corr = np.corrcoef(matrix)
    corr.shape


    movie_title = ratings_only.index
    movie_title_list = list(ratings_only)


    fact = []
    for i in user_rated_movies:
        for j in movie_title_list:
            if i == j:
                fact.append(movie_title_list.index(i))


    corr_fact = corr[fact]

    final_predict = []
    for i in range(len(corr_fact)):
        for j in range(len(corr_fact[i])):
            if corr_fact[i][j] >= 0.9:
                final_predict.append([i, j, corr_fact[i][j]])

    final_predict.sort(key=lambda x: x[2], reverse=True)


    movie_values = {}
    j = -1
    for i in ratings_only:
        j += 1
        movie_values.update({j: i})

    final_list = []

    for i in final_predict:
        if i[2] != 1:
            final_list.append(movie_values[i[1]])


    mf = final_list[:10]

    return mf













