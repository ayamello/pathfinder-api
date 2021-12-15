from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ReviewModel(db.Model):
    name: str
    review: str
    created_at: str
    updated_at: str
   
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    review = db.Column(db.String, nullable=False)
    activity_id = db.Column(
      db.Integer,
      db.ForeignKey('activities.id'),
      nullable=False,
    )
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
