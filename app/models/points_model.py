from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.base_exceptions import NotIntegerError, NotStringError, WrongKeysError
from datetime import datetime, timezone


@dataclass
class PointModel(db.Model):
	id: int
	name: str
	description: str
	initial_date: str
	end_date: str
	duration: str
	created_at: str
	updated_at: str
	activities: list

	__tablename__ = 'points'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	initial_date = db.Column(db.DateTime(timezone=True))
	end_date = db.Column(db.DateTime(timezone=True))
	duration = db.Column(db.String(255))
	created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	address_id = db.Column(
	  db.Integer,
	  db.ForeignKey('addresses.id'),
	  nullable=False,
	)

	activities = db.relationship('ActivityModel', backref='point', cascade='all, delete-orphan')

	@staticmethod
	def validate(**kwargs):
		required_keys = ['name', 'description', 'initial_date', 'end_date', 'duration', 'address_id']
		received_keys = [key for key in kwargs.keys()]

		for key in required_keys:
			if not key in received_keys:
				raise WrongKeysError(required_keys, received_keys)
		
		for key in received_keys:
			if key == 'address_id':
				if not type(kwargs[key]) == int:
					raise NotIntegerError(f'key: {key} must be an integer!')
			else:
				if not type(kwargs[key]) == str:
					raise NotStringError(f'key: {key} must be string!')
		
		return kwargs

	@staticmethod
	def validate_update(**kwargs):
		valid_keys = ['name', 'description', 'initial_date', 'end_date', 'duration', 'address_id']
		received_keys = [key for key in kwargs.keys()]

		for key in received_keys:
			if not key in valid_keys:
				raise WrongKeysError(valid_keys, received_keys)
		
		for key in received_keys:
			if key == 'duration' or key == 'address_id':
				if not type(kwargs[key]) == int:
					raise NotIntegerError(f'key: {key} must be an integer!')
			else:
				if not type(kwargs[key]) == str:
					raise NotStringError(f'key: {key} must be string!')

		return kwargs
