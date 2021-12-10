from app.configs.database import db
from dataclasses import dataclass


@dataclass
class SubscriberModel(db.Model):
    id: int
    user_id: int
    path_id: int
    users: list

    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
    )
    path_id = db.Column(
      db.Integer,
      db.ForeignKey('paths.id'),
      nullable=False,
    )

    users = db.relationship('UserModel')


