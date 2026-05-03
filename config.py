# ======================================
# Configurations for the Flask application
# ======================================

import os

class Config:
  SECRET_KEY = 'my-secret-key'                                  # Used by Flask to secure sessions and other things
  SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'    # Tells Flask-SQLAlchemy where the database is located