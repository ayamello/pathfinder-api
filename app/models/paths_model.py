from app.configs.database import db
from sqlalchemy.orm import validates
from dataclasses import dataclass
from app.exceptions.base_exceptions import EmptyStringError, MissingKeyError, NotIntegerError, NotStringError, PathOwnerError, WrongKeysError
from app.models.points_paths_table import points_paths
from datetime import datetime, timezone

@dataclass
class PathModel(db.Model):
	id: int
	name: str
	description: str
	initial_date: str
	end_date: str
	duration: str
	created_at: str
	updated_at: str
	subscribers: list
	points: list

	__tablename__ = 'paths'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	initial_date = db.Column(db.DateTime(timezone=True))
	end_date = db.Column(db.DateTime(timezone=True))
	duration = db.Column(db.String(255))
	created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	admin_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False,
	)

	subscribers = db.relationship('SubscriberModel', cascade='all, delete-orphan')
	points = db.relationship('PointModel', secondary=points_paths, backref='paths_list')

	@staticmethod
	def validate(**kwargs):
		valid_keys = ['name', 'description', 'initial_date', 'end_date', 'duration', 'admin_id', 'subscribers', 'points']
		required_keys = ['name', 'description', 'admin_id']
		received_keys = [key for key in kwargs.keys()]

		for key in received_keys:
			if not key in valid_keys:
				raise WrongKeysError(valid_keys, received_keys)
		
		for key in required_keys:
			if not key in received_keys:
				raise MissingKeyError(required_keys, key)
		
		for key in received_keys:
			if key == 'admin_id':
				if not type(kwargs[key]) == int:
					raise NotIntegerError('key: admin_id must be an integer!')
			else:
				if not type(kwargs[key]) == str:
					raise NotStringError(f'key: {key} must be string!')
		
		
		kwargs['name'] = kwargs['name'].title()

		return kwargs
	
	@validates('name', 'description', 'admin_id')
	def validate_not_null(self, key, value):
		if value == '':
			raise EmptyStringError(f'{key} must not be an empty string!')

		return value
	
	@staticmethod
	def validate_update(**kwargs):
		valid_keys = ['name', 'description', 'initial_date', 'end_date', 'duration', 'admin_id', 'subscribers', 'points']
		received_keys = [key for key in kwargs.keys()]

		for key in received_keys:
			if not key in valid_keys:
				raise WrongKeysError(valid_keys, received_keys)
		
		for key in received_keys:
			if key == 'admin_id':
				if not type(kwargs[key]) == int:
					raise NotIntegerError('key: admin_id must be an integer!')
			else:
				if not type(kwargs[key]) == str:
					raise NotStringError(f'key: {key} must be string!')

		return kwargs
	
	@staticmethod
	def validate_owner(admin_id: int, path_id: int):
		path = PathModel.query.get(path_id)
		print(path)
		if not path.admin_id == admin_id:
			raise PathOwnerError('user cannot update or delete a path that does not belong to them.')

		return admin_id, path_id
