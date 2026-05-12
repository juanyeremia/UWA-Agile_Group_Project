from flask import render_template, flash, redirect, session, url_for, request, jsonify
from app import app
from app.forms import SignUpForm, LoginForm
import os
import requests
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from app.models import Review
from app import db
from app.models import User

#=================================================
# Define routes
#=================================================

# Home page route
@app.route('/')
def home():
  return render_template('home_page.html')

# Write review page route
@app.route('/write_review/<int:movie_id>')
def write_review(movie_id):
    return render_template('write_review.html')

""" - The original one after the test
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    return render_template('individual_movie.html') """

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip(), 
                email=form.email.data.strip().lower(), 
                role='user'
      )
        user.set_password(form.password.data)  # Hash the password and set it for the user
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    elif form.is_submitted():
        flash('Error creating account. Please check your input and try again.', 'danger')
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        password = form.password.data
        if user is None or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('login.html', form=form)
        else:
            login_user(user, remember=form.remember_me.data)  # Log the user in using Flask-Login
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()  # Log the user out using Flask-Login
    return redirect(url_for('home'))

@app.route('/terms')
def terms():
  return render_template('terms.html')

@app.route('/privacy')
def privacy():
  return render_template('privacy.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('user_profile.html')

#=================================================
# Get the TMDB_ACCESS_TOKEN
#=================================================
token = os.getenv("TMDB_ACCESS_TOKEN")

#=================================================
# Individual movie page for testing
#=================================================
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = {
        "id": movie_id,
        "title": "Arcane",
        "poster_url": "https://img.league-funny.com/imgur/172482406314_o.png",
        "release_date": "2024",
        "director": "Riot Games",
        "description": "This is a sample movie description.",
        "cast": "Hailee Steinfeld, Ella Purnell",
        "crew": "Created by Christian Linke and Alex Yee",
        "details": "Animated series based on League of Legends.",
        "genre": "Animation, Action, Adventure",
        "release_info": "Released on Netflix"
    }

    reviews = [
        {"user": {"username": "Tammy"}, "rating": 5, "content": "Amazing!"},
        {"user": {"username": "Alex"}, "rating": 4, "content": "Pretty good!"}
    ]

    return render_template('individual_movie.html', movie=movie, reviews=reviews)

#=================================================
# Get 'Now Playing' movies from TMDB API
#=================================================
@app.route('/api/movies/now_playing')
def now_playing():
  token = app.config['TMDB_ACCESS_TOKEN']                    # Retrieve the TMDB access token from the Flask app's configuration
  headers = {                                                                        # Set up the headers for the API request, including the Authorization header with the Bearer token
    'Authorization': f'Bearer {token}'
  }
  response = requests.get(                                                   # Make a GET request to the TMDB API endpoint for 'Now Playing' movies, including the headers with the access token
    'https://api.themoviedb.org/3/movie/now_playing',
    headers=headers
  )
  data = response.json()                                                       # Parse the JSON response from the API into a Python dictionary
  return jsonify(data)                                                            # Return the data as a JSON response to the client

#=================================================
# Get average rating from Review for each movie ID 
#=================================================
@app.route('/api/movies/ratings')
def movie_ratings():
    # 1. Get movie IDs from query string ex: /api/movies/ratings?ids=1226863,550,27205
    ids_param = request.args.get('ids','')                  # Reads the API calls and look 'ids' in the url
    if not ids_param:                                                  # If no IDs provided, return empty dictionary
        return jsonify({})

    # 2. Convert the comma-separated string into a list of integers
    movie_ids = [int(id) for id in ids_param.split(',')]        # turns '550,27205' into [ 550', '27205']

    # 3. Query the Review table for average ratings for each movie_id
    results = db.session.query(
        Review.movie_id,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).filter(Review.movie_id.in_(movie_ids))\
     .group_by(Review.movie_id)\
     .all() 
    
    # 4. Build a dictionary of key-value pairs, with movie_id and rating data
    ratings = {
        r.movie_id: {
            'avg_rating': round(r.avg_rating,1),
            'review_count': r.review_count
        }
        for r in results
        
        # Example:
        #   {
        #      "550": {"avg_rating": 4.2, "review_count": 3},
        #       "27205": {"avg_rating": 3.8, "review_count": 1}
        #   }
    }

    return jsonify(ratings)

#=================================================
# Get 'Highest Rated' movies from Internal Database 
#=================================================
@app.route('/api/movies/highest_rated')
def highest_rated():
    # Query the database to get the average rating and review count for each movie, grouped by movie_id, ordered by average rating in descending order, and limited to the top 6 results
    results = db.session.query(                                            # Start a query on the database session
        Review.movie_id,                                                                  # SELECT  the movie_id from the Review model
        func.avg(Review.rating).label('average_rating'),                    # Calculate the average rating for each movie and label it as 'average_rating'
        func.count(Review.id).label('review_count')                           # Count the number of reviews for each movie and label it as 'review_count'
    ).group_by(Review.movie_id).\
    order_by(func.avg(Review.rating).desc())\
    .limit(6)\
    .all()                                                                                # Execute the query and return all results
   
   # Process the query results to create a list of movies with their average rating and review count, rounding the average rating to 1 decimal place for better readability
    movies = [
        {
            'movie_id':  r.movie_id,
            'avg_rating': round(r.average_rating, 1),  # Round the average rating to 1 decimal places
            'review_count': r.review_count
       }
       for r in results
    ]

    return jsonify(movies)                                                            # Return the list of movies as a JSON response to the client

#=================================================
# Get individual movie details from TMDB API based on movie ID (to populate other movie cards)
#=================================================
@app.route('/api/movies/<int:movie_id>')
def movie_detail_api(movie_id):
    token = app.config()['TMDB_ACCESS_TOKEN']                    # Retrieve the TMDB access token from the Flask app's configuration
    headers = { 'Authorization': f'Bearer {token}'}                      # Set up the headers for the API request, including the Authorization header with the Bearer token
    response = requests.get(                                                   # Make a GET request to the TMDB API endpoint for movie details, including the headers with the access token
        f'https://api.themoviedb.org/3/movie/{movie_id}',
        headers=headers
    )
    return jsonify(response.json())                                                   # Parse the JSON response from the API and return it as a JSON response to the client

#=================================================
# Get most recent review from local DB
#=================================================
@app.route('/api/reviews/recent')
def recent_reviews():
    # Query the 5 most recent reviews ordere by review ID descending
    results = Review.query.order_by(Review.id.desc()).limit(5).all()

    reviews = [
        {
            'id': r.id,
            'movie_id': r.body,
            'rating': r.rating,
            'username': r.author.username           # connects Review and User throught the 'author' relationship
        }
        for r in results
    ]

    return jsonify(reviews)