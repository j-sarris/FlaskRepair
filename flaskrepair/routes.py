import secrets, os
from flask import render_template, url_for, flash, redirect, request
from flaskrepair import app, db, bcrypt
from flaskrepair.forms import RegistrationForm, LoginForm, UpdateAccountForm, RepairForm
from flaskrepair.models import User, Repair
from flask_login import login_user, current_user, logout_user, login_required


def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/display")
def display():
    return render_template("display.html")

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf=8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Ο λογαριασμός για τον χρήστη {form.username.data} δημιουργήθηκε. Μπορείτε να συνδεθείτε.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
  
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Ο χρήστης {form.username.data} συνδέθηκε επιτυχώς.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('display'))  
        else:
            flash('Αποτυχημένη σύνδεση. Ελέγξτε όνομα χρήστη και κωδικό.', 'danger')
    return render_template('login.html', form=form)

@app.route("/repair/new", methods=['GET', 'POST'])
@login_required
def new_repair():
    form = RepairForm()
    if form.validate_on_submit():
        flash('Η φόρμα υποβλήθηκε.', 'success')
        return redirect(url_for('home'))
    return render_template('repair.html', form=form) 

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ο λογαριασμός ενημερώθηκε.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'images/' + current_user.image_file) 
    return render_template('account.html', image_file=image_file, form=form)