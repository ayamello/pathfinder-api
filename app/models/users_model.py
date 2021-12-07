from app.configs.database import db
from dataclasses import dataclass
from app.models.users_paths_table import users_paths


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    birthdate: str
    paths_list: list

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    birthdate = db.Column(db.DateTime, nullable=False)
    password_hash = db.Column(db.String)

    paths_list = db.relationship('PathModel', secondary=users_paths, backref='users_list')

