from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.base_exceptions import NotIntegerError, NotStringError, WrongKeysError

@dataclass
class AddressModel(db.Model):
    id: int
    street: str
    number: int
    city: str
    state: str
    country: str
    postal_code: str
    coordenadas: str

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255))
    number = db.Column(db.Integer)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    coordenadas = db.Column(db.String(255))

    @staticmethod
    def validate(**kwargs):
        required_keys = ['street', 'number', 'city', 'state', 'country', 'postal_code', 'coordenadas']
        received_keys = [key for key in kwargs.keys()]

        for key in required_keys:
            if key not in received_keys:
                raise WrongKeysError(required_keys, received_keys)
            
            if key == "number":
                if not type(kwargs[key]) == int:
                    raise NotIntegerError('key: number must be an integer')
                
            else:
                if not type(kwargs[key]) == str:
                    raise NotStringError(f'key: {key} must be string!')
            
        return kwargs