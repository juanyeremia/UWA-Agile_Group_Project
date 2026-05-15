# ======================================
# Configurations for the Flask application
# ======================================

import os

class Config:
  SECRET_KEY = 'my-secret-key'                                  # Used by Flask to secure sessions and other things
  SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'    # Tells Flask-SQLAlchemy where the database is located
  TMDB_ACCESS_TOKEN=os.getenv('TMDB_ACCESS_TOKEN')  # Get the TMDB API token from .env file

class DeploymentConfig(Config):
  pass


class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'   # Use an in-memory database for testing
  TESTING = True  
  WTF_CSRF_ENABLED = False