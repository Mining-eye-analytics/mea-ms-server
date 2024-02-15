# application/models.py
from application import db
from datetime import datetime
from enum import IntEnum
from sqlalchemy.sql import func

class Role(IntEnum):
    SUPER_ADMIN = 3
    ADMIN = 2
    USER = 1

class Realtime_images(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cctv_id = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    avg_panjang_bbox_hd = db.Column(db.Float, nullable=True, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, onupdate=func.now())
    path = db.Column(db.String(100), nullable=True, default='assets/outputFolder/cctvOutput/')
    realtime_deviations = db.relationship('Realtime_deviations', backref='realtime_images', lazy='dynamic')
    crossing_counting = db.relationship('Crossing_counting', backref='realtime_images', lazy='dynamic')

    def __repr__(self):
        return '<Image {}>'.format(self.image)
    
    def to_json(self):
        return {
            'cctv_id': self.cctv_id,
            'image': self.image,
            'avg_panjang_bbox_hd': self.avg_panjang_bbox_hd,
            'path': self.path,
        }

    def to_json_all(self):
        return {
            'id': self.id,
            'cctv_id': self.cctv_id,
            'image': self.image,
            'avg_panjang_bbox_hd': self.avg_panjang_bbox_hd,
            'path': self.path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    
class Realtime_deviations(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    parent_id = db.Column(db.Integer,  db.ForeignKey(id), nullable=True)
    realtime_images_id = db.Column(db.Integer, db.ForeignKey(Realtime_images.id), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    type_validation = db.Column(db.Enum('not_yet', 'true', 'false'), nullable=False, default='not_yet')
    type_object = db.Column(db.String(100), nullable=False, default='person')
    violate_count = db.Column(db.Integer, nullable=True, default=0)
    comment = db.Column(db.String(250), nullable=True, default=None)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return '<Deviation {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'realtime_images_id': self.realtime_images_id,
            'user_id': self.user_id,
            'type_validation': self.type_validation,
            'type_object': self.type_object,
            'violate_count': self.violate_count,
            'comment': self.comment,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Crossing_counting(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    realtime_images_id = db.Column(db.Integer, db.ForeignKey(Realtime_images.id), nullable=False)
    type_object = db.Column(db.String(100), nullable=False, default='bus')
    count = db.Column(db.Integer, nullable=True, default=0)
    track_id = db.Column(db.Integer, nullable=True, default=0)
    direction = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return '<Deviation {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'realtime_images_id': self.realtime_images_id,
            'type_object': self.type_object,
            'count': self.count,
            'track_id': self.track_id,
            'direction': self.direction,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }