from flask import request, current_app, jsonify
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required
import sqlalchemy
from app.controllers.base_controller import create, delete, update
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
            'city': data['city'],
            'state': data['state'],
            'country': data['country'],
            'postal_code': data['postal_code'],
            'coordenadas': data['coordenadas']
        }
        
        keys_data = list(data.keys())
        for key in keys_data:
            if key=='street' or key =='number' or key=='city' or key=='state' or key=='country' or key=='postal_code' or key=='coordenadas':
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
            
        output = {
            "id": point.id,
            "name": point.name,
            "description": point.description,
            "initial_date": point.initial_date,
            "end_date": point.end_date,
            "duration": point.duration,
            "created_at": point.created_at,
            "updated_at": point.updated_at,
            "activities": point.activities,
            "address_id": point.address_id
        }

        return jsonify(output), 201

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
