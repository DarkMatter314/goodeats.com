from flask import request, jsonify
# from flask_login import login_user, current_user, logout_user, login_required 
from goodeats import app, db, bcrypt
from goodeats.forms import RegistrationForm, LoginForm, UpdateProfileForm, RecipeForm,  IngredientForm
from goodeats.models import User, Keywords, Ingredients, Recipe, Collections, Reviews
from sqlalchemy import or_, case, and_
import goodeats.recommend as recommend

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to Good Eats!'}), 200

@app.route("/top_rated", methods=['GET'])
def top_rated():
    recipes = Recipe.query.order_by(Recipe.avgRating.desc()).paginate(per_page=10)
    recipe_count = Recipe.query.count()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    max_pages = recipe_count/10 if recipe_count%10 == 0 else recipe_count//10 + 1
    return jsonify({'recipe_data':recipe_data, 'max_pages':max_pages}), 200

@app.route("/popular_recipes", methods=['GET'])
def popular_recipes():
    recipes = Recipe.query.order_by(Recipe.reviewCount.desc()).paginate(per_page=10)
    recipe_count = Recipe.query.count()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    max_pages = recipe_count/10 if recipe_count%10 == 0 else recipe_count//10 + 1
    return jsonify({'recipe_data':recipe_data, 'max_pages':max_pages}), 200

@app.route("/easiest_recipes", methods = ['GET'])
def easiest_recipes():
    recipes = Recipe.query.order_by(Recipe.cooktime.desc()).paginate(per_page=10)
    recipe_count = Recipe.query.count()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    max_pages = recipe_count/10 if recipe_count%10 == 0 else recipe_count//10 + 1
    return jsonify({'recipe_data':recipe_data, 'max_pages':max_pages}), 200

@app.route("/latest_recipes", methods=['GET'])
def all_recipes():
    recipes = Recipe.query.order_by(Recipe.datePublished.desc()).paginate(per_page=10)
    recipe_count = Recipe.query.count()
    recipe_data = []
    for recipe in recipes:
        recipe_data.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    max_pages = recipe_count/10 if recipe_count%10 == 0 else recipe_count//10 + 1
    return jsonify({'recipe_data':recipe_data, 'max_pages':max_pages}), 200

@app.route("/recommend_recipes", methods=['GET', 'POST'])
def recommend_recipes():
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_id is None):
        return jsonify({'message': 'Error'}), 400
    user = User.query.get_or_404(user_id)
    recipe_ids = recommend.recipe_user(user_id)
    recipe_list = []
    for id in recipe_ids:
        recipe = Recipe.query.get_or_404(id)
        recipe_list.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    return jsonify({'recipe_data':recipe_list}), 200

@app.route("/recommend_users", methods=['GET', 'POST'])
def recommend_users():
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_id is None):
        return jsonify({'message': 'Error'}), 400
    user = User.query.get_or_404(user_id)
    user_ids = recommend.user_user(user_id)
    user_list = []
    for id in user_ids:
        user = User.query.get_or_404(id)
        user_list.append(user.to_dict())
    return jsonify({'user_data':user_list}), 200

@app.route("/register", methods=['GET', 'POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_id is not None):
        return jsonify({'message': 'You are already logged in!'}), 200
    form = RegistrationForm(username=data.get('username'), name=data.get('name'), email=data.get('email'), 
                            password=data.get('password'), confirm_password=data.get('confirm_password'),
                            profile_picture=data.get('profile_picture'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password, image_file=form.profile_picture.data)
        db.session.add(user)
        db.session.commit()
        favourite_collection = Collections(collectionName='Favourites', description='Your favourite recipes!', user_id=user.id)
        db.session.add(favourite_collection)
        user.favourites_id = favourite_collection.id
        db.session.commit()
        response = recommend.add_user(user)
        return jsonify({'message': 'Your account has been created! You are now able to log in', 'user_id': user.id}), 200
    else:
        return jsonify(form.errors), 400


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_id is not None):
        return jsonify({'message': 'You are already logged in.'}), 200
    
    # Parse the data
    form = LoginForm(username=data.get('username'), password=data.get('password'), remember=data.get('remember'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            return jsonify({'message': 'You have logged in successfully', 'user_id': f"{user.id}"}), 200
        else:
            return jsonify({'message': 'Username and password do not match'}), 401
    else:
        return jsonify(form.errors), 400

@app.route("/logout", methods=['POST'])
def logout():
    return jsonify({'message': 'You have been logged out'}), 200

@app.route("/<username>", methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_dict()), 200

@app.route("/<username>/update", methods=['GET', 'POST'])
# @login_required
def update_profile(username):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    if request.method == 'POST':
        form = UpdateProfileForm(data=data, current_user_username = current_user.username, current_user_email = current_user.email)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.name = form.name.data
            current_user.email = form.email.data
            if(data.get('user_image')):
                current_user.image_file = data.get('profile_picture')
            db.session.commit()
            return jsonify({'message': 'Your account has been updated!', 'form_data': current_user.to_dict()}), 200
        else:
            return jsonify(form.errors), 400
    elif request.method == 'GET':
        return jsonify({'form_data': current_user.to_dict()}), 200
    else:
        return jsonify({"message":"Bad Request"}), 400

@app.route("/<username>/delete", methods=['POST'])
# @login_required
def deleteUser(username):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200

@app.route("/recipe/post", methods=['POST'])
# @login_required
def new_recipe():
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    ingredients_list = [] 
    ing = []
    keywords=[]
    for ingredient in data.get('ingredients'):
        ing.append(IngredientForm(ingredient_name = ingredient[0], quantity = ingredient[1]))
        ingredients_list.append(ingredient[1])
    for keyword in data.get('keywords'):
        keywords.append(keyword)
    recipe_form = RecipeForm(data=data, ingredients=ing, keywords=keywords)

    if recipe_form.validate_on_submit():
        recipe = Recipe(name=recipe_form.name.data, author=current_user, instructions=recipe_form.instructions.data, 
                        description=recipe_form.description.data, ingredientAmt=", ".join(ingredients_list), 
                        cooktime=recipe_form.cooktime.data, preptime=recipe_form.preptime.data, recipeServings=int(recipe_form.recipeServings.data),
                        recipe_image=recipe_form.recipe_image.data, )
        
        for ingredient_form in ing:
            name = ingredient_form.ingredient_name.data
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

        db.session.add(recipe)
        db.session.commit()
        response = recommend.add_recipe(recipe, current_user)
        return jsonify({'recipe_data': recipe.to_dict(), 'user_data': current_user.to_dict()}), 200
    
    else:
        return jsonify(recipe_form.errors), 400

@app.route("/recipe/<int:recipe_id>", methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user = recipe.author
    return jsonify({'recipe_data': recipe.to_dict(), 'user_data': user.to_dict()}), 200

@app.route("/recipe/<int:recipe_id>", methods=['POST'])
def recipe_loggedin(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_id is None):
        return jsonify({'message': 'Error'}), 400
    current_user = User.query.get_or_404(user_id)
    user = recipe.author
    response = recommend.add_view(user_id, recipe_id)
    return jsonify({'recipe_data': recipe.to_dict(), 'user_data': user.to_dict()}), 200

@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
# @login_required
def update_recipe(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        return jsonify({'message': 'You do not have access to view this link'}), 403

    if request.method == 'POST':
        ingredients_list = [] 
        ing = []
        keywords=[]
        for ingredient in data.get('ingredients'):
            ing.append(IngredientForm(ingredient_name = ingredient[0], quantity = ingredient[1]))
            ingredients_list.append(ingredient[1])
        for keyword in data.get('keywords'):
            keywords.append(keyword)
        recipe_form = RecipeForm(data=data, ingredients=ing, keywords=keywords)
        
        if(recipe_form.validate_on_submit()):
            recipe.name = recipe_form.name.data
            recipe.instructions = recipe_form.instructions.data
            recipe.description = recipe_form.description.data
            recipe.cooktime = recipe_form.cooktime.data
            recipe.preptime = recipe_form.preptime.data
            recipe.recipeServings = recipe_form.recipeServings.data
            if(data.get('recipe_image')):
                recipe.recipe_image = data.get('recipe_image')

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
        user = recipe.author
        return jsonify({'recipe': recipe.to_dict(), 'user': user.to_dict()}), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 400

@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
# @login_required
def delete_recipe(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
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
        user = recipe.author
        recipe_dict = recipe.to_dict()
        recipe_list.append(recipe_dict)
    return jsonify({'recipe_data': recipe_list, 'user_data': user.to_dict()}), 200

@app.route("/search", methods=['GET'])
def search():
    keywords = request.args.get('keywords').split(',')
    page = request.args.get('page', 1, type=int)
    # Build the query to search for recipes
    name_match = []#[Recipe.name.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    keyword_match = [Keywords.keyword.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    ingredient_match =[]# [Ingredients.ingredient_name.ilike('%{}%'.format(keyword.strip())) for keyword in keywords]
    query = Recipe.query.filter(or_(*name_match)).outerjoin(Recipe.keywords).filter(or_(*keyword_match)
    ).outerjoin(Recipe.ingredients).filter(or_(*ingredient_match)
    ).order_by(
    case(
        (Recipe.name.ilike('%{}%'.format(keywords)), 1),
        (Keywords.keyword.ilike('%{}%'.format(keywords)), 1),
        (Ingredients.ingredient_name.ilike('%{}%'.format(keywords)), 3),
        else_=4
    ))                                                                                                 
    results = query.all()
    
    # Execute the query and return the results
    
    recipe_count = len(list(results))
    max_pages = (recipe_count//10) if (recipe_count%10 == 0) else (recipe_count//10 + 1)
    recipe_data = []
    for recipe in results:
        recipe_data.append({'recipe': recipe.to_dict(), 'user': recipe.author.to_dict()})
    return jsonify({'recipe_data':recipe_data, 'max_pages': max_pages})

@app.route("/recipe/<int:recipe_id>/reviews", methods=['GET', 'POST'])
def get_reviews(recipe_id):
    data = request.get_json()
    user_id = data.get('user_id')
    current_user = User.query.get_or_404(user_id) if user_id else None
    recipe = Recipe.query.get_or_404(recipe_id)
    review_list = recipe.reviews
    user_reviews = [] 
    other_reviews = []
    for review in review_list:
        if current_user is not None:
            review_user = User.query.get(review.user_id)
            if (review_user is not None) and (current_user == review_user):
                user_reviews.append(review)
            else:
                other_reviews.append(review)
        else:
            other_reviews.append(review)
    return jsonify({'user_reviews':[review.to_dict() for review in user_reviews],
                    'other_reviews':[review.to_dict() for review in other_reviews]}), 200

@app.route("/recipe/<int:recipe_id>/reviews/new", methods=['POST'])
# @login_required
def add_review(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
    review = Reviews(rating=data.get('rating'), reviewText = data.get('review_text'), recipe_id=recipe_id , user_id = current_user.id)
    response = recommend.add_rating(current_user.id, recipe_id, data.get('rating'))
    db.session.add(review)
    recipe_rating = recipe.avgRating
    recipe_count = recipe.reviewCount
    recipe.avgRating = (recipe_rating * recipe_count + data.get('rating'))/(recipe_count + 1)
    recipe.reviewCount = recipe_count + 1
    db.session.commit()
    return jsonify(review.to_dict()), 200

@app.route("/recipe/<int:recipe_id>/reviews/like", methods=['POST'])
# @login_required
def change_review_like(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
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
# @login_required
def delete_review(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
    review_id = data.get('review_id')
    review = Reviews.query.get_or_404(review_id)
    if(review.author != current_user):
        return jsonify({'message': 'You do not have access to delete this review'}), 403
    db.session.delete(review)
    recipe_rating = recipe.avgRating
    recipe_count = recipe.reviewCount
    recipe.avgRating = (recipe_rating * recipe_count - data.get('rating'))/(recipe_count - 1)
    recipe.reviewCount = recipe_count - 1  
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully.'}), 200

@app.route("/<username>/collections", methods=['GET', 'POST'])
def collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(request.method == 'POST'):
        data = request.get_json()
        user_id = data.get('user_id')
        current_user = User.query.get_or_404(user_id)
        if(current_user != user):
            return jsonify({'message': 'You do not have access to view this link'}), 403
        data = request.get_json()
        
        new_collection = Collections(collectionName=data.get('name'), user_id=user.id, recipes=[], description=data.get('description'))
        db.session.add(new_collection)
        db.session.commit()
        return jsonify(new_collection.to_dict()), 200

    elif(request.method == 'GET'):
        user_collections = user.collections
        collection_list = []
        for collection in user_collections:
            collection_list.append(collection.to_dict())
        return jsonify(collection_list), 200
    else:
        return jsonify({'message': 'HTTP Bad Request'}), 401
    
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

#for adding
@app.route("/recipe/collection/<int:recipe_id>/", methods=['POST'])
# @login_required
def addtoCollection(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
    collection_id = data.get('collection_id')
    collection = Collections.query.get_or_404(collection_id)
    if(collection.author != current_user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    collection.recipes.append(recipe)
    collection.collection_image = recipe.recipe_image
    response = recommend.add_bookmark(current_user.id, recipe_id)
    db.session.commit()
    return jsonify({'message': 'Successfully added recipe!'}), 200

@app.route("/<username>/collections/<int:collection_id>/delete", methods=['POST'])
# @login_required
def delete_collection(username, collection_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    user = User.query.filter_by(username=username).first_or_404()
    collection = Collections.query.get_or_404(collection_id)
    if collection.author != current_user:
        return jsonify({'message': 'You do not have access to view this link'}), 403
    db.session.delete(collection)
    db.session.commit()
    return jsonify({'message': 'Collection deleted successfully.'}), 200

@app.route("/<username>/following", methods=['GET', 'POST'])
# @login_required
def get_following(username):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        return jsonify({'message': 'You do not have access to view this link'}), 403
    following = user.following.all()
    if request.method == 'POST':
        followed_id = data.get('following_id')
        followed_user = User.query.get_or_404(followed_id)
        if followed_user not in following:
            return jsonify({'message': 'User does not exist'}), 400
        current_user.following.remove(followed_user)
        followed_user.follower_count = followed_user.follower_count - 1
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
# @login_required
def change_following(recipe_id):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    recipe = Recipe.query.get_or_404(recipe_id)
    author = recipe.author
    if current_user.id == author.id:
        return jsonify({'message': 'You cannot follow yourself'}), 400
    elif author in current_user.following.all():
        current_user.following.remove(author)
        author.follower_count = author.follower_count - 1
        db.session.commit()
        return jsonify({'message': f"You have successfully unfollowed {author.username}"}), 400
    else:
        current_user.following.append(author)
        author.follower_count = author.follower_count + 1
        db.session.commit()
        return jsonify({'message': f"You are now following {author.username}"}), 200
    
@app.route('/<username>/follow', methods=['POST'])
# @login_required
def follow_user(username):
    data = request.get_json()
    current_user = User.query.get_or_404(data.get('user_id'))
    user = User.query.filter_by(username=username).first_or_404()

    if current_user == user:
        return jsonify({'message': 'You cannot follow yourself'}), 400
    elif user in current_user.following.all():
        current_user.following.remove(user)
        user.follower_count = user.follower_count - 1
        db.session.commit()
        return jsonify({'message': f"You have successfully unfollowed {user.username}"}), 400
    else:
        current_user.following.append(user)
        user.follower_count = user.follower_count + 1
        db.session.commit()
        return jsonify({'message': f"You are now following {user.username}"}), 200
