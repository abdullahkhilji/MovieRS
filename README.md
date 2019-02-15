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
├── deploy.py
├── directory_tree.txt
├── iicf.py
├── mf.py
├── movies_174_new.json
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
├── user_ratings_4570_new.json
└── uucf.py

4 directories, 25 files

```






## 1. Scraping the Data from IMDb
For scraping the data  from IMDb website, Scrapy (a free open-source web-crawling framework written in python was utilised). It is similar to selenium but with an added in-built ability to HTML, process data and save it.
Thus using the in-built pipelines, the process of extracting the data from the webpage of each movie and directly connecting it to mongDB and downloading thumbnails for each Movie was greatly streamlined.

## 2. Movie Recommendation System
After scraping and storing the data in mongoDB, three algorithms were utilised to predict the ratings for the particular user in consideration and top 10 movies were displayed.

## 3. Deploying to Heroku
The project was deployed to Heroku, by integrating it with GitHub the link to the website is [https://moviers.herokuapp.com/](https://moviers.herokuapp.com/)

## 4. Docker Container
The `Dockerfile`  is included in the root of this repository, and can be build from within this directory by running `docker build --tag=moviers .`  to build and `docker run -p 5000:7000 moviers` to map the port `5000` of the docker container to your machines port: `7000` this can be easily conffigured as per your requirements. 

## An Important Note
Here, it is worthy to note that this repository is used in deploying code directly to Heroku and thus the docker specific files as stored in `docker_content` folder present in this repository but not mentioned in the above tree (for minimizing redundancy). Docker uses only the files stored in `docker_content` and thus you can safely make changes there.






Authored By: Abdullah Faiz Ur Rahman Khilji

Department of Computer Science and Engineering
National Institute of Technology Silchar




