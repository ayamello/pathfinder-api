from sqlalchemy.orm import backref
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UserModel(db.Model):
    id: int
    name: str
    username: str
    email: str
    birthdate: str
    url_image: str
    paths_list: list

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirm_email = db.Column(db.Boolean, default=False)
    birthdate = db.Column(db.DateTime(timezone=True), nullable=False)
    url_image = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)
    password_hash_confirmation = db.Column(db.String)

    paths_list = db.relationship('PathModel', backref=backref('user', uselist=False))


    @property
    def password(self):
        raise AttributeError('Wrong password.')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)