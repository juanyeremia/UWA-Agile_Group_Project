#=============================
# Create Flask app
#=============================

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)      # Load configuration from Config class

# Initialize database and migration objects
db = SQLAlchemy(app)          # Create SQLAlchemy database object
migrate = Migrate(app, db)   # Create Migrate object for migration commands

# Import routes and models to register them with the app
from app import routes, models