from flask import request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from goodeats import app, db, bcrypt
from goodeats.forms import RegistrationForm, LoginForm, UpdateProfileForm, RecipeForm, NutritionalForm, IngredientForm
from goodeats.models import User, Keywords, Ingredients, Recipe, Collections

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    recipes = Recipe.query.all()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({
            'title': recipe.title,
            'description': recipe.description,
            'rating': recipe.avgRating
        })
    return jsonify(recipe_data), 200

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'You are already logged in!'}), 200
    data = request.get_json()
    form = RegistrationForm(username=data.get('username'), name=data.get('name'), email=data.get('email'), 
                            password=data.get('password'), confirm_password=data.get('confirm_password'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Your account has been created! You are now able to log in'}), 200
    else:
        return jsonify(form.errors), 400


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return jsonify({'message': 'You are already logged in.'}), 200
    
    # Parse the data
    data = request.get_json()
    form = LoginForm(username=data.get('username'), password=data.get('password'), remember=data.get('remember'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return jsonify({'message': 'You have logged in successfully'}), 200
        else:
            return jsonify({'message': 'Username and password do not match'}), 401
    else:
        return jsonify(form.errors), 400

@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'You have been logged out'}), 200

@app.route("/<username>", methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    response_data = {'username': user.username, 'name': user.name, 'email': user.email}
    return jsonify(response_data), 200

@app.route("/<username>/update", methods=['GET', 'POST'])
@login_required
def update_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    data = request.get_json()
    form = UpdateProfileForm(data=data)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        form_data = {
            'username': current_user.username,
            'email': current_user.email
        }
        return jsonify({'message': 'Your account has been update!d', 'form_data': form_data}), 200
    elif request.method == 'GET':
        form_data = {
            'username': current_user.username,
            'email': current_user.email
        }
        return jsonify({'form_data': form_data}), 200
    else:
        return jsonify(form.errors), 400

@app.route("/<username>/delete", methods=['POST'])
@login_required
def deleteUser(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200

@app.route("/recipe/post", methods=['POST'])
@login_required
def new_recipe():
    data = request.get_json()
    recipe_form = RecipeForm(data=data)
    ingredients_list = []
    for ingredient in data.get('ingredients'):
        recipe_form.ingredients.append(IngredientForm(ingredient[0], ingredient[1]))
        ingredients_list.append(ingredient[1])
    nutritional_data = {k: v for k, v in data.items() if k in NutritionalForm().data.keys()}
    recipe_form.nutritionalFacts = NutritionalForm(data=nutritional_data)

    if recipe_form.validate_on_submit():
        recipe = Recipe(name=recipe_form.name.data, author=current_user, instructions=recipe_form.instructions.data, 
                        description=recipe_form.description.data, ingredientAmt=", ".join(ingredients_list), 
                        cooktime=recipe_form.cooktime.data, preptime=recipe_form.preptime.data, recipeServings=recipe_form.recipeServings.data,
                        nutritionalFacts=recipe_form.nutritionalFacts.data)
        
        for ingredient_form in recipe_form.ingredients.data:
            name = ingredient_form.name.data
            ingredient = Ingredients.query.filter_by(ingredient_name=name).first()
            if(ingredient):
                recipe.ingredients.append(ingredient)
            else:
                new_ingredient = Ingredients(ingredient_name = name)
                recipe.ingredients.append(new_ingredient)
        
        for key in recipe_form.keywords.data:
            keyword = Keywords.query.filter_by(keyword=key.data).first()
            if(keyword):
                recipe.keywords.append(keyword)
            else:
                new_keyword = Keywords(keyword=key)
                recipe.keywords.append(new_keyword)

        db.session.add(recipe)
        db.session.commit()
        return jsonify({'message': 'Your post has been created!'}), 200
    
    else:
        return jsonify(recipe_form.errors), 400

@app.route("/recipe/<int:recipe_id>", methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    response_body = {
        'name': recipe.name, 'description': recipe.description, 'instructions': recipe.instructions,
        'keywords': [keyword.name for keyword in recipe.keywords],
        'ingredients': [{'name': ingredient.name, 'amount': amount} for ingredient, amount in zip(recipe.ingredients, recipe.ingredientAmt.split(','))],
        'datePublished': recipe.datePublished, 'cookTime': recipe.cooktime, 'prepTime': recipe.preptime, 
        'reviewCount': recipe.reviewCount, 'avgRating': recipe.avgRating, 'recipeServings': recipe.recipeServings,
        'calories': recipe.calories, 'carbohydrates': recipe.carbohydrates, 'saturatedFats': recipe.saturatedFats,
        'cholestrol': recipe.cholestrol, 'fat': recipe.fat, 'protein': recipe.protein,
        'fibers': recipe.fibers, 'sugar': recipe.sugar, 'sodium': recipe.sodium
    }
    return jsonify(response_body), 200

@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        return jsonify({'message': 'You do not have access to view this link'}), 403

    if request.method == 'POST':
        data = request.get_json()
        recipe_form = RecipeForm(data=data, ingredients=None, nutritionalFacts=None)
        ingredients_list = []
        for ingredient in data.get('ingredients'):
            recipe_form.ingredients.append(IngredientForm(ingredient[0], ingredient[1]))
            ingredients_list.append(ingredient[1])
        nutritional_data = {k: v for k, v in data.items() if k in NutritionalForm().data.keys()}
        recipe_form.nutritionalFacts = NutritionalForm(data=nutritional_data)

        if(recipe_form.validate_on_submit()):
            recipe.name = recipe_form.name.data
            recipe.instructions = recipe_form.instructions.data
            recipe.description = recipe_form.description.data
            recipe.cooktime = recipe_form.cooktime.data
            recipe.preptime = recipe_form.preptime.data
            recipe.recipeServings = recipe_form.recipeServings.data

            recipe.ingredients.clear()
            recipe.keywords.clear()
            ingredients_list = []

            for ingredient_form in recipe_form.ingredients:
                name = ingredient_form.name.data
                quantity = ingredient_form.quantity.data
                ingredient_amount = f"{quantity}"
                ingredients_list.append(ingredient_amount)
                ingredient = Ingredients.query.filter_by(ingredient_name=name).first()
                if(ingredient):
                    recipe.ingredients.append(ingredient)
                else:
                    new_ingredient = Ingredients(ingredient_name = name)
                    recipe.ingredients.append(new_ingredient)

            for key in recipe_form.keywords.data:
                keyword = Keywords.query.filter_by(keyword=key).first()
                if(keyword):
                    recipe.keywords.append(keyword)
                else:
                    new_keyword = Keywords(keyword=key)
                    recipe.keywords.append(new_keyword)

            recipe.ingredientAmt = ", ".join(ingredients_list)
            db.session.commit()
            return jsonify({'Your recipe has been updated!'}), 200
        else:
            return jsonify(recipe_form.errors), 400
    
    elif request.method == 'GET':
        response_body = {
            'name': recipe.name, 'description': recipe.description, 'instructions': recipe.instructions,
            'keywords': [keyword.name for keyword in recipe.keywords],
            'ingredients': [{'name': ingredient.name, 'amount': amount} for ingredient, amount in zip(recipe.ingredients, recipe.ingredientAmt.split(','))],
            'datePublished': recipe.datePublished, 'cookTime': recipe.cooktime, 'prepTime': recipe.preptime, 
            'reviewCount': recipe.reviewCount, 'avgRating': recipe.avgRating, 'recipeServings': recipe.recipeServings,
            'calories': recipe.calories, 'carbohydrates': recipe.carbohydrates, 'saturatedFats': recipe.saturatedFats,
            'cholestrol': recipe.cholestrol, 'fat': recipe.fat, 'protein': recipe.protein,
            'fibers': recipe.fibers, 'sugar': recipe.sugar, 'sodium': recipe.sodium
        }
        return jsonify(response_body), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 500

@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        return jsonify({'message': 'You do not have access to view this link'}), 403
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully.'}), 200

@app.route("/<username>/recipes")
def user_recipes(username):
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(author=user).all()
    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            'name': recipe.name, 'description': recipe.description, 'datePublished': recipe.datePublished,
            'reviewCount': recipe.reviewCount, 'avgRating': recipe.avgRating
        })
    return jsonify(recipe_list)

@app.route("/recipe/<int:recipe_id>")
def get_reviews(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    review_list = recipe.reviews
    user_reviews = [], other_reviews = []
    for review in review_list:
        if current_user.is_authenticated:
            if review.author == current_user:
                user_reviews.append(review)
            else:
                other_reviews.append(review)
        else:
            other_reviews.append(review)
    return jsonify(
        user_reviews=[review.to_dict() for review in user_reviews],
        other_reviews=[review.to_dict() for review in other_reviews]
    )
    