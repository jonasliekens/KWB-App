from hashlib import md5

from flask_login import UserMixin
from flask_security import RoleMixin

from app import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column("firstName", db.String(64))
    last_name = db.Column("lastName", db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    city = db.Column(db.String(30))
    zipcode = db.Column(db.String(4))
    address = db.Column(db.String(100))
    password = db.Column('password', db.String(255))
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, first_name, last_name, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def has_role(self, role):
        return role in (role.name for role in self.roles)

    @property
    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text())
    location = db.Column(db.Text())
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())

    def __repr__(self):
        return '<Event {}>'.format(self.title)
