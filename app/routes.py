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