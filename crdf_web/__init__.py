from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '19e7e09074055362bf4032b218a7a315'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crdf.db'




database= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'alert-info'

from crdf_web import routes


