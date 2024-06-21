from datetime import datetime
from flaskrepair import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    repairs = db.relationship('Repair', backref='author', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    tel_no = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)    
    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware_option.id'), nullable=False)
    serial = db.Column(db.String(20))
    guarantee = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    hd = db.Column(db.Boolean)
    ram = db.Column(db.Boolean)
    graphcard = db.Column(db.Boolean)
    power = db.Column(db.Boolean)
    error_description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Repair('{self.id}', '{self.date_posted}', '{self.error}')"
    
class HardwareOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    repairs = db.relationship('Repair', backref='hardware', lazy=True)

    def __repr__(self):
        return f"HardwareOption('{self.name}')"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    telno = db.Column(db.Integer)
    code = db.Column(db.Integer)
    repairs = db.relationship('Repair', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.id}', '{self.first_name}', '{self.last_name}')"