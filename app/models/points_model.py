from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.base_exceptions import EmptyStringError, NotIntegerError, NotStringError, WrongKeysError
from sqlalchemy.orm import validates

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
	initial_date = db.Column(db.Date)
	end_date = db.Column(db.Date)
	duration = db.Column(db.Integer)
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

		for key in received_keys:
			if key not in required_keys:
				raise WrongKeysError(required_keys, received_keys)
		
		for key in received_keys:
			if key == "duration" or key == "address_id":
				if not type(kwargs[key]) == int:
					raise NotIntegerError(f'key: {key} must be an integer!')
			else:
				if not type(kwargs[key]) == str:
					raise NotStringError(f'key: {key} must be string!')
		
		return kwargs

	@staticmethod
	def validate_update(**kwargs):
		valid_keys = ['name', 'description', 'initial_date', 'end_date', 'duration', 'address_id', 'updated_at', 'created_at']
		received_keys = [key for key in kwargs.keys()]

		for key in received_keys:
			if key not in valid_keys:
				raise WrongKeysError(valid_keys, received_keys)
		
		for key in received_keys:
			if key == "duration" or key == "address_id":
				if not type(kwargs[key]) == int:
					raise NotIntegerError(f'key: {key} must be an integer!')

		return kwargs

	@validates('name', 'description', 'address_id')
	def validate_not_null(self, key, value):
		if value == '':
			raise EmptyStringError(f'{key} must not be an empty string!')

		return value