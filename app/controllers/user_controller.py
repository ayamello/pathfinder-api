from flask import request, jsonify
from app.exceptions.base_exceptions import EmptyStringError, MissingKeyError, NotStringError, NotFoundDataError, WrongKeysError, EmailAlreadyExists, UsernameAlreadyExists
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from app.controllers.__init__ import create, delete, get_all, update
import sqlalchemy

def create_user():
    try:
        data = request.get_json()

        UserModel.validate(**data)

        password_to_hash = data.pop('password')

        new_user = create(data, UserModel, password_to_hash)

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except EmptyStringError as err:
        return jsonify({'error': str(err)}), 400

    except UsernameAlreadyExists as err:
        return jsonify({'error': str(err)}), 409

    except EmailAlreadyExists as err:
        return jsonify({'error': str(err)}), 409

    except MissingKeyError as err:
        return jsonify({'error': err.message}), 400

    output = {
        "id": new_user.id,
        "name": new_user.name,
        "username": new_user.username,
        "email": new_user.email,
        "birthdate": new_user.birthdate.strftime("%d/%m/%Y"),
        "url_date": new_user.url_image,
        "paths_lists": new_user.paths_list
    }

    return jsonify(output), 201


def login():
    data = request.get_json()

    found_user: UserModel = UserModel.query.filter_by(email=data['email']).first()

    if not found_user:
        return {'error': 'User not found'}, 404

    if found_user.verify_password(data['password']):
        access_token = create_access_token(identity=found_user)
        return {
            'token': access_token
            }, 200
    else:
        return {'error': 'Unauthorized'}, 401


@jwt_required()
def get_all_users():
    users = get_all(UserModel)

    return jsonify(users), 200


@jwt_required()
def get_by_id(id):
    user = UserModel.query.get(id)

    if not user:
        return {'error': 'User not found.'}, 404

    return jsonify(user), 200
    

@jwt_required()
def update_user(id):
    try:
        data = request.get_json()

        user = update(UserModel, data, id)

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    return user

@jwt_required()
def delete_user(id):
    try:
        user = delete(UserModel, id)
    
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return {'error': 'User not found.'}, 404

    return user
