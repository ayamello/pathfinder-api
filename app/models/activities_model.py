from app.configs.database import db
from dataclasses import dataclass


@dataclass
class ActivityModel(db.Model):
    name: str
    description: str

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False, unique=True)
    point_id = db.Column(
        db.Integer,
        db.ForeignKey('points.id'),
        nullable=False,
    )

    @staticmethod
    def validate(**kwargs):
        name = kwargs['name']

        

        return None