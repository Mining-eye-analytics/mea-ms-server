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
            'updated_at': self.updated_at
        }