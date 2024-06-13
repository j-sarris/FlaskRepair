from datetime import datetime
from flaskrepair import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    repairs = db.relationship('Repair', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(20), nullable=False)
    guarantee = db.Column(db.Integer)
    hardware = db.Column(db.String(20), nullable=False)
    error = db.Column(db.Text)
    client = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    hd = db.Column(db.Boolean)
    ram = db.Column(db.Boolean)
    graphcard = db.Column(db.Boolean)
    power = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Repair('{self.id}', '{self.date_posted}', '{self.error}')"