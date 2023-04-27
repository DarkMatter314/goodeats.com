from datetime import datetime
from goodeats.database import db
# from flask_login import UserMixin
import random

followers_table = db.Table('Followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.Text, nullable=False, default='https://w0.peakpx.com/wallpaper/979/89/HD-wallpaper-purple-smile-design-eye-smily-profile-pic-face.jpg')
    password = db.Column(db.String(60), nullable=False)

    # Relationships
    followers = db.relationship('User', secondary=followers_table,  primaryjoin=(followers_table.c.follower_id == id), 
                                secondaryjoin=(followers_table.c.following_id == id),
                                # backref=db.backref('following', lazy='dynamic'), 
                                lazy='dynamic')
    following = db.relationship('User', secondary=followers_table,  primaryjoin=(followers_table.c.following_id == id), 
                                secondaryjoin=(followers_table.c.follower_id == id),
                                # backref=db.backref('follower', lazy='dynamic'), 
                                lazy='dynamic')
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    reviews = db.relationship('Reviews', backref='author', lazy=True)
    collections = db.relationship('Collections', backref='author', lazy=True)
    is_active = True

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def get_id(self):
        return f"{id}"
    
    def to_dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'profile_picture': self.image_file
        }
    
recipe_keywords = db.Table('recipe_keywords',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('keywords_id', db.Integer, db.ForeignKey('keywords.id'), primary_key=True)
)

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredients_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)
    
class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Keyword: '{self.keyword}'"
    
    def __eq__ (self , user):
        return self.id == user.id

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Ingredient: '{self.ingredient_name}'"  
    
    def __eq__ (self , user):
        return self.id == user.id

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datePublished = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    instructions = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredientAmt = db.Column(db.Text, nullable=False)
    cooktime = db.Column(db.String(20), nullable=True)
    preptime = db.Column(db.String(20), nullable=True)
    reviewCount = db.Column(db.Integer, nullable=True, default=0)
    avgRating = db.Column(db.Integer, nullable=True, default=3.5+random.random())
    recipeServings = db.Column(db.Integer, nullable=True)
    recipe_image = db.Column(db.Text, nullable=False, default='https://w7.pngwing.com/pngs/1013/530/png-transparent-cafe-italian-cuisine-breakfast-menu-eat-food-logo-eating-thumbnail.png')

    #Relationships
    reviews = db.relationship('Reviews', backref='recipe', lazy=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keywords = db.relationship('Keywords', secondary=recipe_keywords, lazy='subquery', backref=db.backref('recipes', lazy=True))
    ingredients = db.relationship('Ingredients', secondary=recipe_ingredients, lazy='subquery', backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return f"Recipe('{self.name}', '{self.datePublished}') \n '{self.description}'"
    
    def __eq__ (self , user):
        return self.id == user.id
    
    def to_dict(self):
        return {
            'recipe_id': self.id,
            'name': self.name, 
            'description': self.description, 
            'datePublished': self.datePublished,
            'reviewCount': self.reviewCount, 
            'avgRating': self.avgRating,
            'cooktime': self.cooktime,
            'preptime' : self.preptime,
            'recipeServings' : self.recipeServings,
            'ingredientAmt' : self.ingredientAmt,
            'recipe_image': self.recipe_image,
            'instructions': self.instructions,
            'keywords': [keyword.keyword for keyword in self.keywords],
            'ingredients': [{'name': ingredient.ingredient_name, 'amount': amount} for ingredient, amount in zip(self.ingredients, self.ingredientAmt.split(','))]
        }
    
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    reviewText = db.Column(db.Text, nullable=True)
    reviewLikes = db.Column(db.Integer, nullable=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f"Review: '{self.reviewText}' by '{self.user_id.author}'"
    
    def to_dict(self):
        return {
            'review_id': self.id,
            'datePosted': self.datePosted,
            'reviewText': self.reviewText,
            'reviewLikes': self.reviewLikes,
            'user_id': self.user_id
        }

collection_recipes = db.Table('collection_recipes',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collectionName = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipes = db.relationship('Recipe', secondary=collection_recipes, lazy='subquery', backref=db.backref('recipes', lazy=True))
    collection_image = db.Column(db.Text, nullable=False, default='/static/collection_pics/default.jpg')

    def __repr__(self):
        return f"Collection '{self.collectionName}' created by '{self.user_id.author}'"
    
    def __eq__ (self , user):
        return self.id == user.id
    
    def to_dict(self):
        return {
            'collection_id': self.id,
            'collection_name': self.name, 
            'user_id' : self.user_id,
            'recipes' : self.recipes
        }