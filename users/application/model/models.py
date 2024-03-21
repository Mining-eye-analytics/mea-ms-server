# application/models.py
from application import db
from datetime import datetime
from enum import IntEnum
from sqlalchemy.sql import func

class Role(IntEnum):
    SUPER_ADMIN = 3
    ADMIN = 2
    USER = 1


class User(db.Model):
    username = db.Column(db.String(255), unique=True, nullable=False)
    company = db.Column(db.String(255), unique=False, nullable=True)
    full_name = db.Column(db.String(255), unique=False, nullable=True)
    role = db.Column(db.String(255), unique=False, nullable=True, default="user")
    password = db.Column(db.String(255), unique=False, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    login_at = db.Column(db.DateTime)
    logout_at = db.Column(db.DateTime)


    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        return {
            'company': self.company,
            'id': self.id,
            'full_name': self.full_name,
            'role': self.role,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'login_at': self.login_at,
            'logout_at': self.logout_at
        }
    
class LoginRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    login_at = db.Column(db.DateTime)
    logout_at = db.Column(db.DateTime)


    def __repr__(self):
        return '<User %r>' % (self.id)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'login_at': self.login_at,
            'logout_at': self.logout_at
        }