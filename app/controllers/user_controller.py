from flask import request, current_app, jsonify
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token
import sqlalchemy
import psycopg2

def create_user():
    data = request.get_json()

    password_to_hash = data.pop("password")

    try:
        new_user = UserModel(**data)

        new_user.password = password_to_hash

        current_app.db.session.add(new_user)
        current_app.db.session.commit()

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.NotNullViolation:
            return {'error': 'There are fields missing.'}, 400

        return {'error': 'This user already exists.'}, 409

    except TypeError as e:
        return {'error': 'There are extra fields.'}, 400


    return jsonify(new_user)

def login():
    data = request.get_json()

    found_user: UserModel = UserModel.query.filter_by(email=data['email']).first()

    if not found_user:
        return {'error': 'User not found'}, 404

    if found_user.verify_password(data['password']):
        access_token = create_access_token(identity=found_user)
        return {
            'username': found_user.username,
            'token': access_token
            }, 200
    else:
        return {'error': 'Unauthorized'}, 401

def get_all_users():

    users = UserModel.query.all()

    return jsonify(users), 200

def get_by_username(id):

    user = UserModel.query.get(id)

    if not user:
        return {'error': 'User not found.'}, 404

    return jsonify(user), 200


    



