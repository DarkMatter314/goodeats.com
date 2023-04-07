from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from goodeats.database import db
from goodeats.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:naman12#$@localhost:3306/recipedatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['WTF_CSRF_ENABLED'] = False
bcrypt = Bcrypt(app)
db.init_app(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from goodeats import routes