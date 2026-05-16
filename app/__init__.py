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
login.login_view = 'main.login'     # Set the login view for @login_required

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)

    return app

# Import routes and models to register them with the app
from app import routes, models




