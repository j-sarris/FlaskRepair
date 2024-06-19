from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, RadioField, SubmitField, TelField, BooleanField, SelectField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp
from flask_login import current_user
from flaskrepair.models import User, HardwareOption, Client
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RegistrationForm(FlaskForm):
    username = StringField('Όνομα χρήστη', validators=[DataRequired(message="Το όνομα του χρήστη δεν μπορεί να είναι κενό"), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email('Συμπληρώστε σωστό email της μορφής name@server')])
    # name = StringField('Όνομα χρήστη', validators=[DataRequired(message="Το όνομα του χρήστη δεν μπορεί να είναι κενό"), Length(min=2, max=20)])
    # surname = StringField('Όνομα χρήστη', validators=[DataRequired(message="Το όνομα του χρήστη δεν μπορεί να είναι κενό"), Length(min=2, max=20)])
    # tel_no = TelField('Τηλέφωνο', validators=[Optional(), Length(max=15), Regexp(r'^\+?\d{0,15}$', message="Λάθος μορφή αριθμού τηλεφώνου")])
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
    username = StringField('Όνομα χρήστη', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Κωδικός', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Σύνδεση')

class RepairForm(FlaskForm):
    # username  = StringField('Σειριακός Αριθμός', validators=[DataRequired()])
    tel_no = TelField('Τηλέφωνο', validators=[Optional(), Length(max=15), Regexp(r'^\+?\d{0,15}$', message="Λάθος μορφή αριθμού τηλεφώνου")])
    client = SelectField('Ονοματεπώνυμο υπαλλήλου', choices=[], validators=[DataRequired(message="Το όνομα του υπαλλήλου δεν μπορεί να είναι κενό")])
    hardware = SelectField('Είδος υλικού', choices=[], validators=[DataRequired(message="Το είδος του υλικού δεν μπορεί να είναι κενό")])
    serial = StringField('Σειριακός Αριθμός', validators=[Optional()])
    guarantee = SelectField('Διάρκεια εγγύησης σε μήνες', choices=[], validators=[Optional()])
    duration = RadioField('Διάρκεια επισκευής σε εργάσιμες μέρες', choices=[('1-3', '1 έως 3 μέρες'), ('4-6', '4 έως 6 μέρες'), 
                                                                            ('7-10', '7 έως 10 μέρες'), ('10+', 'Πάνω από 10 μέρες')], validators=[Optional()])
    hd = BooleanField('Σκληρός Δίσκος')  # Hard Drive
    ram = BooleanField('Μνήμες')         # RAM
    graphcard = BooleanField('Κάρτα Γραφικών')  # Graphics Card
    power = BooleanField('Τροφοδοτικό')  # Power Supply
    error_description = TextAreaField('Περιγραφή βλάβης', validators=[Optional()])
    submit = SubmitField('Καταχώριση')

    def __init__(self, *args, **kwargs):
        super(RepairForm, self).__init__(*args, **kwargs)
        self.hardware.choices = [('', 'Επιλέξτε υλικό...')] + [ (h.id, h.name) for h in HardwareOption.query.all()]
        self.client.choices = [('', 'Επιλέξτε ονοματεπώνυμο...')] + [ (h.id, h.last_name +' '+  h.first_name ) for h in Client.query.order_by('last_name').all()]
        self.guarantee.choices = [('', '0')] + [(h, str(h)) for h in range(1, 61)]


     

