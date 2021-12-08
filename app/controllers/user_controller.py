from os import access
from flask import request, current_app, jsonify
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token
import sqlalchemy
import psycopg2

def create():
    data = request.get_json()

    password_to_hash = data.pop("password")

    try:
        new_user = UserModel(**data)

        new_user.password = password_to_hash

        current_app.db.session.add(new_user)
        current_app.db.session.commit()

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {"message": "There are fields missing."}, 400

        return {"message": "This user already exists."}, 409

    return jsonify(new_user)

def login():
    data = request.get_json()

    found_user: UserModel = UserModel.query.filter_by(email=data["email"]).first()

    if not found_user:
        return {"message": "User not found"}, 404

    if found_user.verify_password(data["password"]):
        access_token = create_access_token(identity=found_user)
        return {"token": access_token}, 200
    else:
        return {"message": "Unauthorized"}, 401
