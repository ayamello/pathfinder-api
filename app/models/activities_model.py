from sqlalchemy.orm import backref
from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.base_exceptions import NotStringError, WrongKeysError


@dataclass
class ActivityModel(db.Model):
    name: str 
    description: str
    reviews: list

    __tablename__ = 'activities'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    point_id = db.Column(
        db.Integer,
        db.ForeignKey('points.id'),
        nullable=False,
    )
    reviews = db.relationship('ReviewModel', backref=backref('activity', uselist=False))


    @staticmethod
    def validate(**kwargs):
        valid_keys = ['name', 'description', 'point_id']
        received_keys = [key for key in kwargs.keys()]

        if not valid_keys == received_keys:
            raise WrongKeysError(valid_keys, received_keys)
        
        if not type(kwargs['name']) == str:
            raise NotStringError('name must be string!')

        kwargs['name']=kwargs['name'].title()

        return kwargs
