from app.configs.database import db
from dataclasses import dataclass
from app.models.users_model import UserModel
from app.models.paths_model import PathModel
from app.exceptions.base_exceptions import NotFoundDataError, PathOwnerError, WrongKeysError


@dataclass
class SubscriberModel(db.Model):
    id: int
    user_id: int
    path_id: int
    users: list

    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
      db.Integer,
      db.ForeignKey('users.id'),
      nullable=False,
    )
    path_id = db.Column(
      db.Integer,
      db.ForeignKey('paths.id'),
      nullable=False,
    )

    users = db.relationship('UserModel', backref='subscriptions')

    @staticmethod
    def validate(**kwargs):
      valid_keys = ['user_id', 'path_id']
      received_keys = [keys for keys in kwargs.keys()]
    
      if not received_keys == valid_keys:
        raise WrongKeysError(valid_keys, received_keys)

      current_path = PathModel.query.get(kwargs['path_id'])
      
      if not current_path:
        raise NotFoundDataError('Path ID not found!')

      current_user = UserModel.query.get(kwargs['user_id'])
      user_path = [path.id for path in current_user.paths_list if path.id == kwargs['path_id']]

      if user_path:
        raise PathOwnerError("You can't subscribe to your own path, chose other path!")
      
      return kwargs


