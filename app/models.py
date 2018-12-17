from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    ebay_store = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.body)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), index=True)
    item_price = db.Column(db.Float)
    item_category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_title = db.Column(db.String(120), index=True)
    item_price = db.Column(db.Float)
    item_category = db.Column(db.String(120))
    selling_state = db.Column(db.String(60))
    img_url = db.Column(db.String)
    ebay_item_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))