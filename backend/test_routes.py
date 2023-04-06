# import unittest
# from flask import url_for
# from goodeats import app, db
# from goodeats.models import Recipe


# class TestRoutes(unittest.TestCase):

#     def setUp(self):
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#         with app.app_context():
#             db.create_all()

#             # Create a sample recipe
#             recipe = Recipe(name='Test Recipe', user_id=1,instructions= "hi" , description = "yo" , ingredientAmt = [0 , 2], ingredients = ["milk" , "brains"])
#             db.session.add(recipe)
#             db.session.commit()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()

#     def test_home_route(self):
#         with app.test_client() as client:
#             response = client.get(url_for('home'))
#             self.assertEqual(response.status_code, 200)
#             self.assertIn(b'Test Recipe', response.data)

import unittest
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from goodeats import app, db
from goodeats.models import User

class TestRegistrationAndLogin(unittest.TestCase):



    def setUp(self):
        with app.app_context():
            # db.drop_all()
            db.create_all()
            # Create a sample recipe
            # self.user = User(username='testuser',name = "test user", email='test@example.com', password='password')
            # db.session.add(self.user)
            # db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.session.execute('SET FOREIGN_KEY_CHECKS = 0')
            db.session.execute('DROP TABLE IF EXISTS collection_recipe')
            db.session.execute('DROP TABLE IF EXISTS recipe')
            db.session.execute('DROP TABLE IF EXISTS collection')
            db.session.execute('DROP TABLE IF EXISTS user')
            db.session.execute('SET FOREIGN_KEY_CHECKS = 1')
            db.session.commit()

    def test_register(self):
        with app.app_context():
            self.app = app.test_client()
            response = self.app.post(url_for('register'), data={
                'username': 'newuser',
                'name': 'New User',
                'email': 'newuser@example.com',
                'password': 'password',
                'confirm_password': 'password'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your account has been created! You are now able to log in', response.data)

    # def test_register_existing_user(self):
    #     response = self.client.post(url_for('register'), data={
    #         'username': 'testuser',
    #         'name': 'Test User',
    #         'email': 'test@example.com',
    #         'password': 'password',
    #         'confirm_password': 'password'
    #     }, follow_redirects=True)
    #     self.assert200(response)
    #     self.assertIn(b'Username already taken. Please choose a different one.', response.data)

    # def test_login(self):
    #     response = self.client.post(url_for('login'), data={
    #         'username': 'testuser',
    #         'password': 'password',
    #         'remember': False
    #     }, follow_redirects=True)
    #     self.assert200(response)
    #     self.assertIn(b'You are now logged in!', response.data)

    # def test_login_invalid_credentials(self):
    #     response = self.client.post(url_for('login'), data={
    #         'username': 'testuser',
    #         'password': 'wrongpassword',
    #         'remember': False
    #     }, follow_redirects=True)
    #     self.assert200(response)
    #     self.assertIn(b'Email and address do not match. Please enter correct email and password', response.data)

    # def test_logout(self):
    #     with self.client:
    #         self.client.post(url_for('login'), data={
    #             'username': 'testuser',
    #             'password': 'password',
    #             'remember': False
    #         })
    #         response = self.client.get(url_for('logout'), follow_redirects=True)
    #         self.assert200(response)
    #         self.assertIn(b'You have been logged out.', response.data)
