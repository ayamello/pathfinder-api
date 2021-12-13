from app.configs.database import db
from dataclasses import dataclass


@dataclass
class PointModel(db.Model):
    id: int
    name: str
    description: str
    initial_date: str
    end_date: str
    duration: str
    activities: list

    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    initial_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    duration = db.Column(db.Integer)
    address_id = db.Column(
      db.Integer,
      db.ForeignKey('addresses.id'),
      nullable=False,
    )

    activities = db.relationship('ActivityModel', backref='point', cascade='all, delete-orphan')
