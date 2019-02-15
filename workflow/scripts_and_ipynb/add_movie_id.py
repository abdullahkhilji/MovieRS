import pandas as pd
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/movie_data'
mongo = PyMongo(app)
movies_174_new = mongo.db.movies_174_new


# read links csv file
links = pd.read_csv("../final_data_to_scrap.csv")

movie = {}

# disabling pandas warning
links.is_copy = False

a = '00000'
for i in range(len(links)):
    link = str(links.iloc[i]["imdbId"])
    link = str(link).split('.')[0]
    length = 7 - len(str(link).split('.')[0])
    to_add = a[:length]
    link = "tt" + to_add + str(int(links.iloc[i]["imdbId"]))
    links.imdbId.iloc[[i]] = str(link)


for i in range(len(links)):
    movies_174_new.update_one({"imdb_id": links.iloc[i]["imdbId"]},
                                {
                                    "$set": {
                                        "movie_id": str(links.iloc[i]["movieId"])

                                    }
                                }
                                )





