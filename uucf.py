import pandas as pd
from pymongo import MongoClient
import numpy as np


def uucf(username):
    person_username = username
    # point the client at mongo URI
    client = MongoClient('mongodb://localhost:27017/movie_data')
    # select database
    db = client['movie_data']
    # select the collection within the database
    ratings_mongodb = db.user_ratings_100836_test
    # convert entire collection to Pandas dataframe
    ratings = pd.DataFrame(list(ratings_mongodb.find()))

    ratings_only = ratings.drop(['_id', 'userId'], axis=1)
    ratings_only = ratings_only.apply(pd.to_numeric)
    ratings_only = ratings_only.replace(np.nan, 0)
    ratings_only = ratings_only.T


    a = list(ratings.T.loc["userId"])
    for i in range(len(a)):
        if a[i] == person_username:
            person = i

    new_user = ratings_only.iloc[:, person]

    corr_user = ratings_only.corrwith(new_user)

    corr_user.nlargest(10)

    userId_list = list(ratings_only)

    final_user = corr_user.nlargest(3)

    # getting list of most similar 10 users (excluding the user itself, the one he is most similar to)
    final_user_list = list(final_user.index)[1:]
    # calculating denominator (sum_of_similarity_scores) before hand to reduce time complexity
    denominator = sum(list(final_user)[1:])  # sum_of_similarity_scores


    # user similarity list
    final_sim_list = list(final_user)[1:]


    columns = ['totals', 'simSums']
    df = pd.DataFrame(columns=columns, index=list(ratings_only.T))


    df = df.replace(np.nan, 0)

    # Gets recommendations for a person by using a weighted average
    # of every other user's rankings
    totals = {}
    simSums = {}
    for other in final_user_list:
        sim = final_user[other]
        # sim=corr_user[other]
        for movie_id in list(ratings_only.T):
            # only score movies I haven't seen yet
            if new_user.loc[movie_id] == 0.0:
                # Similarity * Score
                totals.setdefault(movie_id, 0)
                totals[movie_id] += ratings_only.loc[movie_id][other] * sim


    # Create the normalized list
    rankings = [(total/denominator, item) for item, total in totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()

    r = rankings[:10]

    uucf = []
    for i in range(len(r)):
        uucf.append(r[i][1])

    return uucf

