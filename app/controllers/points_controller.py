from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.__init__ import create, delete, update
from app.exceptions.activities_subscribers_exception import NotFoundDataError
from app.models.paths_model import PathModel
from app.models.points_model import PointModel
from app.models.addresses_model import AddressModel


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

        address = create(data_address, AddressModel, '')

        AddressModel.query.filter(AddressModel.street==address.street, AddressModel.number==address.number).first()
        
        data_point = {
            'name': data['name'],
            'description': data['description'],
            'initial_date':data['initial_date'],
            'end_date': data['end_date'],
            'duration': data['duration'],
            'address_id': address.id
        }

        point = create(data_point, PointModel, '')

        path = PathModel.query.get(path_id)
        path.points.append(point)
        
        current_app.db.session.commit()

        return jsonify(point), 201

    except KeyError as err:
        return {'error': {'Verify key':str(err)}}, 400


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

        point = update(PointModel, data, id)

        return point
    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404


@jwt_required()
def delete_point(id: int):
    try:
        point = delete(PointModel, id)

    except NotFoundDataError:
        return {'error': 'Point ID Not Found'}, 404

    return point
