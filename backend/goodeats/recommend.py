from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import random

client = RecombeeClient('goodeats-dev', 'pmyeJZzC6JqbAjDZuGWp15UVH1TkcQQMiguiE7xVj1WLEByom3SQJMY79ySiMf6Z')

def recipe_user(user_id):
    recommeded_recipes = (client.send(RecommendItemsToUser(str(user_id), 5)))['recomms']
    recipe_list = []
    for recipe in recommeded_recipes:
        recipe_list.append(int(recipe['id']))
    return recipe_list

def user_user(user_id):
    recommeded_users = (client.send(RecommendUsersToUser(str(user_id), 5)))['recomms']
    user_list = []
    for recipe in recommeded_users:
        user_list.append(int(recipe['id']))
    return user_list

def add_view(user_id, recipe_id):
    response = client.send(AddPurchase(str(user_id), str(recipe_id)))
    return response

def add_rating(user_id, recipe_id, rating):
    rate = (rating-3)/2
    response = client.send(AddRating(str(user_id), str(recipe_id), rate))
    return response

def add_bookmark(user_id, recipe_id):
    response = client.send(AddBookmark(str(user_id), str(recipe_id)))
    return response