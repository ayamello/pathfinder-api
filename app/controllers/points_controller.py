from flask import request, current_app, jsonify
from app.models.points_model import PointModel
from app.models.addresses_model import AddressModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import InvalidRequestError
from ipdb import set_trace


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
        return {'Verify key': str(err)}, 400


def list_all_points():
    points = PointModel.query.order_by(PointModel.id).all()
    return jsonify(points), 200


def all_point_activities(id: int):
    try:
        activities_by_point = PointModel.query.get(id)
        return {'activities': activities_by_point.activities}, 200
    except AttributeError:
        return {'msg': 'ID Not Found'}, 404


def update_point(id: int):
    try:
        data = request.get_json()
        if PointModel.query.filter_by(id=id).update(data):
            current_app.db.session.commit()   
            return '', 204
        return {'msg': 'ID Not Found'}, 404
    except InvalidRequestError as err:
        return jsonify({"error": str(err)}), 400
              

def delete_point(id: int):
    try:
        point = PointModel.query.filter_by(id=id).first()
        current_app.db.session.delete(point)
        current_app.db.session.commit()
        return '', 204
    except UnmappedInstanceError:
        return {'msg': 'ID Not Found'}, 404