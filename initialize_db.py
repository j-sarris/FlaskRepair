from datetime import datetime
from flaskrepair import db, app
from flaskrepair.models import User, Repair, HardwareOption, Client


app.app_context().push()

# Drop all tables and recreate them
db.drop_all()
db.create_all()

# Add test data
# Creating test users
user1 = User(username='jdi', first_name='Ιωάννης', last_name='Δημητριάδης', phone=1234567890, email='jdi@oersted.dtu.dk', admin=False)
user1.set_password('1234')

user2 = User(username='yannis', first_name='Γιάννης', last_name='Σαρρής', phone=3975, email='jsa@dtu.dk', admin=True)
user2.set_password('1234')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

# Creating test hardware options
hardware1 = HardwareOption(name='Υπολογιστής')
hardware2 = HardwareOption(name='Οθόνη')
hardware3 = HardwareOption(name='Εκτυπωτής')
hardware4 = HardwareOption(name='Φαξ')
hardware5 = HardwareOption(name='Πολυμηχάνημα')
hardware6 = HardwareOption(name='Scanner')

db.session.add(hardware1)
db.session.add(hardware2)
db.session.add(hardware3)
db.session.add(hardware4)
db.session.add(hardware5)
db.session.add(hardware6)
db.session.commit()

# Creating test clients
client1 = Client(first_name='Θεοδόσιος', last_name='Δημητρίου', telno='3746326521', code='002')
client2 = Client(first_name='Ιωάννης', last_name='Τζαβέλας', telno='123456', code='002')
client3 = Client(first_name='Ευάγγελος', last_name='Ζαμπέτας', telno='2658', code='004')
client4 = Client(first_name='Γεωργία', last_name='Χρυσικού', telno='7856', code='003')

db.session.add(client1)
db.session.add(client2)
db.session.add(client3)
db.session.add(client4)
db.session.commit()

# Creating test repairs
repair1 = Repair(
    user_name=user1.username,
    user_id=user1.id,
    tel_no=1234567890,
    client_id=client1.id,
    hardware_id=hardware3.id,
    serial='SN1234567890',
    guarantee=24,
    duration=3,
    hd=True,
    ram=False,
    graphcard=False,
    power=True,
    error_description='Δεν ανάβει',
    date_posted=datetime.now()
)

repair2 = Repair(
    user_name=user2.username,
    user_id=user2.id,
    tel_no=9876543210,
    client_id=client4.id,
    hardware_id=hardware2.id,
    serial='SN0987654321',
    guarantee=12,
    duration=7,
    hd=False,
    ram=True,
    graphcard=True,
    power=False,
    error_description='Υπερθερμαίνεται',
    date_posted=datetime.now()
)

db.session.add(repair1)
db.session.add(repair2)
db.session.commit()

print("Database initialized and test data added successfully!")
