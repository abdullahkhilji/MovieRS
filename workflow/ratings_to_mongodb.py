import pandas as pd
from pymongo import MongoClient

# read ratings file from mongodb database
ratings = pd.read_csv("../final_ratings.csv")
ratings = ratings.drop(ratings.columns[0], axis=1)

# get a list of all unique users
all_users = []
for i in range(len(ratings)):
    all_users.append(str(int(ratings.iloc[i]['userId'])))
all_users = list(set(all_users))

for each_user in all_users:
    a = {}
    a.update({'userId': each_user})
    for j in range(len(ratings)):
        if str(int(ratings.iloc[j]['userId'])) == each_user:
            a.update({str(int(ratings.iloc[j]['movieId'])): str(int(ratings.iloc[j]['rating']))})
    client = MongoClient('localhost', 27017)
    db = client['movie_data']
    collection = db['user_ratings_4570_new']
    collection.insert(a)




