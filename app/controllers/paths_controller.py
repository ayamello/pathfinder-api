from flask import request, jsonify
from app.controllers.base_controller import create, delete, get_all, update
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from app.exceptions.path_exceptions import NotIntegerError, NotStringError, WrongKeysError, NotFoundDataError
from flask_jwt_extended import jwt_required, get_jwt_identity

#TODO: Paginação das rotas get
#TODO: Regra de negócio para o end date

@jwt_required()
def create_path():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']

        path = create(data, PathModel, '')

        result = {
            "id": path.id,
            "name": path.name,
            "description": path.description,
            "initial_date": path.initial_date.strftime("%d/%m/%Y"),
            "end_date": path.end_date.strftime("%d/%m/%Y"),
            "duration": path.duration,
            "user": {
                "name": path.user.name,
                "email": path.user.email
            }
        }
        
        return jsonify(result), 201

    except IntegrityError:
        return {'error': 'Request must contain only, name, description and point_id'}, 400

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400
    
    except NotIntegerError as err:
        return jsonify({'error': str(err)}), 400


@jwt_required()
def delete_path(id):
    try:
        path = delete(PathModel, id)

    except UnmappedInstanceError:
        return {'error': 'Path ID Not Found'}, 404

    return path


def update_path(id):
    try:
        data = request.get_json()
        validate_data = PathModel.validate(**data)

        if data['user_id']:
            data.pop('user_id')

        path = update(PathModel, data, id)
        return path

    except NotFoundDataError as e:
        return jsonify({'error': str(e)}), 404

    except WrongKeysError as e:
        return jsonify({'error': e.message}), 400

    except InvalidRequestError as err:
        return jsonify({'error': str(err)}), 400


def get_all_paths():
    paths = get_all(PathModel)

    ## Ideia de serialização para mostrar apenas usernames na resposta do get:
    serializer = [{
        'id': path.id,
        'name': path.name,
        'description': path.description,
        'initial_date': path.initial_date,
        'end_date': path.end_date,
        'duration': path.duration,
        'subscribers': [{'username': user.users.username} for user in path.subscribers]
    } for path in paths]
    
    return jsonify(paths), 200


def get_paths_by_user_id(id):
    paths_by_user = PathModel.query.filter_by(user_id=id).all()

    return jsonify(paths_by_user), 200
