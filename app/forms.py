from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


#=================================================
# Define forms
#=================================================
# Define the sign-up form with username, email, password, and confirm password fields
class SignUpForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6, max=200)]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), Length(min=6, max=200), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('Username is already existing.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('Email is already existing.')

# Define the login form with email, password, and remember me fields
class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6, max=200)]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
