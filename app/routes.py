from flask import render_template, flash, redirect, session, url_for, request, jsonify, Blueprint, current_app
from app.forms import SignUpForm, LoginForm
import os
import requests
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from app.models import Review
from app import db
from app.models import User
from werkzeug.utils import secure_filename
from app.blueprints import main
import uuid



#=================================================
# Define routes
#=================================================


# Home page route
@main.route('/')
def home():
 return render_template('home_page.html')


#=================================================
# Individul movie page route & movie details
#=================================================
@main.route('/movie/<int:movie_id>')
def movie_detail(movie_id):


   url = f"https://api.themoviedb.org/3/movie/{movie_id}"


   headers = {
       "Authorization": f"Bearer {os.getenv('TMDB_ACCESS_TOKEN')}"
   }


   response = requests.get(url, headers=headers)


   data = response.json()


   movie = {
       "id": data.get("id"),
       "title": data.get("title"),
       "poster_url": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}",
       "release_date": data.get("release_date"),
       "description": data.get("overview"),
       "rating": data.get("vote_average"),
       "genres": data.get("genres")
   }


   reviews = [
       {
           "user": {"username": "Tammy"},
           "rating": 5,
           "content": "Amazing!"
       },
       {
           "user": {"username": "Alex"},
           "rating": 4,
           "content": "Pretty good!"
       }
   ]


   return render_template(
       'individual_movie.html',
       movie=movie,
       reviews=reviews
   )






@main.route('/sign_up', methods=['GET', 'POST'])
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
       return redirect(url_for('main.login'))
   elif form.is_submitted():
       flash('Error creating account. Please check your input and try again.', 'danger')
   return render_template('sign_up.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
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
           return redirect(url_for('main.home'))
   return render_template('login.html', form=form)




@main.route('/logout')
def logout():
   logout_user()  # Log the user out using Flask-Login
   return redirect(url_for('main.home'))


@main.route('/terms')
def terms():
 return render_template('terms.html')


@main.route('/privacy')
def privacy():
 return render_template('privacy.html')


@main.route('/profile')
@login_required
def profile():


   user_reviews = Review.query.filter_by(
       user_id=current_user.id
   ).order_by(Review.id.desc()
   ).all()


   return render_template(
       'user_profile.html',
       user=current_user,
       reviews=user_reviews,
       review_count=len(user_reviews)
   )




@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.bio = request.form.get('bio')

        image = request.files.get('profile_image')

        if image and image.filename != '':
            original_filename = secure_filename(image.filename)
            file_extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"

            upload_folder = os.path.join(current_app.root_path, 'static/profile_images')
            os.makedirs(upload_folder, exist_ok=True)

            image.save(os.path.join(upload_folder, unique_filename))
            current_user.profile_image = unique_filename

        db.session.commit()

        return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', user=current_user)

def admin_required():
    return current_user.is_authenticated and current_user.role == 'admin'

@main.route('/admin')
@login_required
def admin():

    if not admin_required():
        flash("You do not have permission to access the admin page.", "danger")
        return redirect(url_for('main.profile'))

    flagged_reviews = Review.query.filter_by(flagged=True).all()
    total_users = User.query.count()

    recent_actions = [
        "Deleted a flagged review",
        "Checked reported content",
        "Searched user account",
        "Removed inactive user"
    ]

    return render_template(
        'admin_profile.html',
        flagged_reviews=flagged_reviews,
        flagged_count=len(flagged_reviews),
        total_users=total_users,
        recent_actions=recent_actions
    )

#=================================================
# Delete a review
#=================================================
@main.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):

    if not admin_required():
        return jsonify({"success": False, "message": "Admin access required"}), 403

    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()

    return jsonify({"success": True})

#=================================================
# Unflag a review
#=================================================
@main.route('/unflag_review/<int:review_id>', methods=['POST'])
@login_required
def unflag_review(review_id):

    if not admin_required():
        return jsonify({"success": False, "message": "Admin access required"}), 403

    review = Review.query.get_or_404(review_id)
    review.flagged = False
    review.flag_reason = None
    db.session.commit()

    return jsonify({"success": True})


@main.route('/search_user')
@login_required
def search_user():

    if not admin_required():
        return jsonify({"success": False, "message": "Admin access required"}), 403

    query = request.args.get('query', '')

    users = User.query.filter(
        (User.username.contains(query)) |
        (User.email.contains(query))
    ).all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ])


@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):

    if not admin_required():
        return jsonify({"success": False, "message": "Admin access required"}), 403

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        return jsonify({
            "success": False,
            "message": "You cannot delete your own account."
        }), 400

    Review.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"success": True})

@main.route('/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    user = User.query.get_or_404(user_id)

    user.role = 'admin'

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User is now admin"
    })

@main.route('/remove_admin/<int:user_id>', methods=['POST'])
@login_required
def remove_admin(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        return jsonify({
            "success": False,
            "message": "You cannot remove your own admin role"
        }), 400

    user.role = 'user'

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Admin role removed"
    })

