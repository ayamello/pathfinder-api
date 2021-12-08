from sqlalchemy.orm import backref
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    username: str
    email: str
    birthdate: str
    url_image: str
    paths_list: list

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    birthdate = db.Column(db.DateTime, nullable=False)
    url_image = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)

    paths_list = db.relationship('PathModel', backref=backref('user', uselist=False))

