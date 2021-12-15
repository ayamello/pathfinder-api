from flask import request, jsonify
from app.controllers.__init__ import create, delete, get_all, update
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from app.exceptions.base_exceptions import DateError, EmptyStringError, MissingKeyError, NotIntegerError, NotStringError, WrongKeysError, NotFoundDataError
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_path():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        data['admin_id'] = current_user['id']

        validated_data = PathModel.validate(**data)
        
        path = create(validated_data, PathModel, '')
        
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
        return {'error': 'Request must contain only, name, description, initial_date, end_date, duration and user_id'}, 400

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
def delete_path(id: int):
    try:
        path = delete(PathModel, id)

    except UnmappedInstanceError:
        return {'error': 'Path ID Not Found'}, 404

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    return path

@jwt_required()
def update_path(id: int):
    try:
        data = request.get_json()

        PathModel.validate_update(**data)

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

@jwt_required()
def get_all_paths():
    paths = get_all(PathModel)

    serializer = [{
        'id': path.id,
        'name': path.name,
        'description': path.description,
        'initial_date': path.initial_date.strftime("%d/%m/%Y"),
        'end_date': path.end_date.strftime("%d/%m/%Y"),
        'duration': path.duration,
        'subscribers': [{'username': user.users.username} for user in path.subscribers]
    } for path in paths]

    return jsonify(serializer), 200

@jwt_required()
def get_all_by_page(pg: int):
    record_query = PathModel.query.paginate(page=pg, error_out=False, max_per_page=15)

    serializer = [{
        'id': path.id,
        'name': path.name,
        'description': path.description,
        'initial_date': path.initial_date.strftime("%d/%m/%Y"),
        'end_date': path.end_date.strftime("%d/%m/%Y"),
        'duration': path.duration,
        'subscribers': [{'username': user.users.username} for user in path.subscribers]
    } for path in record_query.items]

    next_page = f'https://pathfinder-q3.herokuapp.com/paths/page/{record_query.next_num}'
    prev_page = f'https://pathfinder-q3.herokuapp.com/paths/page/{record_query.prev_num}'

    if not record_query.next_num:
        next_page = "Empty page"
    
    if not record_query.prev_num:
        prev_page = "Empty page"

    result = dict( total_items=record_query.total, 
                   current_page=record_query.page,
                   total_pages=record_query.pages,
                   per_page=record_query.per_page,
                   next_page=next_page,
                   prev_page=prev_page,
                   data=serializer)

    return jsonify(result), 200

@jwt_required()
def get_paths_by_user_id(id: int):
    paths_by_user = PathModel.query.filter_by(user_id=id).all()

    if not paths_by_user:
        return jsonify({'error': 'There are no paths in this user ID'}), 404

    return jsonify(paths_by_user), 200
