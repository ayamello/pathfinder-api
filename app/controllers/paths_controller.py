from datetime import datetime, timezone
from flask import request, jsonify
from app.controllers import create, delete, get_all, update
from app.models.paths_model import PathModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import InvalidRequestError, DataError
from app.exceptions.base_exceptions import DateError, EmptyStringError, MissingKeyError, NotIntegerError, NotStringError, PathOwnerError, WrongKeysError, NotFoundDataError
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_path():
    try:
        data = request.get_json()

        current_user = get_jwt_identity()

        data['admin_id'] = current_user['id']

        validated_data = PathModel.validate(**data)
        
        path = create(validated_data, PathModel, '')

        initial_date = ''
        end_date = ''

        if not path.initial_date == None and not path.end_date == None: 
            diff = path.end_date - path.initial_date

            if diff.days < 0:
                raise DateError('The final date must be after initial date!')
        
            initial_date = path.initial_date.strftime("%d/%m/%Y")
            end_date = path.end_date.strftime("%d/%m/%Y")

        output = {
            'id': path.id,
            'name': path.name,
            'description': path.description,
            'initial_date': initial_date,
            'end_date': end_date,
            'duration': path.duration,
            'created_at': path.created_at,
            'updated_at': path.updated_at,
            'admin_user': {
                'name': path.user.name,
                'email': path.user.email
            },
            'points': path.points,
            'subscribers': path.subscribers
        }

        return jsonify(output), 201

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except (NotStringError, EmptyStringError, DateError) as err:
        return jsonify({'error': str(err)}), 400

    except MissingKeyError as err:
        return jsonify({'error': err.message}), 400
    
    except DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400


@jwt_required()
def delete_path(id: int):
    try:
        current_user = get_jwt_identity()

        admin_id = current_user['id']

        PathModel.validate_owner(admin_id, id)

        path = delete(PathModel, id)

        return path

    except UnmappedInstanceError:
        return {'error': 'Path ID Not Found'}, 404

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404

    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400
   

@jwt_required()
def update_path(id: int):
    try:
        data = request.get_json()

        current_user = get_jwt_identity()

        admin_id = current_user['id']

        data['updated_at'] = datetime.now(timezone.utc)

        PathModel.validate_owner(admin_id, id)

        PathModel.validate_update(**data)

        path = update(PathModel, data, id)

        return path

    except (InvalidRequestError, EmptyStringError, PathOwnerError ) as err:
        return jsonify({'error': str(err)}), 400

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404


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
        "created_at": path.created_at,
        "updated_at": path.updated_at,
        "admin_user": {
                "name": path.user.name,
                "email": path.user.email
        },
        'points': [point for point in path.points],
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
        "created_at": path.created_at,
        "updated_at": path.updated_at,
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
def get_paths_by_user_id(user_id: int):
    try:
        paths_by_user = PathModel.query.filter_by(admin_id=user_id).all()

        if not paths_by_user:
            raise NotFoundDataError('User ID not found!')
            
        return jsonify(paths_by_user), 200

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404



@jwt_required()
def get_path_by_id(id: int):
    try:
        paths_by_id = PathModel.query.filter_by(id=id).first()

        if not paths_by_id:
            raise NotFoundDataError('Path ID not found!')
            
        return jsonify(paths_by_id), 200

    except NotFoundDataError as err:
        return jsonify({'error': str(err)}), 404
