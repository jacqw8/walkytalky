from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from walkytalky.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CalendarForm(FlaskForm):
    day = StringField('Day', validators=[DataRequired()])
    input = StringField('Availability', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CalendarForm2(FlaskForm):
    removeday = StringField('Day', validators=[DataRequired()])
    removeinput = StringField('Availability', validators=[DataRequired()])
    remove = SubmitField('Remove')

class PostForm(FlaskForm):
    title = StringField('Day', validators=[DataRequired()])
    content = StringField('Availability', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddWalksForm(FlaskForm):
    title = StringField('Walked with', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    day = StringField('Date', validators=[DataRequired()])
    start = StringField('Start Time', validators=[DataRequired()])
    end = StringField('End Time', validators=[DataRequired()])
    distance = StringField('Distance', validators=[DataRequired()])
    submit = SubmitField('Add Walk')

class SearchFriend(FlaskForm):
    search = StringField("Friend's username:", validators=[DataRequired()])
    submit = SubmitField('Submit')
