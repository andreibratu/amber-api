from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db

user_interest_association_table = Table(
    'user_interest_association',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('interest_id', Integer, ForeignKey('interests.id')))

user_event_association_table = Table(
    'user_event_association',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('event_id', Integer, ForeignKey('events.id')))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    given_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(200))
    first_time = db.Column(db.Boolean, default=True)

    interests = relationship(
        'Interest',
        secondary=user_interest_association_table,
        back_populates='users')

    events = relationship(
        'Event',
        secondary=user_event_association_table,
        back_populates='users')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User: ' + self.email

    def __init__(self, first_name, given_name, age, bio, email, password):
        self.first_name = first_name
        self.given_name = given_name
        self.age = age
        self.bio = bio
        self.email = email
        self.password = generate_password_hash(password)


class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(30), index=True)
    category = db.Column(db.String(40))

    users = relationship(
        "User",
        secondary=user_interest_association_table,
        back_populates='interests')

    def __repr__(self):
        return 'Interest: ' + self.category + ' ' + self.interest

    def __init__(self, label, category):
        self.label = label
        self.category = category


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(256))

    busytime = relationship('BusyTime', uselist=False)
    place = relationship('Place', uselist=False)

    users = relationship(
        'User',
        secondary=user_event_association_table,
        back_populates='events')

    def __repr__(self):
        return 'Event: ' + self.title

    def __init__(self, title, description, busytime, place):
        self.title = title
        self.description = description
        self.place = place
        self.busytime = busytime


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    thumbnail = db.Column(db.String(300))
    type = db.Column(db.String(30))
    event_id = db.Column(Integer, ForeignKey('events.id'))

    def __init__(self, name, address, lat, lng, thumbnail, type):
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng
        self.thumbnail = thumbnail
        self.type = type


class BusyTime(db.Model):
    __tablename__ = 'busytimes'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.BigInteger)
    end = db.Column(db.BigInteger)
    event_id = db.Column(Integer, ForeignKey('events.id'))

    def __init__(self, start, end):
        self.start = start
        self.end = end
