from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin):
    def __init__(self, id, is_anonymous=False):
        self.id = id
        self.is_anonymous = is_anonymous

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return not self.is_anonymous

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.is_anonymous


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    image_url = db.Column(db.String(255), nullable=True)
