from app.configs.database import db
from dataclasses import dataclass


@dataclass
class AdressModel(db.Model):
    id: int
    street: str
    number: int
    city: str
    state: str
    country: str
    postal_code: str
    coordenadas: str

    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255))
    number = db.Column(db.Integer)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    coordenadas = db.Column(db.String(255))
