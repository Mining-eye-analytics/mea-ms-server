# application/models.py
from application import db
from datetime import datetime
from enum import IntEnum
from sqlalchemy.sql import func

class Role(IntEnum):
    SUPER_ADMIN = 3
    ADMIN = 2
    USER = 1

class Cctv(db.Model):
    link_rtsp = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    location = db.Column(db.String(255), unique=False, nullable=True)
    ip = db.Column(db.String(255), unique=False, nullable=False)
    type_analytics = db.Column(db.String(255), unique=False, nullable=False, default="StreamCctv")
    username = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __repr__(self):
        return '<cctv %r>' % (self.username)

    def to_json(self):
        return {
            'id': self.id,
            'link_rtsp': self.link_rtsp,
            'name': self.name,
            'location': self.location,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'type_analytics' : self.type_analytics,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }