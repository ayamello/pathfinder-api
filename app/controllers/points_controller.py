from flask import request, current_app, jsonify
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import create, delete, update
from app.models.paths_model import PathModel
from app.models.points_model import PointModel
from app.models.addresses_model import AddressModel
from app.exceptions.base_exceptions import EmptyStringError, NotIntegerError, NotStringError, PathOwnerError, WrongKeysError, NotFoundDataError
from sqlalchemy.exc import DataError
from pdb import set_trace


@jwt_required()
def create_point():
    try:
        data = request.get_json()

        path_id = data.pop('path_id')

        current_user = get_jwt_identity()

        admin_id = current_user['id']

        PathModel.validate_owner(admin_id, path_id)

        keys_data = list(data.keys())

        data_address_keys = ['street', 'number', 'city', 'state', 'country', 'postal_code', 'coordenadas']
       
        initial_data_address = []

        for key in keys_data:
            if key in data_address_keys:
                initial_data_address.append({key: data[key]})
                data.pop(key)

        for i in range(len(initial_data_address)):
            item = initial_data_address[i]
            key = keys_data[i]
            if isinstance(item[key], str):
                item[key] = item[key].title()
            else:
                item[key] = item[key]    

        data_address = {}

        for i in range(len(initial_data_address)):
            item = initial_data_address[i]
            key = keys_data[i]
            
            data_address[key] = item[key]

        AddressModel.validate(**data_address)
        address = create(data_address, AddressModel, '')

        AddressModel.query.filter(AddressModel.street==address.street, AddressModel.number==address.number).first()
            
        data['address_id'] = address.id
            
        PointModel.validate(**data)
        data['path_id'] = path_id
        point = create(data, PointModel, '')
        
        path = PathModel.query.get(path_id)

        path.points.append(point)
            
        current_app.db.session.commit()

        if keys_data.count('initial_date') > 0:
            point.initial_date = point.initial_date.strftime("%d/%m/%Y")
        if keys_data.count('end_date') > 0:
            point.end_date = point.end_date.strftime("%d/%m/%Y")
        
        return jsonify(point), 201

    except KeyError as err:
        return {'error': {'Verify key':str(err)}}, 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotIntegerError as err:
        return jsonify({'error': str(err)}), 400

    except DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400
    
    except EmptyStringError as err:
        return jsonify({'error': str(err)}), 400
    
    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400


@jwt_required()
def points_by_path(path_id: int):
    try:
        path = PathModel.query.get(path_id)

        return {'points': path.points}, 200

    except AttributeError:
        return {'error': 'Point ID Not Found'}, 404


@jwt_required()
def update_point(id: int):
    try:
        data = request.get_json()

        current_user = get_jwt_identity()

        admin_id = current_user['id']

        data['updated_at'] = datetime.now(timezone.utc)
       
        PointModel.validate_user(admin_id, id)

        PointModel.validate_update(**data)

        point = update(PointModel, data, id)

        return point

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404

    except (NotStringError, NotIntegerError, PathOwnerError) as err:
        return jsonify({'error': str(err)}), 400

    except DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400


@jwt_required()
def delete_point(id: int):
    try:
        current_user = get_jwt_identity()
        admin_id = current_user['id']
        PointModel.validate_user(admin_id, id)

        point = delete(PointModel, id)

        return point

    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404

    except PathOwnerError as err:
        return jsonify({'error': str(err)}), 400
