from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # For image files
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DecimalField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from goodeats.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username has already been taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There already exists an account for this email address.')
        
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class IngredientForm(FlaskForm):
    name = StringField('Name')
    quantity = StringField('Quantity')

class NutritionalForm(FlaskForm):
    calories = DecimalField('Calories') 
    carbohydrates = DecimalField('Carbohydrate Content')
    saturatedFats = DecimalField('Saturated Fats')
    cholestrol = DecimalField('Cholestrol Content')
    fat = DecimalField('Fat Content')
    protein = DecimalField('Protein Content')
    fibers = DecimalField('Fiber Content')
    sugar = DecimalField('Sugar Content')
    sodium = DecimalField('Sodium Content')

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    cooktime = StringField('Cooking Time', validators=[Length(min=1, max=100)])
    preptime = StringField('Preparation Time', validators=[Length(min=1, max=100)])
    recipeServings = StringField('Number of servings')
    nutritionalFacts = FormField('Nutritional Information')
    submit = SubmitField('Post')