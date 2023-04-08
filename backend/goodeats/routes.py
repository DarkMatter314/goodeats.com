from flask import request, jsonify
from flask_login import login_user, current_user, logout_user, login_required 
from goodeats import app, db, bcrypt
# from goodeats.forms import RegistrationForm, LoginForm, UpdateProfileForm, RecipeForm, NutritionalForm, IngredientForm
from goodeats.forms import RegistrationForm, LoginForm, UpdateProfileForm, RecipeForm,  IngredientForm
from goodeats.models import User, Keywords, Ingredients, Recipe, Collections, Reviews
from wtforms import FieldList
from sqlalchemy import or_ , case

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    recipes = Recipe.query.order_by(Recipe.datePublished.desc()).paginate(per_page=10)
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({
            'id' : recipe.id,
            'name': recipe.name,
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
        if user and user.password==form.password.data:
            val = login_user(user, remember=form.remember.data)
            return jsonify({'message': 'You have logged in successfully', 'type':f"{val}"}), 200
        else:
            return jsonify({'message': 'Username and password do not match'}), 401
    else:
        return jsonify(form.errors), 400

@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'You have been logged out'}), 200

# @app.route("/check", methods=['GET'])
# @login_required
# def check():
#     id = current_user.id
#     return jsonify({'message': f"The current user is {id}"}), 200

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
    if request.method == 'POST':
        data = request.get_json()
        form = UpdateProfileForm(data=data)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.name = form.name.data
            current_user.email = form.email.data
            db.session.commit()
            form_data = {
                'username': current_user.username,
                'name' : current_user.name,
                'email': current_user.email
            }
            return jsonify({'message': 'Your account has been updated!', 'form_data': form_data}), 200
        else:
            return jsonify(form.errors), 400
    elif request.method == 'GET':
        print("hi")     
        form_data = {
            'username': current_user.username,
            'name' : current_user.name,
            'email': current_user.email
        }
        return jsonify(form_data), 200
    else:
        return jsonify({"message":"Bad Request"}), 400

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
    ingredients_list = [] 
    ing = []
    keywords=[]
    # print(data.get('ingredients'))
    for ingredient in data.get('ingredients'):
        ing.append(IngredientForm(ingredient_name = ingredient[0], quantity = ingredient[1]))
        ingredients_list.append(ingredient[1])
    for keyword in data.get('keywords'):
        keywords.append(keyword)
    recipe_form = RecipeForm(data=data, ingredients=ing, keywords=keywords)

    if recipe_form.validate_on_submit():
        recipe = Recipe(name=recipe_form.name.data, author=current_user, instructions=recipe_form.instructions.data, 
                        description=recipe_form.description.data, ingredientAmt=", ".join(ingredients_list), 
                        cooktime=recipe_form.cooktime.data, preptime=recipe_form.preptime.data, recipeServings=recipe_form.recipeServings.data)
        
        for ingredient_form in ing:
            name = ingredient_form.ingredient_name.data
            ingredient = Ingredients.query.filter_by(ingredient_name=name).first()
            # print(ingredient , name)
            if(ingredient):
                recipe.ingredients.append(ingredient)
            else:
                new_ingredient = Ingredients(ingredient_name = name)
                db.session.add(new_ingredient)
                db.session.commit()
                recipe.ingredients.append(new_ingredient)
        # return jsonify(recipe_form.ingredients.data) , 500
        for key in keywords:
            keyword = Keywords.query.filter_by(keyword=key).first()
            if(keyword):
                recipe.keywords.append(keyword)
            else:
                new_keyword = Keywords(keyword=key)
                db.session.add(new_keyword)
                db.session.commit()
                recipe.keywords.append(new_keyword)

        db.session.add(recipe)
        db.session.commit()
        return jsonify(recipe.to_dict()), 200
    
    else:
        return jsonify(recipe_form.errors), 400

