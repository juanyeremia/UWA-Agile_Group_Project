from flask import Blueprint
# Define the main blueprint for the application
main = Blueprint('main', __name__)

from app import routes, models