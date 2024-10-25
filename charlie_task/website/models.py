from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    surname = db.Column(db.String(100), index=True, unique=True, nullable=False)
    addr = db.Column(db.String(200), index=True, unique=True, nullable=False)
    numb = db.Column(db.String(10), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
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
    quantity = db.Column(db.String(100))
    is_canceled = db.Column(db.Boolean, default=False)  # New field for event cancellation
    comments = db.relationship('Comment', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='events')

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

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
