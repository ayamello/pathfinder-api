from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime, timezone
from app.exceptions.base_exceptions import NotFoundDataError, NotStringError, WrongKeysError
from app.models.activities_model import ActivityModel


@dataclass
class ReviewModel(db.Model):
    username: str
    review: str
    created_at: str
    updated_at: str
   
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    review = db.Column(db.String, nullable=False)
    activity_id = db.Column(
      db.Integer,
      db.ForeignKey('activities.id'),
      nullable=False,
    )
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))

    @staticmethod
    def validate(**kwargs):
        valid_keys = ['review', 'activity_id', 'username']
        received_keys = [key for key in kwargs.keys()]

        
        if not valid_keys == received_keys:
            raise WrongKeysError(valid_keys, received_keys)
        
        if not type(kwargs['username']) == str:
            raise NotStringError('name must be string!')
        
        current_activity = ActivityModel.query.get(kwargs['activity_id'])

        if not current_activity:
            raise NotFoundDataError('Activity ID not found!')

        return kwargs
