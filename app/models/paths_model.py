from app.configs.database import db
from dataclasses import dataclass
from app.models.points_paths_table import points_paths


@dataclass
class PathModel(db.Model):
    id: int
    name: str
    description: str
    initial_date: str
    end_date: str
    duration: str
    subscribers: list
    points: list

    __tablename__ = 'paths'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    initial_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
    )

    subscribers = db.relationship('SubscriberModel', cascade='all, delete-orphan')
    points = db.relationship('PointModel', secondary=points_paths, backref='paths_list')