@app.route("/recipe/<int:recipe_id>", methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    response_body = {
        'name': recipe.name, 'description': recipe.description, 'instructions': recipe.instructions,
        'keywords': [keyword.keyword for keyword in recipe.keywords],
        'ingredients': [{'name': ingredient.ingredient_name, 'amount': amount} for ingredient, amount in zip(recipe.ingredients, recipe.ingredientAmt.split(','))],
        'datePublished': recipe.datePublished, 'cooktime': recipe.cooktime, 'preptime': recipe.preptime, 
        'reviewCount': recipe.reviewCount, 'avgRating': recipe.avgRating, 'recipeServings': recipe.recipeServings
        # 'calories': recipe.calories, 'carbohydrates': recipe.carbohydrates, 'saturatedFats': recipe.saturatedFats,
        # 'cholestrol': recipe.cholestrol, 'fat': recipe.fat, 'protein': recipe.protein,
        # 'fibers': recipe.fibers, 'sugar': recipe.sugar, 'sodium': recipe.sodium
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
        # recipe_form = RecipeForm(data=data, ingredients=None, nutritionalFacts=None)
        # ingredients_list = []
        # for ingredient in data.get('ingredients'):
        #     recipe_form.ingredients.append(IngredientForm(ingredient[0], ingredient[1]))
        #     ingredients_list.append(ingredient[1])
        # nutritional_data = {k: v for k, v in data.items() if k in NutritionalForm().data.keys()}
        # recipe_form.nutritionalFacts = NutritionalForm(data=nutritional_data)
        ingredients_list = [] 
        ing = []
        keywords=[]
        # print(data.get('ingredients'))
        for ingredient in data.get('ingredients'):
            ing.append(IngredientForm(ingredient_name = ingredient[0], quantity = ingredient[1]))
            ingredients_list.append(ingredient[1])
        for keyword in data.get('keywords'):
            keywords.append(keyword)
        recipe_form = RecipeForm(data=data, ingredients=ing, keywords=keywords)
        
        if(recipe_form.validate_on_submit()):
            # print("hi")
            recipe.name = recipe_form.name.data
            recipe.instructions = recipe_form.instructions.data
            recipe.description = recipe_form.description.data
            recipe.cooktime = recipe_form.cooktime.data
            recipe.preptime = recipe_form.preptime.data
            recipe.recipeServings = recipe_form.recipeServings.data

            recipe.ingredients.clear()
            recipe.keywords.clear()
            ingredients_list = []

            for ingredient_form in ing:
                name = ingredient_form.ingredient_name.data
                quantity = ingredient_form.quantity.data
                ingredient_amount = f"{quantity}"
                ingredients_list.append(ingredient_amount)
                ingredient = Ingredients.query.filter_by(ingredient_name=name).first()
                if(ingredient):
                    recipe.ingredients.append(ingredient)
                else:
                    new_ingredient = Ingredients(ingredient_name = name)
                    db.session.add(new_ingredient)
                    db.session.commit()
                    recipe.ingredients.append(new_ingredient)

            for key in keywords:
                keyword = Keywords.query.filter_by(keyword=key).first()
                if(keyword):
                    recipe.keywords.append(keyword)
                else:
                    new_keyword = Keywords(keyword=key)
                    db.session.add(new_keyword)
                    db.session.commit()
                    recipe.keywords.append(new_keyword)

            recipe.ingredientAmt = ", ".join(ingredients_list)
            db.session.commit()
            return jsonify({'message': 'Your recipe has been updated!'}), 200
        else:
            return jsonify(recipe_form.errors), 400
    
    elif request.method == 'GET':
        response_body = {
            'name': recipe.name, 'description': recipe.description, 'instructions': recipe.instructions,
            'keywords': [keyword.keyword for keyword in recipe.keywords],
            'ingredients': [{'name': ingredient.ingredient_name, 'amount': amount} for ingredient, amount in zip(recipe.ingredients, recipe.ingredientAmt.split(','))],
            'datePublished': recipe.datePublished, 'cooktime': recipe.cooktime, 'preptime': recipe.preptime, 
            'reviewCount': recipe.reviewCount, 'avgRating': recipe.avgRating, 'recipeServings': recipe.recipeServings
            # 'calories': recipe.calories, 'carbohydrates': recipe.carbohydrates, 'saturatedFats': recipe.saturatedFats,
            # 'cholestrol': recipe.cholestrol, 'fat': recipe.fat, 'protein': recipe.protein,
            # 'fibers': recipe.fibers, 'sugar': recipe.sugar, 'sodium': recipe.sodium
        }
        return jsonify(response_body), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 400

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
        recipe_list.append(recipe.to_dict())
    return jsonify(recipe_list), 200


@app.route("/search", methods=['GET'])
def search():
    keywords = request.args.get('keywords', '').split(',')

    # Build the query to search for recipes
    name_match = [Recipe.name.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    keyword_match = [Keywords.keyword.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    ingredient_match = [Ingredients.ingredient_name.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    query = Recipe.query.filter(or_(*name_match)).outerjoin(Recipe.keywords).filter(or_(*keyword_match)
    ).outerjoin(
        Recipe.ingredients
    ).filter(
        or_(*ingredient_match)
    ).order_by(
    case(
        (Recipe.name.ilike('%{}%'.format(keywords)), 1),
        (Keywords.keyword.ilike('%{}%'.format(keywords)), 2),
        (Ingredients.ingredient_name.ilike('%{}%'.format(keywords)), 3),
        else_=4
    )
    )

    # Execute the query and return the results
    results = query.all()
    return jsonify([recipe.to_dict() for recipe in results])

@app.route("/recipe/<int:recipe_id>/reviews")
def get_reviews(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    review_list = recipe.reviews
    user_reviews = [] 
    other_reviews = []
    for review in review_list:
        if current_user.is_authenticated:
            if current_user == review.author:
                user_reviews.append(review)
            else:
                other_reviews.append(review)
        else:
            other_reviews.append(review)
    return jsonify({'user_reviews':[review.to_dict() for review in user_reviews],
                    'other_reviews':[review.to_dict() for review in other_reviews]}), 200

@app.route("/recipe/<int:recipe_id>/reviews/new", methods=['POST'])
@login_required
def add_review(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()
    review = Reviews(rating=data.get('rating'), reviewText = data.get('review_text'), recipe_id=recipe_id , user_id = current_user.id)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 200

@app.route("/recipe/<int:recipe_id>/reviews/like", methods=['POST'])
@login_required
def change_review_like(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()
    review_id = data.get('review_id')
    review = Reviews.query.get_or_404(review_id)
    if(data.get('liked') == True):
        review.reviewLikes = review.reviewLikes + 1
    elif(data.get('unliked') == True):
        if(review.reviewLikes <= 0):
            return jsonify({'message': 'HTTP Bad Request'}), 400
        review.reviewLikes = review.reviewLikes - 1
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Success'}), 200

@app.route("/recipe/<int:recipe_id>/reviews/delete", methods=['POST'])
@login_required
def delete_review(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()
    review_id = data.get('review_id')
    review = Reviews.query.get_or_404(review_id)
    if(review.author != current_user):
        return jsonify({'message': 'You do not have access to delete this review'}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully.'}), 200

@app.route("/<username>/collections", methods=['GET', 'POST'])
def collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(request.method == 'POST'):
        if(current_user != user):
            return jsonify({'message': 'You do not have access to view this link'}), 403
        data = request.get_json()
        # print(data.get('name') , user.id)
        new_collection = Collections(name=data.get('name'), user_id=user.id,recipes=[])
        db.session.add(new_collection)
        db.session.commit()
        return jsonify(new_collection.to_dict()), 200
    elif(request.method == 'GET'):
        user_collections = user.collections
        collection_list = []
        for collection in user_collections:
            collection_list.append({'name': collection.name})
        return jsonify(collection_list), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 400
    
@app.route("/<username>/collections/<int:collection_id>", methods=['GET'])
def collection_recipes(username, collection_id):
    user = User.query.filter_by(username=username).first_or_404()
    collection = Collections.query.get_or_404(collection_id)
    if(collection.author != user):
        return jsonify({'message':'The provided link does not exist'}), 400
    recipe_list = []
    for recipe in collection.recipes:
        recipe_list.append(recipe.to_dict())
    return jsonify(recipe_list), 200

@app.route("/recipe/<int:recipe_id>", methods=['POST'])
@login_required
def addtoCollection(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()
    collection_id = data.get('collection_id')
    collection = Collections.query.get_or_404(collection_id)
    if(collection.author != current_user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    collection.recipes.append(recipe)
    db.session.commit()
    return jsonify({'message': 'Successfully added recipe!'}), 200

@app.route("/<username>/collections/<int:collection_id>/delete", methods=['POST'])
@login_required
def delete_collection(collection_id , username):
    user = User.query.filter_by(username=username).first_or_404()
    collection = Collections.query.get_or_404(collection_id)
    if collection.author != current_user:
        return jsonify({'message': 'You do not have access to view this link'}), 403
    db.session.delete(collection)
    db.session.commit()
    return jsonify({'message': 'Collection deleted successfully.'}), 200

@app.route("/<username>/following", methods=['GET', 'POST'])
@login_required
def get_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    following = user.following.all()
    if request.method == 'POST':
        data = request.get_json()
        followed_id = data.get('following_id')
        followed_user = User.query.get_or_404(followed_id)
        if followed_user not in following:
            return jsonify({'message': 'User does not exist'}), 400
        current_user.following.remove(followed_user)
        db.session.commit()
        return jsonify({'message': 'User successfully unfollowed!'}), 200
    elif request.method == 'GET':
        following_list = []
        for followed_user in following:
            following_list.append({'username': followed_user.username})
        return jsonify(following_list), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 400



@app.route("/recipe/<int:recipe_id>/follow", methods=['POST'])
@login_required
def change_following(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    author = recipe.author
    # print(current_user.id , author.id)
    if current_user.id == author.id:
        return jsonify({'message': 'You cannot follow yourself'}), 400
    elif author in current_user.following.all():
        current_user.following.remove(author)
        db.session.commit()
        return jsonify({'message': f"You have successfully unfollowed {author.username}"}), 400
    else:
        current_user.following.append(author)
        db.session.commit()
        return jsonify({'message': f"You are now following {author.username}"}), 200
    
@app.route('/<username>/follow', methods=['POST'])
@login_required
def follow_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.id == user.id:
        return jsonify({'message': 'You cannot follow yourself'}), 400
    elif user in current_user.following.all():
        current_user.following.remove(user)
        db.session.commit()
        return jsonify({'message': f"You have successfully unfollowed {user.username}"}), 400
    else:
        current_user.following.append(user)
        db.session.commit()
        return jsonify({'message': f"You are now following {user.username}"}), 200