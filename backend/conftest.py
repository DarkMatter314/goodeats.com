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


