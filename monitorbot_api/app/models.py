from . import db
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='noload')

    def __repr__(self):
        return '<Role %r>' % self.name



class Frequency(db.Model):
    __tablename__ = 'frequencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    value = db.Column(db.BigInteger, unique=True)

    watchs = db.relationship('Watch', backref='frequency', lazy='noload')

    def __repr__(self):
        return '<Role %r>' % self.name



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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

    def __repr__(self):
        return '<User %r>' % self.username


class Watch(db.Model):
    __tablename__ = 'watchs'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    frequency_id = db.Column(db.Integer, db.ForeignKey('frequencies.id'))
    email = db.Column(db.String(64))
    client = db.Column(db.String(64))
    timestamp = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean)
    
    checks = db.relationship('Check', backref='watch', lazy='immediate')

    def __repr__(self):
        return '<Watch %r>' % self.url


class Check(db.Model):
    __tablename__ = 'checks'
    id = db.Column(db.Integer, primary_key=True)
    watch_id = db.Column(db.Integer, db.ForeignKey('watchs.id'))
    report = db.Column(db.String(64))
    timestamp = db.Column(db.BigInteger)
    mail_sent = db.Column(db.Boolean)

    def __repr__(self):
        return '<Check %r>' % datetime.fromtimestamp(self.timestamp)


# class Client(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     password = db.Column(db.String(64), index=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
# 
#     def __repr__(self):
#         return '<User %r>' % self.username


