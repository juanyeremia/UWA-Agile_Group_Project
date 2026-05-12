from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SignUpForm, LoginForm
import os
import requests
from flask import jsonify
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
  flash('Error creating account. Please check your input and try again.', 'danger')
  return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
      email = form.email.data.strip().lower()
      user = User.query.filter_by(email=email).first()
      password = form.password.data
      if user and user.check_password(password):
          flash('Logged in successfully!', 'success')
          return redirect(url_for('home'))
      else:
          flash('Invalid email or password. Please try again.', 'danger')
  return render_template('login.html', form=form)

@app.route('/terms')
def terms():
  return render_template('terms.html')

@app.route('/privacy')
def privacy():
  return render_template('privacy.html')

@app.route('/profile')
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
# Get 'Highest Rated' movies from Internal Database (Placeholder)
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