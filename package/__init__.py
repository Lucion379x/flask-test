from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = 'salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


db = SQLAlchemy(app)
manager = LoginManager(app)
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')

from package import models, routes

db.create_all()