from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_assets import Bundle, Environment
from uucf import uucf
from iicf import iicf
from mf import mf


app = Flask(__name__)


app.config['MONGO_URI'] = 'mongodb://db_username:db_password_12345@moviers-shard-00-00-3hnlg.mongodb.net:27017,moviers-shard-00-01-3hnlg.mongodb.net:27017,moviers-shard-00-02-3hnlg.mongodb.net:27017/moviers?ssl=true&replicaSet=moviers-shard-0&authSource=admin&retryWrites=true'
app.config['MONGO_DB'] = 'moviers'
app.secret_key = 'mysecret'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if 'username' in session:
        #return 'You are logged in as  :' + session['username']
        return render_template('dashboard.html')
    test = True
    return render_template('login.html', test = test)


@app.route('/login_check', methods=['POST'])
def login_check():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if check_password_hash(login_user['password'], request.form['pass']):
            session['username'] = request.form['username']
            return redirect(url_for('login'))
    test = False
    return render_template('login.html', test=test)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        user_ratings = mongo.db.user_ratings_4570_new
        existing_user = users.find_one({'name': request.form['username']})
        if existing_user is None:
            hashpass = generate_password_hash(request.form['pass'], method='sha256')
            users.insert({'name': request.form['username'], 'password': hashpass})
            user_ratings.insert({'userId': request.form['username']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return redirect(url_for('register'))
    return render_template('register.html')





@app.route('/see_uucf_suggestions')
def see_uucf_suggestions():
    if 'username' in session:
        movies = uucf(session['username'])
        movie_data = []
        #movies = ['1302', '1306', '1305', '1307', '1312', '1318', '1320', '1322', '1321', '1324', '1326']
        for i in movies:
            movie_data.append(mongo.db.movies_174_new.find({'movie_id': i}))

        return render_template('see_uucf_suggestions.html', movies=movie_data)
    return render_template('login.html')


@app.route('/see_iicf_suggestions')
def see_iicf_suggestions():
    if 'username' in session:
        movies = iicf(session['username'])
        movie_data = []
        for i in movies:
            movie_data.append(mongo.db.movies_174_new.find({'movie_id': i}))
        return render_template('see_iicf_suggestions.html', movies=movie_data)
    return render_template('login.html')


@app.route('/see_mf_suggestions')
def see_mf_suggestions():
    if 'username' in session:
        movies = mf(session['username'])
        movie_data = []
        for i in movies:
            movie_data.append(mongo.db.movies_174_new.find({'movie_id': i}))
        return render_template('see_mf_suggestions.html', movies=movie_data)
    return render_template('login.html')



@app.route('/rate_movies')
def rate_movies():
    if 'username' in session:
        movies = mongo.db.movies_174_new.find({})
        user = mongo.db.users_4570_new.find({'userId': session['username']})
        return render_template('rate_movies.html', movies=movies, user=user)
    return render_template('login.html')


@app.route('/submit_rate', methods=['POST'])
def submit_rate():
    user_ratings = mongo.db.user_ratings_4570_new
    query = {"userId": session['username']}
    newvalues = {'$set': {request.form['movies']: request.form['rating']}}
    user_ratings.update_one(query, newvalues)
    return redirect(url_for('rate_movies'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)


