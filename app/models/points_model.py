from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.base_exceptions import EmptyStringError, NotIntegerError, NotStringError, PathOwnerError, WrongKeysError
from sqlalchemy.orm import validates
from datetime import datetime, timezone
from app.models.users_model import UserModel

@dataclass
class PointModel(db.Model):
	id: int
	name: str
	description: str
	initial_date: str
	end_date: str
	duration: str
	address_id: int
	path_id: int
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
	path_id = db.Column(
        db.Integer,
        db.ForeignKey('paths.id'),
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
	
	@staticmethod
	def validate_user(user_id, point_id):
		current_user = UserModel.query.get(user_id)
		user_paths = [path for path in current_user.paths_list]
		
		for path in user_paths:
			for point in path.points:
				if point.id == point_id:
					return user_id, point_id
				
		raise PathOwnerError('you need to be the path owner to update or delete a point!')
