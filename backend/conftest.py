import pytest
import json
from flask_login import login_user , current_user
from goodeats import app, db
from goodeats.models import User,Recipe,Keywords,Ingredients


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        client = app.test_client()
        
        yield client
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user():
    return User(
        username='testuser',
        name='Test User',
        email='test@example.com',
        password='testpassword'
    )
    

@pytest.fixture
def login_user(client, user):
    db.session.add(user)
    db.session.commit()

    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword',
        'remember': 'false'
    })

    return user



@pytest.fixture
def new_recipe(client,current_user):

    with app.app_context():
        # create a test user
        # user = User(username='testuser', email='testuser@example.com')
        # user.set_password('testpassword')
        # db.session.add(user)
        # db.session.commit()

        keyword1 = Keywords(keyword='test')
        keyword2 = Keywords(keyword='recipe')
        ingredient1 = Ingredients(ingredient_name='test_ingredient1')
        ingredient2 = Ingredients(ingredient_name='test_ingredient2')
        recipe = Recipe(name='test_recipe', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', user_id = current_user.id, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
        db.session.add(recipe)
        db.session.commit()
        # client.post('recipe/post' , json = recipe.to_dict)
        
        yield recipe

        # cleanup
        db.session.delete(recipe)
        # db.session.delete(user)
        db.session.commit()

