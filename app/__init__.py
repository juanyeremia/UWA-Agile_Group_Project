#=============================
# Create Flask app
#=============================

from flask import Flask

app = Flask(__name__)

# Import routes after creating the app to avoid circular imports
from app import routes