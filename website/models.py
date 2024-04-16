from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TIME


class RecyclingPoint(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(500))
    city = db.Column(db.String(150))
    material_id = (db.Integer, db.ForeignKey('material.id'))
    works_from = db.Column(db.TIME())
    works_to = db.Column(db.TIME())
    additional_info = db.Column(db.String(3000)) # ??


class ScoreTable(db.Model):
    material_id = (db.Integer, db.ForeignKey('material.id')) # primary key ?
    user_id = (db.Integer, db.ForeignKey('user.id')) # primary key ?
    score = db.Column(db.Integer)
    reward = db.Column(db.String(250))


class Material(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    sorting_info = db.Column(db.String(3000)) # ??


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name =  db.Column(db.String(150))
    

