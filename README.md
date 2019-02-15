# MovieRS
#### The task is to build a movie recommender system, which asks a user to rate a small set of movies and based on these ratings, suggests more movies which will suit their taste.


```
tree -I '*.jpg|docker_content|venv|__pycache__' MovieRS > directory_tree.txt
```

```
MovieRS
├── Dockerfile
├── Procfile
├── README.md
├── boot.sh
├── deploy.py
├── directory_tree.txt
├── docker_run.py
├── iicf.py
├── mf.py
├── mongodb_collections
│   ├── movies_174_new.json
│   └── user_ratings_4570_new.json
├── requirements.txt
├── static
│   ├── bootstrap.min.css
│   ├── bootstrap.min.js
│   ├── images
│   ├── jquery.min.js
│   └── new.css
├── templates
│   ├── dashboard.html
│   ├── includes
│   │   └── _navbar.html
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── rate_movies.html
│   ├── register.html
│   ├── see_iicf_suggestions.html
│   ├── see_mf_suggestions.html
│   └── see_uucf_suggestions.html
├── uucf.py
└── workflow
├── movielens_data
│   ├── links.csv
│   └── ratings.csv
├── new_data
│   ├── final_data_to_scrap.csv
│   └── final_ratings.csv
├── ratings_to_mongodb.py
├── scrapy_spiders
│   └── scrap_imdb
│       ├── scrap_imdb
│       │   ├── __init__.py
│       │   ├── items.py
│       │   ├── middlewares.py
│       │   ├── pipelines.py
│       │   ├── settings.py
│       │   └── spiders
│       │       ├── SpiderCrawl.py
│       │       ├── Untitled.ipynb
│       │       ├── __init__.py
│       │       ├── final_data.csv
│       │       ├── images_174_new
│       │       │   └── full
│       │       ├── log.txt
│       │       └── test.txt
│       └── scrapy.cfg
└── scripts_and_ipynb
├── add_movie_id.py
├── dataset.ipynb
└── get_only_new_movies_ratings.ipynb

15 directories, 47 files


```

#### Dependencies:

Click==7.0  <br>
Flask==1.0.2 <br>
Flask-PyMongo==2.2.0 <br>
gunicorn==19.9.0 <br>
itsdangerous==1.1.0 <br>
Jinja2==2.10 <br>
MarkupSafe==1.1.0 <br>
numpy==1.16.1 <br>
pandas==0.24.1 <br>
pymongo==3.7.2 <br>
python-dateutil==2.8.0 <br>
pytz==2018.9 <br>
scikit-learn==0.20.2 <br>
scipy==1.2.1 <br>
six==1.12.0 <br>
sklearn==0.0 <br>
Werkzeug==0.14.1 <br>



# 1. Scraping the Data from IMDb
For scraping the data  from IMDb website, Scrapy (a free open-source web-crawling framework written in python was utilised). It is similar to selenium but with an added in-built ability to HTML, process data and save it.
Thus using the in-built pipelines, the process of extracting the data from the webpage of each movie and directly connecting it to mongDB and downloading thumbnails for each Movie was greatly streamlined.

### 1.1. Scrapy
The scrapy spider files are stored  under `scrapy_spiders`  it also includes the CSV files of the scrapped data. The initial dataset was procured from [http://files.grouplens.org/datasets/movielens/ml-latest-small.zip](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip)

#### 1.1.1. MovieLens Dataset Description
>This dataset (ml-latest-small) describes 5-star rating and free-text tagging activity from MovieLens, a movie recommendation service. It contains 100836 ratings and 3683 tag applications across 9742 movies. These data >were created by 610 users between March 29, 1996 and September 24, 2018. This dataset was generated on September 26, 2018. Users were selected at random for inclusion. All selected users had rated at least 20 >movies. The data are contained in the files links.csv, movies.csv, ratings.csv and tags.csv. 


### 1.2. Populating the Movies Table
By undertaking a array of analysis, 10 movies were chosen from each Genre viz. Comedy, Drama, Action, Adventure, Crime, Horror, Documentary, Animation, Children, Thriller, Sci-Fi, Mystery, Fantasy, Romance, Western, Musical and Film-Noir with the exception of War which had only 4. Thus a total list of 174 movies was curated from the MovieLens dataset and the respective data extracted from the IMDb webpages. (This system can easily be scaled to accomodate all 9704 movies and the corresponding 100836 ratings, but since due to the limited resources given by the free Heroku plan, the scalability issue persisted. The full size extracted data is also included in this repository in /full_size ) 

### 1.3. Populating the User's Rating Table
For our algorithm to be effective enough atleast for the first two, it requires that it it has enough user ratings. Thus,  a  `ratings_to_mongodb.py`  script under was written to capture ratings present in each line and populate the database only for the movies taken into consideration. It takes `final_ratings.csv` (a file similar to `ratings.csv` but containing only those ratings for which we have stored the data in our database) and updates the ratings value in the Movies x Users table in the mongoDB database.

### 1.4. The Mongo Database
All the database for this project is hosted at MongoDB Atlas free clusters. The same database is synced across the Heroku deployment as well as in Docker.





# 2. Movie Recommendation System
After scraping and storing the data in mongoDB, three algorithms were utilised to predict the ratings for the particular user in consideration and top 10 movies were displayed.
It is suggested that the user rate at least 20 of the movies, effectively taking the value of K as 20. This value is taken considering that All selected users had rated at least 20 movies as written in the README section of the MovieLens Dataset.

### 2.1. User User Collaborative Filtering (UUCF)
In UUCF the main idea is that, the algorithm finds the User's most similar to the current User and calculates the ratings of the movies he has not rated by the similarity score. The similarity is based on Pearson Correlation.
### 2.2. Item Item Collaborative Filtering (IICF)
In IICF the algorithm selects the movies most closest to the movies the user has already rated and takes this similarity score and ratings of the movies the user has rated into consideration and gives suggestions based on the highest ratings predicted. The similarity is based on Pearson Correlation.
### 2.3. Matrix Factorisation (MF)
The strength of matrix factorization is the that it can gather information that are not seen directly but can be visualized by analyzing user's behavior. Using this criteria we can judge the user's opinion regarding th particular movie. This method is the most viable option for recommender systems.



# 3. Deploying to Heroku
The project was deployed to Heroku, by integrating it with GitHub the link to the website is [https://moviers.herokuapp.com/](https://moviers.herokuapp.com/)

### 3.1. Flask
For the backend of this project Flask was used. Flask is a micro web framework written in Python.

### 3.2. Gunicorn
The Gunicorn "Green Unicorn" is a Python Web Server Gateway Interface HTTP server.  Since Flask cannot serve multiple users at the same time, we serve the application using Gunicorn. 


# 4. Docker Container
The `Dockerfile`  is included in the root of this repository, and can be build from within this directory using:

```
docker build --tag=moviers .
```

and then run:
```
docker run -p 5000:5000 moviers
```
to map the port `5000` of the docker container to your machines port: `5000` this can be easily conffigured as per your requirements.  Then visit `localhost:5000` in your web-browser.




<br>
<br>
<br>
<br>
<br>
<br>
<br>



Authored By: Abdullah Faiz Ur Rahman Khilji

Department of Computer Science and Engineering <br>
National Institute of Technology Silchar <br>

[https://abdullahkhilji.github.io/](https://abdullahkhilji.github.io/)
