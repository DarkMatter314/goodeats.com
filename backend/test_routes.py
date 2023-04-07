import json
import pytest
from goodeats import app, db, bcrypt
from goodeats.models import User, Recipe,Keywords,Ingredients , Reviews
from flask import url_for
from flask_login import current_user
from goodeats.forms import UpdateProfileForm

def test_home(client):
    with app.app_context():
        response = client.get('/home')
        assert response.status_code == 200
        assert len(json.loads(response.data)) == 0
        
        user = User(username='testuser', name='Test User', email='test@example.com', password=bcrypt.generate_password_hash('testpassword').decode('utf-8'))
        recipe = Recipe(name='Test Recipe', author=user, description='A test recipe', instructions='Cook it and enjoy', ingredientAmt='1 cup of flour', cooktime='30 min', preptime='10 min', recipeServings=2)
        db.session.add(user)
        db.session.add(recipe)
        db.session.commit()
        
        response = client.get('/home')
        assert response.status_code == 200
        
def test_register(client):
    response = client.post('/register', json={
        'username': 'newuser',
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })
    print(json.loads(response.data))
    assert response.status_code == 200
    assert json.loads(response.data)['message']== 'Your account has been created! You are now able to log in'
          
    response = client.post('/register', json={
        'username': 'newuser',
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })
    assert response.status_code == 400
    assert json.loads(response.data)['username']== ['That username has already been taken. Please choose a different one.']

