from flask import render_template
from app import app
from app.forms import SignUpForm, LoginForm

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