from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required
from app.models.points_model import PointModel
from app.models.addresses_model import AddressModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import InvalidRequestError

@jwt_required()
def create_point():
    try:
        data = request.get_json()
        data_address = {'street': data['street'],
                        'number': data['number'],
                        'city': data['city'],
                        'state': data['state'],
                        'country': data['country'],
                        'postal_code': data['postal_code'],
                        'coordenadas': data['coordenadas']
                        }
        address = AddressModel(**data_address)
        current_app.db.session.add(address)

        id_filter = AddressModel.query.filter(AddressModel.street==address.street, AddressModel.number==address.number).first()
        
        data_point = {'name': data['name'],
                    'description': data['description'],
                    'initial_date':data['initial_date'],
                    'end_date': data['end_date'],
                    'duration': data['duration'],
                    'address_id': address.id
                    }
        point = PointModel(**data_point)
        current_app.db.session.add(point)
        current_app.db.session.commit()
        return jsonify(point), 201
    except KeyError as err:
        return {'error': {'Verify key':str(err)}}, 400


def activities_by_point(id: int):
    try:
        activities_by_point = PointModel.query.get(id)
        return {'activities': activities_by_point.activities}, 200
    except AttributeError:
        return {'error': 'Point ID Not Found'}, 404

@jwt_required()
def update_point(id: int):
    try:
        data = request.get_json()
        if PointModel.query.filter_by(id=id).update(data):
            current_app.db.session.commit()  
            point = PointModel.query.get(id)
            return jsonify(point), 200
        return {'error': ' Point ID Not Found'}, 404
    except InvalidRequestError as err:
        return jsonify({"error": str(err)}), 400
              
@jwt_required()
def delete_point(id: int):
    try:
        point = PointModel.query.filter_by(id=id).first()
        current_app.db.session.delete(point)
        current_app.db.session.commit()
        return '', 204
    except UnmappedInstanceError:
        return {'error': 'Point ID Not Found'}, 404