def test_profile_route(client):
        # Replace "client" with the name of your Flask app's test client fixture
        user = User(username='testuser', name='Test User', email='test@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()
        username = "testuser"
        response = client.get(url_for("profile", username=username))
        
        # Check that the response status code is 200
        assert response.status_code == 200
        
        # Check that the response data contains the expected keys and values
        expected_data = {
            "username": "testuser",
            "name": "Test User",
            "email": "test@example.com"
        }
        print(json.loads(response.data))
        assert json.loads(response.data) == expected_data

def test_logout(client,login_user):
    response2 = client.post('/logout', follow_redirects=True)
    print(json.loads(response2.data))
    assert response2.status_code == 200 
    assert json.loads(response2.data)['message'] == 'You have been logged out'

def test_login_logout(client):
    user = User(username='testuser', name='Test User', email='test@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', json={
        'username': 'testuser', 
        'password': 'testpassword',
        'remember': 'false'
    })
    print(json.loads(response.data))
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'You have logged in successfully'

    response3 = client.get('/check')
    print(json.loads(response3.data))
    assert response3.status_code == 200
    # assert json.loads(response3.data)['message'] == 'You have logged in successfully'

    response2 = client.post('/logout', follow_redirects=True)
    print(json.loads(response2.data))
    assert response2.status_code == 200 
    assert json.loads(response2.data)['message'] == 'You have been logged out'

    response1 = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    print(json.loads(response1.data))
    assert response1.status_code == 401
    assert json.loads(response1.data)['message'] == 'Username and password do not match'

def test_update_profile_route(client , login_user):
   
    # Test GET request with logged-in user
    response1 = client.get(url_for("update_profile", username = login_user.username))
    
    print(response1.text)
    
    print(json.loads(response1.data))
    assert response1.status_code == 200
    assert json.loads(response1.data)["username"] == login_user.username
    
    # Test POST request with logged-in user and valid form data
    valid_data = {"username" : "testuser1" , "email" : "test_email@gmial.com" , "name" : "Tst User1"}
    response = client.post(
        url_for("update_profile", username = login_user.username),
        json=valid_data,
        content_type="application/json"
    )
    print(response.text)
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Your account has been updated!"
    assert json.loads(response.data)["form_data"] == valid_data
    
    # Test POST request with logged-in user and invalid form data
    invalid_data = {"username": "t","email" : "test_email@gmial.com" , "name" : "Tst User1"}  # This username is invalid according to the form validator
    response1 = client.post(
        url_for("update_profile", username=login_user.username),
        json=invalid_data,
        content_type="application/json"
    )
    print(json.loads(response1.data))
    assert response1.status_code == 400
    # assert json.loads(response1.data)["username"][0] == "Username must contain only letters, numbers, and underscores."

def test_delete_user(client, login_user):
    # Create a test user
    response = client.post(url_for("deleteUser", username = login_user.username))
    assert response.status_code == 200
    assert b'User deleted successfully.' in response.data

    # Check that user is actually deleted
    response = client.get(url_for('profile' , username = login_user.username))
    assert response.status_code == 404

def test_new_recipe(client, login_user):
    data = {
        'name': 'Test Recipe',
        'description': 'A delicious test recipe',
        'instructions': '1. Mix ingredients. 2. Cook for 30 minutes.',
        'cooktime': "30",
        'preptime': "10",
        'recipeServings': "1",
        'ingredients': [['flour', '2 cups'], ['sugar', '1 cup'], ['butter', '1 stick']],
        # 'calories': '500',
        # 'fat': '20',
        # 'protein':' 10',

        # 'carbohydrates': '70',
        'keywords': ['test', 'recipe']
    }
   
    response = client.post('/recipe/post', json = data , content_type='application/json')
    print(response.text)
    assert response.status_code == 200
    # assert b'Your post has been created!' in response.data
    # recipe = Recipe.query.filter_by(name='Test Recipe').first()
    # assert recipe is not None
    # print(recipe.cooktime)
    # print(recipe.ingredients)
    # print(recipe.keywords)
    # assert 0 == 1
    # assert recipe.author == login_user()
    # assert len(recipe.ingredients )== 3
    # assert len(recipe.keywords) == 2

def test_recipe(client):
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='test_recipe', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', user_id = 1, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()
    # Test valid request
    response = client.get('/recipe/1')
    assert response.status_code == 200
    response_body = json.loads(response.data)
    assert response_body['name'] == 'test_recipe'
    assert response_body['description'] == 'test_description'
    assert response_body['instructions'] == 'test_instructions'
    assert response_body['keywords'] == ['test', 'recipe']
    assert response_body['ingredients'] == [{'name': 'test_ingredient1', 'amount': '1'}, {'name': 'test_ingredient2', 'amount': '2'}]
    # assert response_body['datePublished'] == '2022-01-01'
    assert response_body['cooktime'] == '30'
    assert response_body['preptime'] == '10'
    assert response_body['reviewCount'] == 0
    assert response_body['avgRating'] == 0
    assert response_body['recipeServings'] == 4

    # Test invalid request
    response = client.get('/recipe/2')
    assert response.status_code == 404
    response_body = json.loads(response.data)
    assert response_body['error'] == 'Not found'

def test_update_recipe(client, login_user):
    # log in as a user
    # auth.login()
    
    # create a recipe to update
    recipe_data = {
        "name": "Test Recipe",
        "instructions": "Test instructions",
        "description": "Test description",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }
    response = client.post('/recipe/post', json=recipe_data)
    assert response.status_code == 200
    recipe_id = response.json['recipe_id']
    
    # update the recipe
    updated_data = {
        "name": "Updated Test Recipe",
        "instructions": "Updated test instructions",
        "description": "Updated test description",
        "cooktime": '45',
        "preptime": '10',
        "recipeServings": 6,
        "ingredients": [["Ingredient 1", "2 cups"], ["Ingredient 3", "1 cup"]],
        "keywords": ["Test Keyword 2", "Test Keyword 3"]
    }
    response1 = client.post(f'/recipe/{recipe_id}/update', json=updated_data)
    print(response1.text)
    assert response1.status_code == 200
    assert response1.json['message'] == 'Your recipe has been updated!'
    
    # check that the recipe was updated correctly
    response2 = client.get(f'/recipe/{recipe_id}')
    assert response2.status_code == 200
    updated_recipe = json.loads(response2.data)
    print(response2.data)
    # response_body = json.loads(response2.data)
    assert updated_recipe['name'] == "Updated Test Recipe"
    assert updated_recipe['instructions'] == "Updated test instructions"
    assert updated_recipe['description'] == "Updated test description"
    assert updated_recipe['cooktime'] == '45'
    assert updated_recipe['preptime'] == '10'
    assert updated_recipe['recipeServings'] == 6
    assert updated_recipe['ingredients'] == [{"amount":"2 cups","name":"Ingredient 1"},{"amount":" 1 cup","name":"Ingredient 3"}]

    assert "Test Keyword 1" not in updated_recipe['keywords']
    assert "Test Keyword 2" in updated_recipe['keywords']
    assert "Test Keyword 3" in updated_recipe['keywords']

    response3 = client.get(f'/recipe/{recipe_id}/update')
    assert response3.status_code == 200
    get_recipe = json.loads(response3.data)
    assert get_recipe['name'] == "Updated Test Recipe"
    assert get_recipe['instructions'] == "Updated test instructions"
    assert get_recipe['description'] == "Updated test description"
    assert get_recipe['cooktime'] == '45'
    assert get_recipe['preptime'] == '10'
    assert get_recipe['recipeServings'] == 6
    assert get_recipe['ingredients'] == [{"amount":"2 cups","name":"Ingredient 1"},{"amount":" 1 cup","name":"Ingredient 3"}]

    assert "Test Keyword 1" not in get_recipe['keywords']
    assert "Test Keyword 2" in get_recipe['keywords']
    assert "Test Keyword 3" in get_recipe['keywords']

def test_delete_recipe(client, login_user):
    # Log in as the author of the recipe
    # auth.login()
    recipe_data = {
        "name": "Test Recipe",
        "instructions": "Test instructions",
        "description": "Test description",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }
    response = client.post('/recipe/post', json=recipe_data)
    assert response.status_code == 200
    recipe_id = response.json['recipe_id']

    # Send a POST request to delete the recipe
    response = client.post(f'/recipe/{recipe_id}/delete')

    # Check that the response is valid
    assert response.status_code == 200
    assert response.json == {'message': 'Recipe deleted successfully.'}

    # Check that the recipe was actually deleted from the database
    assert Recipe.query.get(recipe_id) is None

def test_user_recipes(client, login_user):
    recipe_data = {
        "name": "Test Recipe",
        "instructions": "Test instructions",
        "description": "Test description",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }
    response = client.post('/recipe/post', json=recipe_data)
    assert response.status_code == 200
    recipe_id = response.json['recipe_id']

    response = client.get(f'/{login_user.username}/recipes')
    assert response.status_code == 200

    # data = response.get_json()
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Recipe'

def test_get_reviews(client, login_user):

    recipe_data = {
        "name": "Test Recipe",
        "instructions": "Test instructions",
        "description": "Test description",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }
    response = client.post('/recipe/post', json=recipe_data)
    assert response.status_code == 200
    recipe_id = response.json['recipe_id']

    response = client.get(f'/{login_user.username}/recipes')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Recipe'

    review1 = Reviews(
        reviewText='test review 1',
        rating=3,
        recipe_id=recipe_id,
        user_id=login_user.id
    )
    db.session.add(review1)
    db.session.commit()

    review2 = Reviews(
        reviewText='test review 2',
        rating=4,
        recipe_id=recipe_id,
        user_id=login_user.id
    )
    db.session.add(review2)
    db.session.commit()

    res = client.get(f'/recipe/{recipe_id}')
    assert res.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert len(data['user_reviews']) == 2
    assert data['user_reviews'][0]['reviewText'] == review1.reviewText
    assert data['user_reviews'][1]['reviewText'] == review2.reviewText
    assert len(data['other_reviews']) == 0







    
