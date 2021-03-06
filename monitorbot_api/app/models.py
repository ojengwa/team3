from flask import current_app, request, url_for, jsonify
from datetime import datetime
from . import db
import json

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='noload')

    def to_json(self):
        json_rep = {
            'id': self.id,
            'name': self.name
        }
        return json.dumps(json_rep)

    def __repr__(self):
        return '<Role %r>' % self.name


class Frequency(db.Model):
    
    __tablename__ = 'frequencies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    value = db.Column(db.BigInteger, unique=True)

    def to_json(self):
        json_rep = {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }
        return json.dumps(json_rep)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    watchs = db.relationship('Watch', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
   
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_rep = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
        return json.dumps(json_rep)

    def __repr__(self):
        return '<User %r>' % self.username


class Watch(db.Model):
    __tablename__ = 'watchs'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    email = db.Column(db.String(64))
    frequency = db.Column(db.BigInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean)
    
    checks = db.relationship('Check', backref='watch', lazy='immediate')

    def to_json(self):
        json_rep = {
            'id': self.id,
            'url': self.url,
            'frequency': self.frequency,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            "is_active": self.is_active
        }
        return json.dumps(json_rep)

    def __repr__(self):
        return '<Watch %r>' % self.url


class Check(db.Model):
    __tablename__ = 'checks'
    id = db.Column(db.Integer, primary_key=True)
    watch_id = db.Column(db.Integer, db.ForeignKey('watchs.id'))
    report = db.Column(db.String(64))
    timestamp = db.Column(db.BigInteger)
    mail_sent = db.Column(db.Boolean)

    def to_json(self):
        json_rep = {
            'id': self.id,
            'watch_id': self.watch_id,
            'report': self.report,
            'timestamp': self.timestamp,
            'mail_sent': self.mail_sent
        }
        return json.dumps(json_rep)

    def __repr__(self):
        return '<Check %r>' % datetime.fromtimestamp(self.timestamp)




