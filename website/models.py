from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TIME


class Material(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    sorting_info = db.Column(db.String(3000)) # ??
    recycling_point_id = db.Column(db.Integer, db.ForeignKey('recycling_point.id'))


class RecyclingPoint(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(500)) # coordinates
    city = db.Column(db.String(150))
    materials = db.relationship('Material')
    works_from = db.Column(db.TIME())
    works_to = db.Column(db.TIME())
    additional_info = db.Column(db.String(3000)) # ??


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name =  db.Column(db.String(150))
    entries = db.relationship('Entry')
    is_admin = db.Column(db.Boolean)


class Entry (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # хто здав
    material_id = db.Column(db.Integer, db.ForeignKey('material.id')) # що здав
    recycling_point_id = db.Column(db.Integer, db.ForeignKey('recycling_point.id')) # де здав
    points_earned = db.Column(db.Integer)
    reward = db.Column(db.String(250))