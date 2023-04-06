from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from goodeats import app, db, bcrypt
from goodeats.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeForm
from goodeats.models import User, Keywords, Ingredients, Recipe, Collections


@app.route("/")
@app.route("/home")
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', posts=recipes)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'success')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email and address do not match. Please enter correct email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/<username>")
def profile(username):
    return render_template('account.html', user=User.query.filter_by(username).first_or_404())

@app.route("/<username>/update", methods=['GET', 'POST'])
@login_required
def update_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if(current_user != user):
        abort(403)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('/<username>'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/<username>/delete", methods=['POST'])
@login_required
def deleteUser(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.author != current_user:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/recipe/post", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        ingredients_list = []
        for ingredient in form.ingredients:
            quantity = ingredient.quantity.data
            ingredient_amount = f"{quantity}"
            ingredients_list.append(ingredient_amount)

        recipe = Recipe(name=form.name.data, author=current_user, instructions=form.instructions.data, 
                        description=form.description.data, ingredientAmt=", ".join(ingredients_list), 
                        cooktime=form.cooktime.data, preptime=form.preptime.data, recipeServings=form.recipeServings.data,
                        nutritionalFacts=form.nutritionalFacts.data)
        
        for ingredient_form in form.ingredients.data:
            name = ingredient_form.name.data
            ingredient = Ingredients.query.filter_by(ingredient_name=name).first()
            if(ingredient):
                recipe.ingredients.append(ingredient)
            else:
                new_ingredient = Ingredients(ingredient_name = name)
                recipe.ingredients.append(new_ingredient)
        
        for key in form.keywords.data:
            keyword = Keywords.query.filter_by(keyword=key.data).first()
            if(keyword):
                recipe.keywords.append(keyword)
            else:
                new_keyword = Keywords(keyword=key)
                recipe.keywords.append(new_keyword)

        db.session.add(recipe)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.name, post=recipe)

@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.instructions = form.instructions.data
        recipe.description = form.description.data
        recipe.cooktime = form.cooktime.data
        recipe.preptime = form.preptime.data
        recipe.recipeServings = form.recipeServings.data

        recipe.ingredients.clear()
        recipe.keywords.clear()
        ingredients_list = []

        for ingredient_form in form.ingredients:
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

        for key in form.keywords.data:
            keyword = Keywords.query.filter_by(keyword=key).first()
            if(keyword):
                recipe.keywords.append(keyword)
            else:
                new_keyword = Keywords(keyword=key)
                recipe.keywords.append(new_keyword)

        recipe.ingredientAmt = ", ".join(ingredients_list)
        db.session.commit()
        return redirect(url_for('recipe', post_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.name
        form.instructions.data = recipe.instructions
        form.description.data = recipe.description
        form.cooktime.data = recipe.cooktime
        form.preptime.data = recipe.preptime
        form.recipeServings.data = recipe.recipeServings

        # Populate Ingredients field
        form.ingredients.entries.clear() # clear any existing entries
        ingredient_amounts = recipe.ingredientAmt.split(', ')
        for i in range(0, len(recipe.ingredients)):
            form.ingredients.append_entry({'name': recipe.ingredients[i].name, 'quantity': ingredient_amounts[i]})

        #Populate nutritional facts
        form.nutritionalFacts.calories.data = recipe.calories
        form.nutritionalFacts.carbohydrates.data = recipe.carbohydrates
        form.nutritionalFacts.saturatedFats.data = recipe.saturatedFats
        form.nutritionalFacts.cholestrol.data = recipe.cholestrol
        form.nutritionalFacts.fat.data = recipe.fat
        form.nutritionalFacts.protein.data = recipe.protein
        form.nutritionalFacts.fibers.data = recipe.fibers
        form.nutritionalFacts.sugar.data = recipe.sugar
        form.nutritionalFacts.sodium.data = recipe.sodium

    return render_template('create_recipe.html', title='Update Recipe',form=form, legend='Update Recipe')

@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_post(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/<username>/recipes")
def user_recipes(username):
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(author=user).all()
    return render_template('user_recipes.html', user=user, recipes=recipes)

