from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # For image files
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, DecimalField, FieldList, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from goodeats.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username has already been taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There already exists an account for this email address.')
        
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
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
    ingredient_name = StringField('Name')
    quantity = StringField('Quantity')

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    cooktime = StringField('Cooking Time', validators=[Length(min=1, max=100)])
    preptime = StringField('Preparation Time', validators=[Length(min=1, max=100)])
    recipe_image = FileField('Recipe Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    recipeServings = StringField('Number of servings')
    keywords = FieldList(StringField('Keywords'))
    submit = SubmitField('Post')
    picture = FileField('Recipe Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])