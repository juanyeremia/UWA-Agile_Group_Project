from flask import render_template
from app import app
from app.forms import SignUpForm, LoginForm
import os
import requests
from flask import jsonify

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

@app.route('/sign_up')
def sign_up():
  return render_template('sign_up.html', form=SignUpForm())

@app.route('/login')
def login():
  return render_template('login.html', form=LoginForm())

@app.route('/terms')
def terms():
  return render_template('terms.html')

@app.route('/privacy')
def privacy():
  return render_template('privacy.html')

@app.route('/profile')
def profile():
    return render_template('user_profile.html')

@app.route('/admin')
def admin():
    return render_template('admin_profile.html')
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
   token = app.config['TMDB_ACCESS_TOKEN']
   headers = {
      'Authorization': f'Bearer {token}'
   }
   response = requests.get(
      'https://api.themoviedb.org/3/movie/now_playing',
      headers=headers
   )
   data = response.json()
   return jsonify(data)
