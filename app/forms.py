from flask_wtf import FlaskForm
from wtforms import  FloatField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, HiddenField, RadioField
from wtforms.validators import DataRequired
from app.models import User
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional, AnyOf



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SearchForm(FlaskForm):
    search_term = StringField('Enter Search', validators=[DataRequired()])
    filter = RadioField('Filter', choices=[('A', 'All'), ('S', 'Ended With Sales'), ('U', 'Ended Without Sales')], default='A')
    submit = SubmitField('Search')

class ItemForm(FlaskForm):
    item_name = StringField('Enter Item Name', validators=[DataRequired()])
    item_price = FloatField('Enter Item Price', validators=[DataRequired()])
    item_category = StringField('Enter Category', validators=[DataRequired()])
    submit = SubmitField("Add")