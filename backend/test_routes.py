import json
import pytest
from goodeats import app, db, bcrypt
from goodeats.models import User, Recipe,Keywords,Ingredients , Reviews , Collections
from flask import url_for
from flask_login import current_user
from goodeats.forms import UpdateProfileForm
import re

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

    # response3 = client.get('/check')
    # print(json.loads(response3.data))
    # assert response3.status_code == 200
    # # assert json.loads(response3.data)['message'] == 'You have logged in successfully'

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

def test_search(client , login_user):
    recipe_data1 = {
        "name": "Testw Recipe",
        "instructions": "Teswt instructions",
        "description": "Test wdescription",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["chicken", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }
   
    response1 = client.post('/recipe/post', json=recipe_data1)
    # print(response1.text)
    assert response1.status_code == 200

    recipe_data2 = {
        "name": "Test Recipe",
        "instructions": "Test instructions",
        "description": "Test description",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["chicken", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "Test Keyword 2"]
    }

    response2 = client.post('/recipe/post', json=recipe_data2)
    assert response2.status_code == 200
    recipe_data3 = {
        "name": "Test Recipwqe",
        "instructions": "Test insqwtructions",
        "description": "Test descrwqiption",
        "cooktime": '30',
        "preptime": '15',
        "recipeServings": 4,
        "ingredients": [["Ingredient 1", "1 cup"], ["Ingredient 2", "2 cups"]],
        "keywords": ["Test Keyword 1", "chicken"]
    }
    response3 = client.post('/recipe/post', json=recipe_data3)
    assert response3.status_code == 200

    response = client.get('/search', json={'search_query': 'chicken'})
    assert response.status_code == 200
    data = response.json
    for recipe in data:
        print(recipe)
    assert len(data) > 0


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

    res = client.get(f'/recipe/{recipe_id}/reviews')
    assert res.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert len(data['user_reviews']) == 2
    assert data['user_reviews'][0]['reviewText'] == review1.reviewText
    assert data['user_reviews'][1]['reviewText'] == review2.reviewText
    assert len(data['other_reviews']) == 0

def test_get_reviews(client,login_user):

    user = User(username='testy_user', name = "Testy" , email='testy_user@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='Chicken Curry', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', author = user, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()
    # user = User(username='testuser', email='test@example.com', password='testpassword')
    review1 = Reviews(reviewText='This chicken curry was amazing!', rating=5, recipe_id=recipe.id , user_id = 2)
    review2 = Reviews(reviewText='The chicken was a bit dry, but the sauce was good', rating=3, recipe_id=recipe.id, user_id = login_user.id)

    # Add objects to the database
    db.session.add_all([review1, review2])
    db.session.commit()

    # Make request to endpoint
    response = client.get(f'/recipe/{recipe.id}/reviews')

    # Check response status code
    assert response.status_code == 200

    # Check response data
    data = response.get_json()
    assert 'user_reviews' in data
    assert 'other_reviews' in data
    assert len(data['user_reviews']) == 1
    assert len(data['other_reviews']) == 1
    assert data['other_reviews'][0]['reviewText'] == 'This chicken curry was amazing!'
    assert data['user_reviews'][0]['reviewText'] == 'The chicken was a bit dry, but the sauce was good'

def test_add_review(client,login_user):
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='Chicken Curry', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', user_id = 1, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()
    print(login_user.id)
    response = client.post(f'/recipe/{recipe.id}/reviews/new', json={
        'rating': 4,
        'review_text': 'Test Review',
        'user_id' : login_user.id,
        'recipe_id': recipe.id
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    # assert 'message' in data
    # assert data['message'] == 'Review successfully added'
    assert Reviews.query.count() == 1
    review = Reviews.query.first()
    assert review.rating == 4
    assert review.reviewText == 'Test Review'
    assert review.recipe_id == recipe.id

def test_change_review_like(client, login_user):
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='Chicken Curry', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', user_id = 1, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()
    # create a review for the recipe
    review = {'rating': 4, 'review_text': 'Great recipe!' , 'recipe_id' : 1 , 'user_id' : login_user.id}
    response = client.post(f"/recipe/{recipe.id}/reviews/new", json=review)
    assert response.status_code == 200

    # get the ID of the new review
    review_id = response.json['review_id']

    # like the review
    data1 = {'review_id': review_id, 'liked': True}
    response1 = client.post(f"/recipe/{recipe.id}/reviews/like", json=data1)
    assert response1.status_code == 200
    # assert response1.json['message'] == 'Success'

    # check that the review was liked
    response2 = client.get(f"/recipe/{recipe.id}/reviews")
    assert response2.status_code == 200
    # assert len(response2.json['user_reviews']) == 1
    # assert response2.json['user_reviews'][0]['reviewLikes'] == 1

    # unlike the review
    data2 = {'review_id': review_id, 'unliked': True}
    response3 = client.post(f"/recipe/{recipe.id}/reviews/like", json=data2)
    assert response3.status_code == 200
    # assert response3.json['message'] == 'Success'

    # check that the review was unliked
    response4 = client.get(f"/recipe/{recipe.id}/reviews")
    assert response4.status_code == 200
    # assert len(response4.json['user_reviews']) == 1
    # assert response4.json['user_reviews'][0]['reviewLikes'] == 0

def test_delete_review(client, login_user ):
    # create a recipe and add a review to it
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='Chicken Curry', description='test_description', instructions='test_instructions',
                    ingredientAmt='1,2', cooktime='30', preptime='10', user_id = 1, 
                    reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                    ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()
    review = Reviews(rating=3, reviewText="Test Review1", recipe_id=recipe.id, user_id=login_user.id)
    db.session.add(review)
    db.session.commit()
    
    response = client.post(f"/recipe/{recipe.id}/reviews/delete", json={'review_id': review.id})
    assert response.status_code == 200
    assert b"Review deleted successfully." in response.data

    # try deleting a non-existent review
    response = client.post(f"/recipe/{recipe.id}/reviews/delete", json={'review_id': 100})
    assert response.status_code == 404

def test_collections(client, login_user):
    # Test POST request
    collection_name = "Test Collection"
    response = client.post(f"/{login_user.username}/collections", json={'name': collection_name})
    assert response.status_code == 200

    new_user = User(username='testuse1r', email='testu1ser@example.com' , name = "Tets" , password = "hi")
    db.session.add(new_user)
    db.session.commit()

    # Test GET request
    response = client.get(f"/{new_user.username}/collections")
    assert response.status_code == 200
    assert response.json == []

    response = client.get(f"/{login_user.username}/collections")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == collection_name

def test_addtocollection_and_collectionrecipes(client,login_user):
    collection = Collections(name = "Test Collection" , user_id = login_user.id , recipes =[])
    db.session.add(collection)
    db.session.commit()
    
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='test_recipe', description='test_description', instructions='test_instructions',
                ingredientAmt='1,2', cooktime='30', preptime='10', user_id = login_user.id, 
                reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()

    response = client.post(f"/recipe/{recipe.id}" , json = {"collection_id" : collection.id})
    assert response.status_code == 200

    response2 = client.get(f"/{login_user.username}/collections/{collection.id}")
    assert response2.status_code == 200
    data = json.loads(response2.data)
    print(data)
    assert data[0]['name'] == "test_recipe"

def test_delete_collection(client, login_user):
    response = client.post(f'/{login_user.username}/collections', json={'name': 'Test Collection'})
    assert response.status_code == 200
    collection_id = response.json['collection_id']
    print(collection_id , login_user.username)

    response1 = client.post(f'/{login_user.username}/collections/{collection_id}/delete' )
    print(response1.data)
    assert response1.status_code == 200
    assert response1.json['message'] == 'Collection deleted successfully.'

def test_get_following(client, login_user):
    # Create a user to follow
    followed_user = User(username='testy_user' , name = 'Tet User' , email = 'hi@gmail.com' , password = "hi")
    db.session.add(followed_user)
    db.session.commit()

    # Make current user follow the test user
    login_user.following.append(followed_user)
    db.session.commit()
    # followed_user.followers.append(login_user)
    # db.session.commit()
    print(followed_user.followers.all())

    # Test GET request
    response1 = client.get(f'/{login_user.username}/following')
    assert response1.status_code == 200
    assert response1.json == [{'username': 'testy_user'}]

    # Test POST request
    data = {'following_id': followed_user.id}
    response2 = client.post(f'/{login_user.username}/following', json=data)
    assert response2.status_code == 200
    assert response2.json == {'message': 'User successfully unfollowed!'}

    # Check that the user has been removed from following list
    assert followed_user not in login_user.following

    # Test case where user is not in following list
    data = {'following_id': followed_user.id}
    response3 = client.post(f'/{login_user.username}/following', json=data)
    assert response3.status_code == 400
    assert response3.json == {'message': 'User does not exist'}


def test_change_following(client, login_user):
    # create a user to follow
    user = User(username='testy_user', name = "Testy" , email='testy_user@example.com', password='password')
    db.session.add(user)
    db.session.commit()
    # print(user.id , login_user.id)
    # create a recipe by the user
    keyword1 = Keywords(keyword='test')
    keyword2 = Keywords(keyword='recipe')
    ingredient1 = Ingredients(ingredient_name='test_ingredient1')
    ingredient2 = Ingredients(ingredient_name='test_ingredient2')
    recipe = Recipe(name='test_recipe', description='test_description', instructions='test_instructions',
                ingredientAmt='1,2', cooktime='30', preptime='10', author = user, 
                reviewCount=0, avgRating=0, recipeServings=4, keywords=[keyword1, keyword2],
                ingredients=[ingredient1, ingredient2])
    db.session.add(recipe)
    db.session.commit()

    # follow the user by POST request
    response = client.post(f'/recipe/{recipe.id}/follow')
    print(response.data)
    assert response.status_code == 200
    assert response.json == {'message': f'You are now following {user.username}'}

    # unfollow the user by POST request
    response1 = client.post(f'/recipe/{recipe.id}/follow')
    assert response1.status_code == 400
    assert response1.json == {'message': f'You have successfully unfollowed {user.username}'}

def test_follow_user(client, login_user):
    # create a user to follow
    user_to_follow = User(username='testy_user', name = "Testy" , email='testy_user@example.com', password='password')
    db.session.add(user_to_follow)
    db.session.commit()

    # follow the user
    response = client.post(f'/{user_to_follow.username}/follow')
    assert response.status_code == 200
    assert response.json['message'] == f"You are now following {user_to_follow.username}"
    assert user_to_follow in login_user.following.all()

    # try to follow yourself
    response = client.post(f'/{login_user.username}/follow')
    assert response.status_code == 400
    assert response.json['message'] == 'You cannot follow yourself'
    assert login_user not in login_user.following.all()

    # unfollow the user
    response = client.post(f'/{user_to_follow.username}/follow')
    assert response.status_code == 400
    assert response.json['message'] == f"You have successfully unfollowed {user_to_follow.username}"
    assert user_to_follow not in login_user.following.all()





    
