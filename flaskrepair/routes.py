import secrets, os
from flask import render_template, url_for, flash, redirect, request, abort
from flaskrepair import app, db, bcrypt
from flaskrepair.forms import RegistrationForm, LoginForm, UpdateAccountForm, RepairForm
from flaskrepair.models import User, Repair, HardwareOption
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/display")
@login_required
def display():
    repairs = Repair.query.all()
    return render_template("display.html", repairs=repairs)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf=8')
        user = User(username=form.username.data, first_name=form.name.data, last_name=form.surname.data, phone=form.tel_no.data, 
                    email=form.email.data, password=hashed_password, admin=form.admin.data)
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

    author = User.query.get(current_user.id)  # Fetch the author details

    form = RepairForm()
    if form.validate_on_submit():
        repair = Repair(tel_no = form.tel_no.data, serial=form.serial.data, guarantee=form.guarantee.data, hardware_id=form.hardware_id.data,
                        error_description=form.error_description.data, client_id=form.client_id.data, duration=form.duration.data, 
                        hd=form.hd.data, ram=form.ram.data, graphcard=form.graphcard.data, power=form.power.data, 
                        user_name=current_user.username, user_id=current_user.id)
        db.session.add(repair)
        db.session.commit()
        flash('Το έντυπο τεχνικών εργασιών καταχωρίστηκε.', 'success')
        return redirect(url_for('display'))
    elif request.method == 'GET':
        form.tel_no.data = current_user.phone
        form.username.data = current_user.username
    return render_template('repair.html', form=form, legend = 'Εισαγωγή νέου Εντύπου Τεχνικών Εργασιών', author=author) 

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

@app.route("/repair/<int:repair_id>", methods=['GET', 'POST'])
@login_required
def update_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    if repair.author != current_user and not current_user.admin:
        abort(403)

    author = User.query.get(repair.user_id)  # Fetch the author details
    
    form = RepairForm()
    if form.validate_on_submit():
        repair.tel_no = form.tel_no.data
        repair.client_id = form.client_id.data
        repair.hardware_id = form.hardware_id.data
        repair.serial = form.serial.data
        repair.guarantee = form.guarantee.data 
        repair.duration = form.duration.data
        repair.hd = form.hd.data
        repair.ram = form.ram.data
        repair.graphcard = form.graphcard.data
        repair.power = form.power.data
        repair.error_description = form.error_description.data
        db.session.commit()
        flash('Το έντυπο τεχνικών εργασιών ενημερώθηκε.', 'success')
        return redirect(url_for('display'))
    elif request.method == 'GET':
        form.tel_no.data = repair.tel_no
        form.client_id.data = repair.client_id
        form.hardware_id.data = repair.hardware_id
        form.serial.data = repair.serial
        form.guarantee.data = repair.guarantee
        form.duration.data = repair.duration
        form.hd.data = repair.hd
        form.ram.data = repair.ram
        form.graphcard.data = repair.graphcard
        form.power.data = repair.power  
        form.error_description.data = repair.error_description
    return render_template('repair.html', form=form, legend = 'Ενημέρωση Εντύπου Τεχνικών Εργασιών', author=author, repair=repair)

@app.route("/repair/<int:repair_id>/delete", methods=['POST'])
@login_required
def delete_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    if repair.author != current_user and not current_user.admin:
        abort(403)
    db.session.delete(repair)
    db.session.commit()
    flash('Η εγγραφή διαγράφηκε.', 'success')
    return redirect(url_for('display'))
