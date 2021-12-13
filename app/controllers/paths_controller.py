from flask import request, jsonify
from app.controllers.base_controller import create, delete, get_all, update
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from app.exceptions.path_exceptions import DateError, EmptyStringError, MissingKeyError, NotIntegerError, NotStringError, WrongKeysError, NotFoundDataError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ipdb import set_trace
#TODO: Paginação das rotas get

@jwt_required()
def create_path():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']

        validated_data = PathModel.validate(**data)
        
        path = create(data, PathModel, '')
        
        diff = path.end_date - path.initial_date

        if diff.days < 0:
            raise DateError('The final date must be after initial date!')
        
        elif diff.days == 0:
            raise DateError('The dates must not be in the same day!')
        
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

    except EmptyStringError as err:
        return jsonify({'error': str(err)}), 400
    
    except MissingKeyError as err:
        return jsonify({'error': err.message}), 400

    except DateError as err:
        return jsonify({'error': str(err)}), 400
      


@jwt_required()
def delete_path(id):
    try:
        path = delete(PathModel, id)

    except UnmappedInstanceError:
        return {'error': 'Path ID Not Found'}, 404

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404
        
    return "", 200


def update_path(id):
    try:
        data = request.get_json()

        validate_data = PathModel.validate(**data)

        if data['user_id']:
            data.pop('user_id')

        path = update(PathModel, data, id)
        return path

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except InvalidRequestError as err:
        return jsonify({'error': str(err)}), 400
    
    except EmptyStringError as err:
        return jsonify({'error': str(err)}), 400


def get_all_paths():
    paths = get_all(PathModel)

    serializer = [{
        'id': path.id,
        'name': path.name,
        'description': path.description,
        'initial_date': path.initial_date,
        'end_date': path.end_date,
        'duration': path.duration,
        'subscribers': [{'username': user.users.username} for user in path.subscribers]
    } for path in paths]
    
    return jsonify(serializer), 200


def get_paths_by_user_id(id):
    paths_by_user = PathModel.query.filter_by(user_id=id).all()

    if not paths_by_user:
        return jsonify({'error': 'There are no paths in this user ID'}), 404

    return jsonify(paths_by_user), 200
