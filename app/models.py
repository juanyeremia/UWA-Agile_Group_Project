from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone

#=================================================
# Define database models  
#=================================================
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(200), nullable=False)
  role = db.Column(db.String(20), nullable=False, default='user')   # Role can be 'user' or 'admin'
  reviews = db.relationship('Review', back_populates='author')    # One-to-many relationship with Review
  def set_password(self, password): # Hash the password and store it in the database
    self.password_hash = generate_password_hash(password) 

  def check_password(self, password): # Check the provided password against the stored hash
    return check_password_hash(self.password_hash, password)
  
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', name="fk_review_movie_id"), nullable=False)   # Assuming movie_id is an integer referencing a movie in an external database
  body = db.Column(db.Text, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  flagged = db.Column(db.Boolean, default=False)   # Flag to indicate if the review is flagged for moderation
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', back_populates='reviews')    # Many-to-one relationship with User
  movie = db.relationship('Movie', back_populates='reviews')  # 
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class Movie(db.Model):
  id = db.Column(db.Integer, primary_key=True)  # This IS the TMDB movie_id
  reviews = db.relationship('Review', back_populates='movie')
