from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from jinja2 import Environment, FileSystemLoader


app = Flask(__name__)
app.config['SECRET_KEY'] = '19e7e09074055362bf4032b218a7a315'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crdf.db'

env = Environment(loader=FileSystemLoader('templates'))
env.filters['tojson'] = jsonify


def format_datetime(value, format='%d/%m/%Y %H:%M:%S'):
    return value.strftime(format)

database= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'alert-info'

migrate = Migrate(app, database)

from crdf_web import routes




