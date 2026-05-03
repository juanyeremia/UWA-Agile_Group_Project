from app import db

#=================================================
# Define database models  
#=================================================
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)
  role = db.Column(db.String(20), nullable=False, default='user')   # Role can be 'user' or 'admin'
  reviews = db.relationship('Review', back_populates='author')    # One-to-many relationship with Review

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, nullable=False)   # Assuming movie_id is an integer referencing a movie in an external database
  body = db.Column(db.Text, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  flagged = db.Column(db.Boolean, default=False)   # Flag to indicate if the review is flagged for moderation
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', back_populates='reviews')    # Many-to-one relationship with User