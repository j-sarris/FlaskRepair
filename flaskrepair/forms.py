from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user
from flaskrepair.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Όνομα χρήστη', validators=[DataRequired(message="Το όνομα του χρήστη δεν μπορεί να είναι κενό"), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email('Συμπληρώστε σωστό email της μορφής name@server')])
    password = PasswordField('Κωδικός', validators=[DataRequired()])
    confirm_password = PasswordField('Επιβεβαίωση κωδικού',
                                    validators=[DataRequired(), EqualTo('password', message="Η επιβεβαίωση δεν είναι ίδια με τον κωδικό")]) 
    submit = SubmitField('Εγγραφή')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
                raise ValidationError('Αυτό τό όνομα χρήστη χρησιμοποιείται ήδη. Επιλέξτε άλλο όνομα.')
        
class UpdateAccountForm(FlaskForm):
    username = StringField('Όνομα χρήστη', validators=[DataRequired(message="Το όνομα του χρήστη δεν μπορεί να είναι κενό"), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email('Συμπληρώστε σωστό email της μορφής name@server')])
    pic = FileField('Εικόνα λογαριασμού', validators=[FileAllowed(['png', 'jpg'], 'Λάθος τύπος αρχείου. Επιτρεπτοί τύποι .jpg, .png')])
    submit = SubmitField('Ενημέρωση')

    def validate_username(self, username):
        if username.data != current_user.username:
             user = User.query.filter_by(username=username.data).first()
             if user:
                raise ValidationError('Αυτό τό όνομα χρήστη χρησιμοποιείται ήδη. Επιλέξτε άλλο όνομα.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Σύνδεση')

class RepairForm(FlaskForm):
    serial = StringField('Σειριακός Αριθμός', validators=[DataRequired()])
    error_description = TextAreaField('Περιγραφή βλάβης', validators=[DataRequired()])
    submit = SubmitField('Καταχώριση')

     

