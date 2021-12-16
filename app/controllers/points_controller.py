from flask import request, current_app, jsonify
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required
import sqlalchemy
from app.controllers import create, delete, update
from app.models.paths_model import PathModel
from app.models.points_model import PointModel
from app.models.addresses_model import AddressModel
from app.exceptions.base_exceptions import NotIntegerError, NotStringError, WrongKeysError, NotFoundDataError
from pdb import set_trace


@jwt_required()
def create_point():
    try:
        data = request.get_json()
        path_id = data.pop('path_id')

        data_address = {
            'street': data['street'],
            'number': data['number'],
            'city': data['city'].title(),
            'state': data['state'].title(),
            'country': data['country'].title(),
            'postal_code': data['postal_code'],
            'coordenadas': data['coordenadas']
        }
        
        keys_data = list(data.keys())
        data_address_keys = ['street', 'number', 'city', 'state', 'country', 'postal_code', 'coordenadas']
        
        for key in keys_data:
            if key in data_address_keys:
                data.pop(key)
            
        AddressModel.validate(**data_address)
        address = create(data_address, AddressModel, '')
        AddressModel.query.filter(AddressModel.street==address.street, AddressModel.number==address.number).first()
            
        data['address_id'] = address.id
            
        PointModel.validate(**data)
        point = create(data, PointModel, '')

        path = PathModel.query.get(path_id)
        path.points.append(point)
            
        current_app.db.session.commit()

        if keys_data.count('initial_date') > 0:
            point.initial_date = point.initial_date.strftime("%d/%m/%Y")
        if keys_data.count('end_date') > 0:
            point.initial_date = point.end_date.strftime("%d/%m/%Y")

        return jsonify(point), 201

    except KeyError as err:
        return {'error': {'Verify key':str(err)}}, 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotIntegerError as err:
        return jsonify({'error': str(err)}), 400

    except sqlalchemy.exc.DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400


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
        data['updated_at'] = datetime.now(timezone.utc)

        PointModel.validate_update(**data)
        point = update(PointModel, data, id)

        return point

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except NotIntegerError as err:
        return jsonify({'error': str(err)}), 400

    except sqlalchemy.exc.DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400


@jwt_required()
def delete_point(id: int):
    try:
        point = delete(PointModel, id)

    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404

    return point
