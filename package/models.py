from flask_login import UserMixin
from datetime import datetime

from package import db, manager


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(128), nullable=False)
    
    
    def __repr__(self):
        return '<Post %r>' % self.id
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    
    
    
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)