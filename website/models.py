from . import db
from datetime import datetime
from flask_login import  UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    surname = db.Column(db.String(100), index=True, nullable=False)
    addr = db.Column(db.String(200), index=True, nullable=False)
    numb = db.Column(db.String(10), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, unique=True, nullable=False)
	# password should never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long, depending on your hashing algorithm
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    category = db.Column(db.String(200))
    image = db.Column(db.String(400))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(5), nullable=False)
    etime = db.Column(db.String(5), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(100))
    price = db.Column(db.String(100))
    quantity = db.Column(db.String(100))
    # ... Create the Comments db.relationship
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Assuming the user who created the event

    creator = db.relationship('User', backref='events')  # Relationship to User
    # bookings = db.relationship('Booking', backref='event_reference', lazy=True, cascade="all, delete-orphan")
	
    def cancel_event(self):  # New method for canceling an event
        self.is_canceled = True
        db.session.commit()

    def update_details(self, name=None, description=None, date=None):  # New method for updating event details
        if name:
            self.name = name
        if description:
            self.description = description
        if date:
            self.date = date
        db.session.commit()
	
    def __repr__(self):
        return f"Name: {self.name}"

class Booking(db.Model):
    __tablename__ = 'bookings'  # Name of the database table

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    boname = db.Column(db.String(100), nullable=False)  # User's name
    boemail = db.Column(db.String(100), nullable=False)  # Email
    phone = db.Column(db.String(10), nullable=False)  # User's phone number
    billing_address = db.Column(db.String(250), nullable=False)  # Billing address
    payment_method = db.Column(db.String(10), nullable=False)  # Payment method (e.g., 'visa', 'credit')
    card_number = db.Column(db.String(16), nullable=False)  # Card number
    expiry_date = db.Column(db.String(5), nullable=False)  # Expiry date in MM/YY format
    cvv = db.Column(db.String(3), nullable=False)  # CVV
    number_of_tickets = db.Column(db.Integer, nullable=False) # tickets

    events = db.relationship('Event', backref='bookings')
    users = db.relationship('User', backref='bookings')

    def __repr__(self):
        return f"Booking: {self.id}: {self.name}, {self.phone}>"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"