#=================================================
# Get the TMDB_ACCESS_TOKEN
#=================================================
token = os.getenv("TMDB_ACCESS_TOKEN")


#=================================================
# Get 'Now Playing' movies from TMDB API
#=================================================
@main.route('/api/movies/now_playing')
def now_playing():
 token = current_app.config['TMDB_ACCESS_TOKEN']                    # Retrieve the TMDB access token from the Flask app's configuration
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
@main.route('/api/movies/ratings')
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
@main.route('/api/movies/highest_rated')
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
@main.route('/api/movies/<int:movie_id>')
def movie_detail_api(movie_id):
   token = current_app.config['TMDB_ACCESS_TOKEN']                    # Retrieve the TMDB access token from the Flask app's configuration
   headers = { 'Authorization': f'Bearer {token}'}                      # Set up the headers for the API request, including the Authorization header with the Bearer token
   response = requests.get(                                                   # Make a GET request to the TMDB API endpoint for movie details, including the headers with the access token
       f'https://api.themoviedb.org/3/movie/{movie_id}',
       headers=headers
   )
   return jsonify(response.json())                                                   # Parse the JSON response from the API and return it as a JSON response to the client


#=================================================
# Get most recent review from local DB
#=================================================
@main.route('/api/reviews/recent')
def recent_reviews():
    # Query the 5 most recent reviews ordere by review ID descending
    results = Review.query.order_by(Review.id.desc()).limit(5).all()

    reviews = [
        {
            'id': r.id,
            'movie_id': r.movie_id,
            'rating': r.rating,
            'body': r.body,
            'username': r.author.username,           # connects Review and User throught the 'author' relationship
            'flagged': r.flagged,
        }
        for r in results
    ]

    return jsonify(reviews)

#=================================================
# Set up route for submitting a new review
#=================================================
@main.route('/write_review/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def write_review(movie_id):


   # Handle the form submission when the request method is POST
   if request.method == 'POST':
       body = request.form.get('body') # Get the review content from the form data
       rating = request.form.get('rating') # Get the review rating from the form data


       # Write review to the database
       review = Review(
           movie_id=movie_id,
           body=body,
           rating=int(rating),
           user_id=current_user.id  # Associate the review with the currently logged-in user
       )
       db.session.add(review) # Add the new review to the database session
       db.session.commit() # Commit the session to save the review to the database
       return redirect(url_for('main.movie_detail', movie_id=movie_id)) # Redirect back to the movie detail page after submitting the review
  
   # GET request: Fetch movie data and just render the review submission form
   token = current_app.config['TMDB_ACCESS_TOKEN']                    # Retrieve the TMDB access token from the Flask app's configuration
   headers = {'Authorization':f'Bearer {token}'}                      # Set up the headers for the API request, including the Authorization header with the Bearer token
   response = requests.get(                                                   # Make a GET request to the TMDB API endpoint for movie details, including the headers with the access token
       f'https://api.themoviedb.org/3/movie/{movie_id}',
       headers=headers
   )
   movie = response.json()


   return render_template('write_review.html', movie_id=movie_id, movie=movie) # Render the review submission form for GET requests

#=================================================
# Flagging a review for admin review
#=================================================
@main.route('/flag_review/<int:review_id>', methods=['POST'])
@login_required
def flag_review(review_id):
   review = Review.query.get_or_404(review_id)
   review.flagged = True
   review.flagged_reason = request.form.get('reason', 'Inappropriate content') # Get the reason for flagging from the form data, with a default reason if none provided
   db.session.commit() 
   return jsonify({'success':True}) # Return a JSON response indicating the review was flagged successfully

#=================================================
# Redirect to the search page
#=================================================
@main.route('/search')
def search():
   query = request.args.get('query')


   movies = []


   if query:
       url = "https://api.themoviedb.org/3/search/movie"


       headers = {
           "Authorization": f"Bearer {os.getenv('TMDB_ACCESS_TOKEN')}"
       }


       params = {
           "query": query
       }


       response = requests.get(url, headers=headers, params=params)
       data = response.json()

       movies = data.get("results", [])

       movie_ids =[movie["id"] for movie in movies]

       if movie_ids:
          rating_results =db.session.query(
             Review.movie_id,
             func.avg(Review.rating).label('avg_rating'),
             func.count(Review.id).label('review_count')
          ).filter(
             Review.movie_id.in_(movie_ids)
          ).group_by(
             Review.movie_id
          ).all()

          ratings = {
             r.movie_id:{
                "avg_rating": round(r.avg_rating, 1),
                "review_count": r.review_count
             }
             for r in rating_results
          }

          for movie in movies:
             local_rating = ratings.get(movie["id"], {
                "avg_rating": 0,
                "review_count": "No"
             })

             movie["local_avg_rating"] = local_rating["avg_rating"]
             movie["local_review_count"] = local_rating["review_count"]


   return render_template(
       'search.html',
       movies=movies,
       query=query
   )
