#=============================
# Create Flask app
#=============================

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os
from dotenv import load_dotenv

load_dotenv() # Load the environment (for the TMDB token)

app = Flask(__name__)
app.config.from_object(Config)      # Load configuration from Config class

# Initialize database and migration objects
db = SQLAlchemy(app)          # Create SQLAlchemy database object
migrate = Migrate(app, db)   # Create Migrate object for migration commands
login = LoginManager(app)       # Create LoginManager object for user session management
login.login_view = 'login'     # Set the login view for @login_required

# User loader function for Flask-Login
@login.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))  # Load user by ID for session management

# Import routes and models to register them with the app
from app import routes, models




