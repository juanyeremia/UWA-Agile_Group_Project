from flask import render_template
from app import app

#=================================================
# Define routes
#=================================================

# Home page route
@app.route('/')
def home():
  return render_template('home_page.html')

# Write review page route
@app.route('/write_review')
def write_review():
  return render_template('write_review.html')

# Admin profile page route
@app.route('/admin_profile')
def admin_profile():
  return render_template('admin_profile.html')

# User profile page route
@app.route('/user_profile')
def user_profile():
  return render_template('user_profile.html')